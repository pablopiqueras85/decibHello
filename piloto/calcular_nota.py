"""DecibHello: primera nota de ruido 0-100 (100 = muy ruidoso) para las direcciones del piloto.

Fuentes (Open Data BCN, CC BY 4.0, leídas por la API del portal):
- Mapa estratégico de ruido 2017 por tramo de calle.
- Censo de locales en planta baja 2024 (ocio nocturno, bares y restaurantes).
- Quejas IRIS 2025 por ruido en la vía pública.
- Viviendas de uso turístico.
- Instalaciones de la red de sensores de ruido.
Geocodificación: OpenStreetMap Nominatim.

Uso: python3 piloto/calcular_nota.py  ->  piloto/resultados.csv
"""

import csv
import json
import math
import time
import urllib.parse
import urllib.request
from pathlib import Path

from pyproj import Transformer
from shapely import wkt
from shapely.geometry import LineString, Point
from shapely.ops import unary_union
from shapely.strtree import STRtree

AQUI = Path(__file__).parent
CACHE = AQUI / "cache"
API = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/"
UA = {"User-Agent": "DecibHello-pilot/0.1 (research)"}

RES_TRAMER_2017 = "3ef70228-789c-47f7-8712-d3789b01a82e"
RES_CENS_2024 = "38babeec-5c47-43d3-84e7-b13a4b89004f"
RES_IRIS_2025 = "efc9fd4d-a812-427c-846d-a086d22012a4"
RES_HUT = "b32fa7f6-d464-403b-8a02-0292a64883bf"
RES_SENSORS = "f4562942-1fd8-48fb-9e9d-d41088f97a03"

RADIO_M = 100  # radio para contar focos cercanos
RADIO_SENSOR_M = 150  # sensor "cercano" para la confianza alta

# Pesos de cada franja en la nota global: la noche pesa más.
PESOS = {"D": 0.3, "E": 0.2, "N": 0.5}
# Nivel (dB) que da 50 puntos en cada franja; cada 3 dB más suman unos 5 puntos (30 dB = 50 puntos).
# Noche: 45 dB es la recomendación OMS (Lnight, tráfico); día y tarde, un margen equivalente.
ANCLA_50 = {"D": 55, "E": 50, "N": 45}
PUNTOS_POR_DB = 50 / 30

a_utm = Transformer.from_crs("EPSG:4326", "EPSG:25831", always_xy=True)


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def sql(nombre, consulta):
    """Ejecuta una consulta SQL en la API del portal, con caché local."""
    f = CACHE / f"{nombre}.json"
    if f.exists():
        return json.loads(f.read_text())
    url = API + "datastore_search_sql?" + urllib.parse.urlencode({"sql": consulta})
    recs = get_json(url)["result"]["records"]
    CACHE.mkdir(exist_ok=True)
    f.write_text(json.dumps(recs))
    return recs


def geocodificar(direcciones):
    f = CACHE / "geocodigos.json"
    cache = json.loads(f.read_text()) if f.exists() else {}
    for d in direcciones:
        if d in cache:
            continue
        q = urllib.parse.urlencode({"q": d + ", Barcelona", "format": "json", "limit": 1})
        r = get_json("https://nominatim.openstreetmap.org/search?" + q)
        cache[d] = [float(r[0]["lat"]), float(r[0]["lon"])] if r else None
        time.sleep(1.1)  # política de uso de Nominatim: 1 petición por segundo
    CACHE.mkdir(exist_ok=True)
    f.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
    return cache


def banda_a_db(texto):
    """'60 - 65 dB(A)' -> 62.5 ; '< 40 dB(A)' -> 37.5"""
    t = texto.replace("dB(A)", "").strip()
    if t.startswith("<"):
        return float(t[1:]) - 2.5
    lo, hi = (float(x) for x in t.split("-"))
    return (lo + hi) / 2


def nota_franja(db, franja):
    return max(0.0, min(100.0, 50 + (db - ANCLA_50[franja]) * PUNTOS_POR_DB))


