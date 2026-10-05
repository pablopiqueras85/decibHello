"""DecibHello: nota de ruido 0-100 (100 = muy ruidoso), hora a hora, para las direcciones del piloto.

Fuentes (Open Data BCN, CC BY 4.0, leídas por la API del portal):
- Mapa estratégico de ruido 2017 por tramo de calle.
- Censo de locales en planta baja 2024 (ocio nocturno, bares y restaurantes).
- Quejas IRIS 2025 por ruido en la vía pública.
- Viviendas de uso turístico.
- Instalaciones de la red de sensores de ruido.
Geocodificación y geometría de calles: OpenStreetMap Nominatim.

Uso: python3 piloto/calcular_nota.py
Salidas: piloto/resultados.csv, tabla en piloto/resultados.md y piloto/visor.html (desde visor_plantilla.html).
"""

import csv
import json
import math
import re
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

# Franjas del mapa oficial: día 7-19 h, tarde 19-23 h, noche 23-7 h.
FRANJA = ["N"] * 7 + ["D"] * 12 + ["E"] * 4 + ["N"]
HORAS = {f: [h for h in range(24) if FRANJA[h] == f] for f in "DEN"}
# Pesos de cada franja en la nota global: la noche pesa más.
PESOS = {"D": 0.3, "E": 0.2, "N": 0.5}
# Nivel (dB) que da 50 puntos en cada franja. Es la misma penalización que el indicador europeo Lden
# (+5 dB tarde, +10 dB noche); de noche, 45 dB es la recomendación OMS para tráfico.
ANCLA_50 = {"D": 55, "E": 50, "N": 45}
PUNTOS_POR_DB = 50 / 30

# Forma típica del ruido de tráfico urbano a lo largo del día (dB relativos a la hora punta).
PERFIL_TRAFICO = [-6, -8, -9, -10, -10, -8, -4, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -2, -3, -4, -5]
# Forma del ruido de ocio nocturno dentro de la franja de noche (pico entre las 23 y la 1).
PERFIL_OCIO = {23: 0, 0: 0, 1: -1, 2: -3, 3: -6, 4: -9, 5: -12, 6: -15}
# Reparto horario de los focos intermitentes (bares, quejas, pisos turísticos): peso 1 = todo el extra en esa hora.
REPARTO_FOCOS = {19: 0.3, 20: 0.4, 21: 0.5, 22: 0.7, 23: 1, 0: 1, 1: 1, 2: 0.8, 3: 0.5, 4: 0.2}

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


def tramo_patio(p, geoms, tramer, arbol):
    """Fachada interior (patio de manzana, código P) más cercana, si la hay a menos de 60 m."""
    cand = [(geoms[int(i)].distance(p), int(i)) for i in arbol.query(p.buffer(60)) if tramer[int(i)]["TRAM"].startswith("P")]
    return tramer[min(cand)[1]] if cand else None


def banda_a_db(texto):
    """'60 - 65 dB(A)' -> 62.5 ; '< 40 dB(A)' -> 37.5"""
    t = texto.replace("dB(A)", "").strip()
    if t.startswith("<"):
        return float(t[1:]) - 2.5
    lo, hi = (float(x) for x in t.split("-"))
    return (lo + hi) / 2


def energia(db):
    return 10 ** (db / 10)


def perfil_horario(total, trafico=None, ocio_noche=None):
    """Reparte los niveles oficiales de día, tarde y noche en 24 horas.

    Dentro de cada franja, el tráfico sigue PERFIL_TRAFICO y el ocio nocturno PERFIL_OCIO; el resto del ruido
    se reparte plano. Después se reescala para que la media energética de cada franja sea la del mapa oficial.
    """
    db = [0.0] * 24
    for f, horas in HORAS.items():
        e_total = energia(total[f])
        comp = {h: 0.0 for h in horas}
        e_usada = 0.0
        if trafico:
            forma = {h: energia(PERFIL_TRAFICO[h]) for h in horas}
            k = energia(trafico[f]) / (sum(forma.values()) / len(horas))
            for h in horas:
                comp[h] += forma[h] * k
            e_usada += energia(trafico[f])
        if ocio_noche is not None and f == "N":
            forma = {h: energia(PERFIL_OCIO[h]) for h in horas}
            k = energia(ocio_noche) / (sum(forma.values()) / len(horas))
            for h in horas:
                comp[h] += forma[h] * k
            e_usada += energia(ocio_noche)
        resto = max(0.0, e_total - e_usada)
        if not trafico:  # sin desglose: forma de tráfico para todo
            forma = {h: energia(PERFIL_TRAFICO[h]) for h in horas}
            k = e_total / (sum(forma.values()) / len(horas))
            comp = {h: forma[h] * k for h in horas}
            resto = 0.0
        for h in horas:
            comp[h] += resto
        ajuste = e_total / (sum(comp.values()) / len(horas))
        for h in horas:
            db[h] = 10 * math.log10(comp[h] * ajuste)
    # Suaviza el salto entre franjas (6-7 h, 18-19 h, 22-23 h) conservando la energía de cada pareja de horas.
    for h1, h2 in ((6, 7), (18, 19), (22, 23)):
        e1, e2 = energia(db[h1]), energia(db[h2])
        db[h1], db[h2] = 10 * math.log10((2 * e1 + e2) / 3), 10 * math.log10((e1 + 2 * e2) / 3)
    return db


