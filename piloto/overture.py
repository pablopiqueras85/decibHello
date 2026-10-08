"""Bares y locales de noche de Overture Maps en Barcelona (base abierta de negocios, se publica cada mes).

Fuente: Overture Maps Foundation, tema "places" (datos de Meta, Microsoft, Foursquare y otros). Licencia CDLA-Permissive 2.0
(lo de Foursquare, Apache 2.0): se puede guardar y usar en un producto comercial citando la fuente.
Se descarga con DuckDB, sin registro. Para actualizar: pon en VERSION la última de https://docs.overturemaps.org/release/latest/
y ejecuta `python3 piloto/overture.py` (si existe piloto/cache/overture/bcn_places.parquet de otra versión, bórralo antes).

Resultado: piloto/datos/overture_locales.json.gz con los bares y los locales de noche (confianza ≥ 0,7, sin los cerrados):
{"version", "bares": [[lat, lon], …], "noche": [[lat, lon], …]}. locales.py los combina con el censo del Ajuntament.
Estudio previo (7 oct 2026): por sí solo predice el ruido igual de bien que el censo (fuentes-datos-barcelona.md, 2.18).
"""
import gzip
import json
import sys
from pathlib import Path

AQUI = Path(__file__).parent
PARQUET = AQUI / "cache" / "overture" / "bcn_places.parquet"
SALIDA = AQUI / "datos" / "overture_locales.json.gz"
VERSION = "2026-09-23.1"
CAJA = (2.05, 2.23, 41.32, 41.47)  # lon mín, lon máx, lat mín, lat máx (Barcelona)
CONFIANZA_MIN = 0.7
BARES = ["bar", "wine_bar", "beer_bar", "brewery", "sports_bar", "tapas_bar"]
NOCHE = ["dance_club", "cocktail_bar", "pub", "music_venue", "lounge", "hookah_bar", "gay_bar", "irish_pub",
         "speakeasy", "dive_bar", "beer_garden"]


def descargar(con):
    PARQUET.parent.mkdir(parents=True, exist_ok=True)
    con.execute("INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial; "
                "CREATE SECRET anon (TYPE s3, KEY_ID '', SECRET '', REGION 'us-west-2');")
    x0, x1, y0, y1 = CAJA
    con.execute(f"""
        COPY (
          SELECT id, names.primary AS nombre, taxonomy.primary AS categoria, operating_status, confidence,
                 ST_X(geometry) AS lon, ST_Y(geometry) AS lat, sources[1].dataset AS fuente, sources[1].update_time AS actualizado
          FROM read_parquet('s3://overturemaps-us-west-2/release/{VERSION}/theme=places/type=place/*', hive_partitioning=1)
          WHERE bbox.xmin BETWEEN {x0} AND {x1} AND bbox.ymin BETWEEN {y0} AND {y1}
        ) TO '{PARQUET}' (FORMAT PARQUET)""")


def main():
    import duckdb
    con = duckdb.connect()
    if not PARQUET.exists():
        print("descargando Overture", VERSION)
        descargar(con)

    def puntos(categorias):
        lista = ",".join(f"'{c}'" for c in categorias)
        filas = con.execute(f"""SELECT round(lat, 6), round(lon, 6) FROM '{PARQUET}'
                                WHERE categoria IN ({lista}) AND confidence >= {CONFIANZA_MIN}
                                  AND coalesce(operating_status, '') <> 'permanently_closed'
                                ORDER BY 1, 2""").fetchall()
        return [list(f) for f in filas]

    datos = {"version": VERSION, "fuente": "Overture Maps Foundation (places), CDLA-Permissive 2.0",
             "confianza_min": CONFIANZA_MIN, "bares": puntos(BARES), "noche": puntos(NOCHE)}
    SALIDA.parent.mkdir(exist_ok=True)
    with gzip.open(SALIDA, "wt", encoding="utf-8") as f:
        json.dump(datos, f, separators=(",", ":"))
    print(f"Overture {VERSION}: {len(datos['bares'])} bares y {len(datos['noche'])} locales de noche "
          f"(confianza ≥ {CONFIANZA_MIN}) · {SALIDA.stat().st_size / 1e3:.0f} kB")


if __name__ == "__main__":
    sys.exit(main())
