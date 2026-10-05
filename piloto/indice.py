"""DecibHello: índice de ruido de toda Barcelona para el buscador del visor.

Para cada portal de la ciudad (listado oficial de adreces d'edificis) busca:
- el tramo del mapa estratégico de ruido 2017 que da a su calle (fachada exterior);
- el tramo de patio interior de manzana más cercano (fachada interior);
- los focos intermitentes a menos de 100 m (ocio nocturno, bares y restaurantes, quejas por ruido, pisos turísticos);
- la distancia al sensor municipal de ruido activo más cercano.
Los portales consecutivos de una calle con el mismo resultado se agrupan en rangos de números.

Uso: python3 piloto/indice.py   ->  piloto/cache/indice.json (lo incrusta construir_visor en visor.html)
"""

import json
import math
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np
from pyproj import Transformer
from shapely import wkt
from shapely.geometry import Point
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
RES_ADRECES = "661fe190-67c8-423a-b8eb-8140f547fde2"
RES_CARRERER = "2b010e59-6952-4b27-9c4e-47fcaf64c916"

BANDAS = ["< 40 dB(A)", "40 - 45 dB(A)", "45 - 50 dB(A)", "50 - 55 dB(A)", "55 - 60 dB(A)",
          "60 - 65 dB(A)", "65 - 70 dB(A)", "70 - 75 dB(A)", "75 - 80 dB(A)"]
CAMPOS_TRAMO = ["TOTAL_D", "TOTAL_E", "TOTAL_N", "TRANSIT_D", "TRANSIT_E", "TRANSIT_N", "OCI_N"]
RADIO_FOCOS = 100
RADIO_TRAMO = 50
RADIO_PATIO = 50
PENALIZACION_ANGULO = 40  # metros extra para un tramo perpendicular a la calle (la calle de al lado)

a_wgs = Transformer.from_crs("EPSG:25831", "EPSG:4326", always_xy=True)
a_utm = Transformer.from_crs("EPSG:4326", "EPSG:25831", always_xy=True)


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def con_cache(nombre, obtener):
    f = CACHE / f"{nombre}.json"
    if f.exists():
        return json.loads(f.read_text())
    datos = obtener()
    CACHE.mkdir(exist_ok=True)
    f.write_text(json.dumps(datos))
    return datos


def sql(nombre, consulta):
    return con_cache(nombre, lambda: get_json(API + "datastore_search_sql?" + urllib.parse.urlencode({"sql": consulta}))["result"]["records"])


def todo(nombre, recurso, campos):
    """Descarga un recurso completo por páginas."""
    def obtener():
        filas, offset = [], 0
        while True:
            q = urllib.parse.urlencode({"resource_id": recurso, "limit": 20000, "offset": offset, "fields": ",".join(campos)})
            r = get_json(API + "datastore_search?" + q)["result"]
            filas += r["records"]
            offset += 20000
            if offset >= r["total"]:
                return filas
            time.sleep(0.5)
    return con_cache(nombre, obtener)


def puntos(recs, lat, lon):
    out = []
    for r in recs:
        try:
            out.append(a_utm.transform(float(r[lon]), float(r[lat])))
        except (TypeError, ValueError):
            pass
    return np.array(out)


def direccion_tramo(g):
    coords = [c for parte in getattr(g, "geoms", [g]) for c in parte.coords]
    (x0, y0), (x1, y1) = coords[0], coords[-1]
    v = np.array([x1 - x0, y1 - y0])
    n = np.linalg.norm(v)
    return v / n if n else np.array([1.0, 0.0])


def direcciones_calle(xy):
    """Dirección local de la calle en cada portal: eje principal de los portales de la misma calle a menos de 70 m."""
    out = np.zeros_like(xy)
    for i, p in enumerate(xy):
        cerca = xy[np.hypot(*(xy - p).T) <= 70]
        if len(cerca) < 3:
            out[i] = np.nan
            continue
        c = cerca - cerca.mean(axis=0)
        _, _, vt = np.linalg.svd(c, full_matrices=False)
        out[i] = vt[0]
    return out