def suavizar_extremos(v):
    """Comprime suavemente por encima de 70 y por debajo de 30 para no saturar en 0 o 100 y mantener el orden."""
    if v > 70:
        return 70 + 30 * (1 - math.exp(-(v - 70) / 30))
    if v < 30:
        return 30 - 30 * (1 - math.exp(-(30 - v) / 30))
    return v


def notas_horarias(db, extra):
    """Nota 0-100 de cada hora: nivel respecto al umbral de su franja + focos intermitentes repartidos por hora."""
    return [suavizar_extremos(50 + (db[h] - ANCLA_50[FRANJA[h]]) * PUNTOS_POR_DB + extra * REPARTO_FOCOS.get(h, 0)) for h in range(24)]


def resumen(notas):
    franjas = {f: sum(notas[h] for h in HORAS[f]) / len(HORAS[f]) for f in "DEN"}
    return franjas, sum(PESOS[f] * franjas[f] for f in "DEN")


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


def leer_direcciones():
    filas = []
    for linea in (AQUI / "direcciones.txt").read_text(encoding="utf-8").splitlines():
        if not linea.strip() or linea.startswith("#"):
            continue
        partes = [x.strip() for x in linea.split("|")] + ["", "", ""]
        filas.append({"direccion": partes[0], "grupo": partes[1], "barrio": partes[2], "aviso": partes[3]})
    return filas


