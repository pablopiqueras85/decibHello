"""Lee los horarios de los espacios de música y copas (Open Data BCN) y calcula qué noches abren hasta tarde."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).parent
DIAS = {"dilluns": 0, "lunes": 0, "dimarts": 1, "martes": 1, "dimecres": 2, "miércoles": 2, "miercoles": 2,
        "dijous": 3, "jueves": 3, "divendres": 4, "viernes": 4, "dissabte": 5, "dissabtes": 5, "sábado": 5, "sabado": 5, "sábados": 5,
        "diumenge": 6, "diumenges": 6, "domingo": 6, "domingos": 6}
TIPOS_NOCHE = {"Discoteques", "Sales de festes", "Bars i pubs musicals", "Karaokes", "Tablaos flamencs", "Xampanyeries", "Cocteleries"}


def dias_de(texto):
    t = texto.lower()
    if "tots els dies" in t or "todos los días" in t or "cada dia" in t:
        return set(range(7))
    encontrados = [(m.start(), DIAS[m.group(0)]) for m in re.finditer("|".join(sorted(DIAS, key=len, reverse=True)), t)]
    dias = {d for _, d in encontrados}
    m = re.search(r"(?:de\s+)?(\w+)\s+a\s+(\w+)", t)  # "de dilluns a dijous"
    if m and m.group(1) in DIAS and m.group(2) in DIAS:
        a, b = DIAS[m.group(1)], DIAS[m.group(2)]
        dias |= {(a + i) % 7 for i in range(((b - a) % 7) + 1)}
    return dias


def noches_tarde(timetable):
    """Días (0=lunes) en que el local cierra entre las 2:00 y las 8:00 (abierto de madrugada esa noche)."""
    if not timetable:
        return None
    texto = re.sub(r"<[^>]+>", "|", timetable).replace("&nbsp;", " ")
    celdas = [c.strip() for c in texto.split("|") if c.strip()]
    tarde = set()
    for i in range(len(celdas) - 1):
        dias = dias_de(celdas[i])
        horas = re.findall(r"(\d{1,2})[.:](\d{2})", celdas[i + 1])
        if dias and horas:
            cierre = int(horas[-1][0])
            if 2 <= cierre <= 8:
                tarde |= dias
    return sorted(tarde)


RES_ESPAIS = "062da2e7-ddc9-4659-807a-2c1c5918b73c"  # Open Data BCN: culturailleure-espaismusicacopes


def locales():
    f = AQUI / "cache" / "espais_musica_copes.json"
    if not f.exists():
        import urllib.parse
        import urllib.request
        url = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/datastore_search?" + urllib.parse.urlencode({"resource_id": RES_ESPAIS, "limit": 5000})
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "DecibHello/0.1"}), timeout=120) as resp:
            f.parent.mkdir(exist_ok=True)
            f.write_text(json.dumps(json.load(resp)["result"]["records"]))
    r = json.loads(f.read_text())
    vistos = {}
    for x in r:
        vistos.setdefault(x["register_id"].strip("﻿"), x)
    out = []
    for x in vistos.values():
        if x["secondary_filters_name"] not in TIPOS_NOCHE or not x.get("geo_epgs_4326_lat"):
            continue
        out.append({"nombre": x["name"], "tipo": x["secondary_filters_name"], "lat": float(x["geo_epgs_4326_lat"]),
                    "lon": float(x["geo_epgs_4326_lon"]), "noches": noches_tarde(x.get("timetable"))})
    return out


PESO_TIPO = {"Discoteques": 3, "Sales de festes": 3, "Bars i pubs musicals": 1, "Karaokes": 1, "Cocteleries": 0.5,
             "Xampanyeries": 0.5, "Tablaos flamencs": 0}
RADIO_M = 150


def carga_por_local(ls):
    """Matriz locales x 7 noches: peso del tipo x probabilidad de abrir de madrugada esa noche.
    Sin horario publicado, se usa la proporción de locales del mismo tipo que abren cada noche."""
    import numpy as np
    prob = {}
    for t in PESO_TIPO:
        con = [l for l in ls if l["tipo"] == t and l["noches"] is not None]
        prob[t] = np.array([np.mean([d in l["noches"] for l in con]) if con else 0.0 for d in range(7)])
    filas = [[(d in l["noches"]) if l["noches"] is not None else prob[l["tipo"]][d] for d in range(7)] for l in ls]
    return np.array(filas, dtype=float) * np.array([PESO_TIPO[l["tipo"]] for l in ls])[:, None]


def carga_en_puntos(xy, ls=None):
    """Carga de ocio de madrugada (7 noches) a menos de RADIO_M de cada punto (coordenadas UTM 31N)."""
    import numpy as np
    from pyproj import Transformer
    from scipy.spatial import cKDTree
    ls = ls or locales()
    t = Transformer.from_crs("EPSG:4326", "EPSG:25831", always_xy=True)
    p = np.array([t.transform(l["lon"], l["lat"]) for l in ls])
    carga = carga_por_local(ls)
    vecinos = cKDTree(p).query_ball_point(xy, RADIO_M)
    return np.array([carga[v].sum(0) if v else np.zeros(7) for v in vecinos])


if __name__ == "__main__":
    ls = locales()
    con = [l for l in ls if l["noches"] is not None]
    print(len(ls), "locales de noche;", len(con), "con horario")
    import collections
    for t in sorted({l["tipo"] for l in con}):
        c = collections.Counter(d for l in con if l["tipo"] == t for d in l["noches"])
        n = sum(1 for l in con if l["tipo"] == t)
        print(f"{t:<22} {n:>3} con horario · abiertos de madrugada L..D:", [c[d] for d in range(7)])
    for l in con:
        if "Sutton" in l["nombre"] or "Bling" in l["nombre"]:
            print(l)