def lineas_calle(direccion, lat, lon):
    """Geometría (UTM) de la calle de la dirección cerca del punto, desde Nominatim."""
    f = CACHE / "calles.json"
    cache = json.loads(f.read_text()) if f.exists() else {}
    if direccion not in cache:
        calle = direccion.rsplit(" ", 1)[0]
        d = 0.001  # ~100 m
        q = urllib.parse.urlencode({"street": calle, "city": "Barcelona", "format": "jsonv2", "polygon_geojson": 1, "limit": 20,
                                    "viewbox": f"{lon-d},{lat+d},{lon+d},{lat-d}", "bounded": 1})
        r = get_json("https://nominatim.openstreetmap.org/search?" + q)
        cache[direccion] = [x["geojson"]["coordinates"] for x in r if x["geojson"]["type"] == "LineString"]
        time.sleep(1.1)
        f.write_text(json.dumps(cache, ensure_ascii=False))
    return [LineString([a_utm.transform(*c) for c in coords]) for coords in cache[direccion] if len(coords) > 1]


def elegir_tramo(p, calle, geoms, tramer, arbol):
    """Tramo de fachada a la calle (no patio) que coincide con la calle de la dirección."""
    cand = [int(i) for i in arbol.query(p.buffer(60))]
    calle_buf = unary_union(calle).buffer(20) if calle else None
    mejores = []
    for i in cand:
        if tramer[i]["TRAM"].startswith("P"):
            continue
        g = geoms[i]
        solape = g.intersection(calle_buf).length / g.length if calle_buf is not None and g.length else 0
        mejores.append((solape < 0.5, g.distance(p), i))
    if not mejores:
        return None, False
    mejores.sort()
    return mejores[0][2], not mejores[0][0]


def patio(p, geoms, tramer, arbol):
    """Nivel de noche de la fachada interior (patio de manzana) más cercana, si la hay."""
    cand = [(geoms[int(i)].distance(p), int(i)) for i in arbol.query(p.buffer(60)) if tramer[int(i)]["TRAM"].startswith("P")]
    return tramer[min(cand)[1]]["TOTAL_N"] if cand else ""


def puntos_utm(recs, lat, lon):
    pts = []
    for r in recs:
        try:
            pts.append(a_utm.transform(float(r[lon]), float(r[lat])))
        except (TypeError, ValueError):
            pass
    return pts


def contar(pts, x, y, radio=RADIO_M):
    return sum(1 for px, py in pts if math.hypot(px - x, py - y) <= radio)