def main():
    direcciones = leer_direcciones()
    geo = geocodificar([d["direccion"] for d in direcciones])

    tramer = sql("tramer2017_v2", f'SELECT "TRAM","TOTAL_D","TOTAL_E","TOTAL_N","TRANSIT_D","TRANSIT_E","TRANSIT_N","OCI_N","GEOM_WKT" FROM "{RES_TRAMER_2017}"')
    geoms = [wkt.loads(t["GEOM_WKT"]) for t in tramer]
    arbol = STRtree(geoms)

    oci = puntos_utm(sql("cens_oci", f'SELECT "Latitud","Longitud" FROM "{RES_CENS_2024}" WHERE "SN_Oci_Nocturn"=\'Si\''), "Latitud", "Longitud")
    bars = puntos_utm(sql("cens_bars", f'SELECT "Latitud","Longitud" FROM "{RES_CENS_2024}" WHERE "Nom_Grup_Activitat" ILIKE \'Restaurants, bars%\''), "Latitud", "Longitud")
    queixes = puntos_utm(sql("iris2025_soroll", f'SELECT "LATITUD","LONGITUD" FROM "{RES_IRIS_2025}" WHERE "ELEMENT"=\'Molèsties soroll a la via pública\''), "LATITUD", "LONGITUD")
    hut = puntos_utm(sql("hut", f'SELECT "LATITUD_Y","LONGITUD_X" FROM "{RES_HUT}"'), "LATITUD_Y", "LONGITUD_X")
    sensors = puntos_utm(sql("sensors_actius", f'SELECT "Latitud","Longitud" FROM "{RES_SENSORS}" WHERE "Data_DesInstalacio" IS NULL'), "Latitud", "Longitud")

    filas, visor = [], []
    for info in direcciones:
        d = info["direccion"]
        if not geo.get(d):
            print("Sin geocodificar:", d)
            continue
        lat, lon = geo[d]
        x, y = a_utm.transform(lon, lat)
        p = Point(x, y)
        i, por_calle = elegir_tramo(p, lineas_calle(d, lat, lon), geoms, tramer, arbol)
        t = tramer[i]
        dist_tram = geoms[i].distance(p)

        n_oci, n_bar = contar(oci, x, y), contar(bars, x, y)
        n_queixes, n_hut = contar(queixes, x, y), contar(hut, x, y)
        # Focos intermitentes: hasta 25 puntos extra en las horas punta del ocio (23-1 h), menos el resto de la noche y la tarde.
        extra = min(10, 4 * n_oci) + min(6, 1.2 * math.sqrt(n_bar)) + min(6, 2 * math.sqrt(n_queixes)) + min(3, math.sqrt(n_hut) / 3)

        db_ext = perfil_horario({f: banda_a_db(t[f"TOTAL_{f}"]) for f in "DEN"},
                                {f: banda_a_db(t[f"TRANSIT_{f}"]) for f in "DEN"}, banda_a_db(t["OCI_N"]))
        notas_ext = notas_horarias(db_ext, extra)
        franjas, global_ = resumen(notas_ext)

        patio = tramo_patio(p, geoms, tramer, arbol)
        interior = None
        if patio:
            # Interior: solo el nivel del patio de manzana; los focos de la calle no se suman.
            db_int = perfil_horario({f: banda_a_db(patio[f"TOTAL_{f}"]) for f in "DEN"})
            notas_int = notas_horarias(db_int, 0)
            fr_int, gl_int = resumen(notas_int)
            interior = {"db": [round(v, 1) for v in db_int], "nota": [round(v, 1) for v in notas_int],
                        "franjas": {f: round(v) for f, v in fr_int.items()}, "global": round(gl_int),
                        "mapa": {f: patio[f"TOTAL_{f}"] for f in "DEN"}}

        d_sensor = min(math.hypot(sx - x, sy - y) for sx, sy in sensors)
        confianza = "alta" if d_sensor <= RADIO_SENSOR_M else "media"
        if not por_calle or dist_tram > 40:
            confianza = "baja"

        filas.append({
            "direccion": d, "grupo": info["grupo"],
            "nota_global": round(global_), "nota_dia": round(franjas["D"]), "nota_tarde": round(franjas["E"]), "nota_noche": round(franjas["N"]),
            "mes_dia": t["TOTAL_D"], "mes_tarde": t["TOTAL_E"], "mes_noche": t["TOTAL_N"],
            "mes_trafico_noche": t["TRANSIT_N"], "mes_ocio_noche": t["OCI_N"], "mes_patio_noche": patio["TOTAL_N"] if patio else "",
            "nota_global_interior": interior["global"] if interior else "",
            "ocio_nocturno_100m": n_oci, "bares_rest_100m": n_bar, "quejas_ruido_100m": n_queixes, "pisos_turisticos_100m": n_hut,
            "sensor_mas_cercano_m": round(d_sensor), "distancia_tramo_m": round(dist_tram, 1), "confianza": confianza,
        })
        visor.append({
            "direccion": d, "grupo": info["grupo"], "barrio": info["barrio"], "aviso": info["aviso"], "confianza": confianza,
            "exterior": {"db": [round(v, 1) for v in db_ext], "nota": [round(v, 1) for v in notas_ext],
                         "franjas": {f: round(v) for f, v in franjas.items()}, "global": round(global_),
                         "mapa": {f: t[f"TOTAL_{f}"] for f in "DEN"}},
            "interior": interior,
            "fuentes": {"trafico_noche": t["TRANSIT_N"], "ocio_noche": t["OCI_N"]},
            "focos": {"ocio": n_oci, "bares": n_bar, "quejas": n_queixes, "turisticos": n_hut},
            "sensor_m": round(d_sensor),
        })

    with open(AQUI / "resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    escribir_tabla_md(filas)
    plantilla = AQUI / "visor_plantilla.html"
    if plantilla.exists():
        html = plantilla.read_text(encoding="utf-8").replace("/*DATOS*/[]", json.dumps(visor, ensure_ascii=False))
        (AQUI / "visor.html").write_text(html, encoding="utf-8")

    for r in sorted(filas, key=lambda r: -r["nota_global"]):
        print(f'{r["nota_global"]:>3}  D{r["nota_dia"]:>3} T{r["nota_tarde"]:>3} N{r["nota_noche"]:>3}  int {str(r["nota_global_interior"]):>3}  '
              f'{r["grupo"]:<11} {r["direccion"]:<42} {r["confianza"]}')


def escribir_tabla_md(filas):
    md = AQUI / "resultados.md"
    if not md.exists():
        return
    lineas = ["| Nota | Día | Tarde | Noche | Interior | Dirección | Hipótesis | Ruido noche (mapa) | Ocio / bares / quejas / HUT (100 m) | Confianza |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(filas, key=lambda r: -r["nota_global"]):
        noche = r["mes_noche"].replace(" dB(A)", "").replace(" - ", "–")
        interior = r["nota_global_interior"] if r["nota_global_interior"] != "" else "—"
        lineas.append(f'| {r["nota_global"]} | {r["nota_dia"]} | {r["nota_tarde"]} | {r["nota_noche"]} | {interior} | {r["direccion"]} | {r["grupo"]} | {noche} | '
                      f'{r["ocio_nocturno_100m"]} / {r["bares_rest_100m"]} / {r["quejas_ruido_100m"]} / {r["pisos_turisticos_100m"]} | {r["confianza"]} |')
    texto = md.read_text(encoding="utf-8")
    texto = re.sub(r"<!-- tabla:inicio -->.*<!-- tabla:fin -->", "<!-- tabla:inicio -->\n" + "\n".join(lineas) + "\n<!-- tabla:fin -->", texto, flags=re.S)
    md.write_text(texto, encoding="utf-8")


if __name__ == "__main__":
    main()