def main():
    tramer = sql("tramer2017_v2", f'SELECT "TRAM","TOTAL_D","TOTAL_E","TOTAL_N","TRANSIT_D","TRANSIT_E","TRANSIT_N","OCI_N","GEOM_WKT" FROM "{RES_TRAMER_2017}"')
    adreces = todo("adreces_edificis", RES_ADRECES, ["codi_carrer", "numpost_i", "numpost_f", "nom_barri", "x_etrs89", "y_etrs89"])
    carrerer = todo("carrerer", RES_CARRERER, ["codi_via", "nom_oficial"])
    oci = puntos(sql("cens_oci", f'SELECT "Latitud","Longitud" FROM "{RES_CENS_2024}" WHERE "SN_Oci_Nocturn"=\'Si\''), "Latitud", "Longitud")
    bars = puntos(sql("cens_bars", f'SELECT "Latitud","Longitud" FROM "{RES_CENS_2024}" WHERE "Nom_Grup_Activitat" ILIKE \'Restaurants, bars%\''), "Latitud", "Longitud")
    queixes = puntos(sql("iris2025_soroll", f'SELECT "LATITUD","LONGITUD" FROM "{RES_IRIS_2025}" WHERE "ELEMENT"=\'Molèsties soroll a la via pública\''), "LATITUD", "LONGITUD")
    hut = puntos(sql("hut", f'SELECT "LATITUD_Y","LONGITUD_X" FROM "{RES_HUT}"'), "LATITUD_Y", "LONGITUD_X")
    sensors = puntos(sql("sensors_actius", f'SELECT "Latitud","Longitud" FROM "{RES_SENSORS}" WHERE "Data_DesInstalacio" IS NULL'), "Latitud", "Longitud")
    print(f"tramos {len(tramer)} · portales {len(adreces)} · calles {len(carrerer)}")

    geoms = [wkt.loads(t["GEOM_WKT"]) for t in tramer]
    es_patio = np.array([t["TRAM"].startswith("P") for t in tramer])
    dir_tramo = np.array([direccion_tramo(g) for g in geoms])
    arbol = STRtree(geoms)

    nombres = {str(int(float(c["codi_via"]))): c["nom_oficial"] for c in carrerer}

    # Portales válidos agrupados por calle.
    por_calle = defaultdict(list)
    for a in adreces:
        try:
            x, y = float(a["x_etrs89"]), float(a["y_etrs89"])
            ni = int(float(a["numpost_i"]))
            nf = int(float(a["numpost_f"] or a["numpost_i"]))
        except (TypeError, ValueError):
            continue
        codi = str(int(float(a["codi_carrer"])))
        if codi not in nombres or ni <= 0:
            continue
        por_calle[codi].append((ni, max(ni, nf), x, y, (a["nom_barri"] or "").strip()))

    # Tramo exterior y patio de cada portal.
    todos = [(codi, p) for codi, ps in por_calle.items() for p in ps]
    xy = np.array([[p[2], p[3]] for _, p in todos])
    dir_calle = np.zeros_like(xy)
    inicio = 0
    for codi, ps in por_calle.items():
        n = len(ps)
        dir_calle[inicio:inicio + n] = direcciones_calle(xy[inicio:inicio + n])
        inicio += n
    pts = [Point(x, y) for x, y in xy]
    pares = arbol.query(pts, predicate="dwithin", distance=max(RADIO_TRAMO, RADIO_PATIO))
    mejor = np.full(len(pts), -1)
    mejor_coste = np.full(len(pts), np.inf)
    patio = np.full(len(pts), -1)
    patio_d = np.full(len(pts), np.inf)
    for ip, it in zip(*pares):
        d = geoms[it].distance(pts[ip])
        if es_patio[it]:
            if d < patio_d[ip] and d <= RADIO_PATIO:
                patio_d[ip], patio[ip] = d, it
            continue
        if d > RADIO_TRAMO:
            continue
        dc = dir_calle[ip]
        seno = 0.0 if np.isnan(dc[0]) else abs(dc[0] * dir_tramo[it][1] - dc[1] * dir_tramo[it][0])
        coste = d + PENALIZACION_ANGULO * seno
        if coste < mejor_coste[ip]:
            mejor_coste[ip], mejor[ip] = coste, it
    print(f"portales con tramo: {(mejor >= 0).sum()} de {len(pts)} · con patio: {(patio >= 0).sum()}")

    # Agrupar en rangos de números (por paridad) con el mismo tramo y patio.
    usados = {}
    def idx_tramo(i):
        if i < 0:
            return -1
        if i not in usados:
            usados[i] = len(usados)
        return usados[i]

    barrios = []
    def idx_barrio(nombre):
        if nombre not in barrios:
            barrios.append(nombre)
        return barrios.index(nombre)

    rangos_calle = {}
    pos = 0
    for codi, ps in por_calle.items():
        filas = []
        for k, p in enumerate(ps):
            j = pos + k
            if mejor[j] >= 0:
                filas.append((p[0] % 2, p[0], p[1], int(mejor[j]), int(patio[j]), xy[j], p[4]))
        pos += len(ps)
        filas.sort(key=lambda f: (f[0], f[1]))
        rangos = []
        for par, ni, nf, t, pt, punto, barrio in filas:
            r = rangos[-1] if rangos else None
            if r and r["par"] == par and r["t"] == t and r["p"] == pt:
                r["fin"] = max(r["fin"], nf)
                r["xy"].append(punto)
            else:
                rangos.append({"par": par, "ini": ni, "fin": nf, "t": t, "p": pt, "xy": [punto], "barrio": barrio})
        if rangos:
            rangos_calle[codi] = rangos

    # Focos y sensor por rango (en su punto central).
    todos_r = [r for rs in rangos_calle.values() for r in rs]
    centros = np.array([np.mean(r["xy"], axis=0) for r in todos_r])

    def contar(nube):
        if not len(nube):
            return np.zeros(len(centros), dtype=int)
        out = np.zeros(len(centros), dtype=int)
        for i0 in range(0, len(centros), 2000):
            c = centros[i0:i0 + 2000]
            d = np.hypot(c[:, None, 0] - nube[None, :, 0], c[:, None, 1] - nube[None, :, 1])
            out[i0:i0 + 2000] = (d <= RADIO_FOCOS).sum(axis=1)
        return out

    n_oci, n_bar, n_quej, n_hut = contar(oci), contar(bars), contar(queixes), contar(hut)
    d_sens = np.min(np.hypot(centros[:, None, 0] - sensors[None, :, 0], centros[:, None, 1] - sensors[None, :, 1]), axis=1)
    lon, lat = a_wgs.transform(centros[:, 0], centros[:, 1])

    k = 0
    salida_calles = []
    for codi, rs in rangos_calle.items():
        planos = []
        for r in rs:
            planos += [r["ini"], r["fin"], idx_tramo(r["t"]), idx_tramo(r["p"]), idx_barrio(r["barrio"]),
                       int(n_oci[k]), int(n_bar[k]), int(n_quej[k]), int(n_hut[k]), int(round(d_sens[k] / 10)),
                       int(round((lat[k] - 41.3) * 1e5)), int(round((lon[k] - 2.0) * 1e5))]
            k += 1
        salida_calles.append([nombres[codi], planos])

    tramos = [None] * len(usados)
    for i, j in usados.items():
        tramos[j] = "".join(str(BANDAS.index(tramer[i][c])) for c in CAMPOS_TRAMO)

    indice = {"bandas": BANDAS, "campos_tramo": CAMPOS_TRAMO, "tramos": tramos, "barrios": barrios,
              "campos_rango": ["ini", "fin", "tramo", "patio", "barrio", "ocio", "bares", "quejas", "turisticos", "sensor_dam", "lat_e5", "lon_e5"],
              "origen": {"lat": 41.3, "lon": 2.0}, "calles": salida_calles}
    (CACHE / "indice.json").write_text(json.dumps(indice, ensure_ascii=False, separators=(",", ":")))
    print(f"calles {len(salida_calles)} · rangos {len(todos_r)} · tramos usados {len(tramos)} · "
          f"{(CACHE / 'indice.json').stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