def main():
    direcciones = [l.split("|")[0].strip() for l in (AQUI / "direcciones.txt").read_text().splitlines() if l.strip() and not l.startswith("#")]
    etiquetas = {l.split("|")[0].strip(): l.split("|")[1].strip() for l in (AQUI / "direcciones.txt").read_text().splitlines() if "|" in l and not l.startswith("#")}
    geo = geocodificar(direcciones)

    tramer = sql("tramer2017", f'SELECT "TRAM","TOTAL_D","TOTAL_E","TOTAL_N","TRANSIT_N","OCI_N","GEOM_WKT" FROM "{RES_TRAMER_2017}"')
    geoms = [wkt.loads(t["GEOM_WKT"]) for t in tramer]
    arbol = STRtree(geoms)

    oci = puntos_utm(sql("cens_oci", f'SELECT "Latitud","Longitud" FROM "{RES_CENS_2024}" WHERE "SN_Oci_Nocturn"=\'Si\''), "Latitud", "Longitud")
    bars = puntos_utm(sql("cens_bars", f'SELECT "Latitud","Longitud" FROM "{RES_CENS_2024}" WHERE "Nom_Grup_Activitat" ILIKE \'Restaurants, bars%\''), "Latitud", "Longitud")
    queixes = puntos_utm(sql("iris2025_soroll", f'SELECT "LATITUD","LONGITUD" FROM "{RES_IRIS_2025}" WHERE "ELEMENT"=\'Molèsties soroll a la via pública\''), "LATITUD", "LONGITUD")
    hut = puntos_utm(sql("hut", f'SELECT "LATITUD_Y","LONGITUD_X" FROM "{RES_HUT}"'), "LATITUD_Y", "LONGITUD_X")
    sensors = puntos_utm(sql("sensors_actius", f'SELECT "Latitud","Longitud" FROM "{RES_SENSORS}" WHERE "Data_DesInstalacio" IS NULL'), "Latitud", "Longitud")

    filas = []
    for d in direcciones:
        if not geo.get(d):
            print("Sin geocodificar:", d)
            continue
        lat, lon = geo[d]
        x, y = a_utm.transform(lon, lat)
        p = Point(x, y)
        i, por_calle = elegir_tramo(p, lineas_calle(d, lat, lon), geoms, tramer, arbol)
        t = tramer[i]
        dist_tram = geoms[i].distance(p)

        db = {f: banda_a_db(t[f"TOTAL_{f}"]) for f in "DEN"}
        nota = {f: nota_franja(db[f], f) for f in "DEN"}

        n_oci, n_bar = contar(oci, x, y), contar(bars, x, y)
        n_queixes, n_hut = contar(queixes, x, y), contar(hut, x, y)
        # Focos intermitentes: suben la nota de tarde y de noche (no están bien recogidos en una media anual).
        # Máximo 25 puntos extra de noche (la mitad de tarde).
        extra = min(10, 4 * n_oci) + min(6, 1.2 * math.sqrt(n_bar)) + min(6, 2 * math.sqrt(n_queixes)) + min(3, math.sqrt(n_hut) / 3)
        nota["E"] = min(100.0, nota["E"] + extra * 0.5)
        nota["N"] = min(100.0, nota["N"] + extra)
        global_ = sum(PESOS[f] * nota[f] for f in "DEN")

        d_sensor = min(math.hypot(sx - x, sy - y) for sx, sy in sensors)
        confianza = "alta" if d_sensor <= RADIO_SENSOR_M else "media"
        if not por_calle or dist_tram > 40:
            confianza = "baja"

        filas.append({
            "direccion": d, "grupo": etiquetas.get(d, ""),
            "nota_global": round(global_), "nota_dia": round(nota["D"]), "nota_tarde": round(nota["E"]), "nota_noche": round(nota["N"]),
            "mes_dia": t["TOTAL_D"], "mes_tarde": t["TOTAL_E"], "mes_noche": t["TOTAL_N"],
            "mes_trafico_noche": t["TRANSIT_N"], "mes_ocio_noche": t["OCI_N"], "mes_patio_noche": patio(p, geoms, tramer, arbol),
            "ocio_nocturno_100m": n_oci, "bares_rest_100m": n_bar, "quejas_ruido_100m": n_queixes, "pisos_turisticos_100m": n_hut,
            "sensor_mas_cercano_m": round(d_sensor), "distancia_tramo_m": round(dist_tram, 1), "confianza": confianza,
        })

    with open(AQUI / "resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    for r in sorted(filas, key=lambda r: -r["nota_global"]):
        print(f'{r["nota_global"]:>3}  D{r["nota_dia"]:>3} T{r["nota_tarde"]:>3} N{r["nota_noche"]:>3}  {r["grupo"]:<11} {r["direccion"]:<42} '
              f'noche {r["mes_noche"]:<14} patio {r["mes_patio_noche"]:<14} oci{r["ocio_nocturno_100m"]:>2} bar{r["bares_rest_100m"]:>3} quej{r["quejas_ruido_100m"]:>3} hut{r["pisos_turisticos_100m"]:>3} '
              f'sens {r["sensor_mas_cercano_m"]:>5}m tramo {r["distancia_tramo_m"]:>5}m {r["confianza"]}')


if __name__ == "__main__":
    main()
