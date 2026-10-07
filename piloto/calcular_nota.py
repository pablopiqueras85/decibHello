"""DecibHello: nota de ruido del piloto y construcción del visor.

1. Lee el índice de toda la ciudad (indice.py -> cache/indice.json).
2. Calcula la nota hora a hora (modelo.py) de las direcciones de direcciones.txt -> resultados.csv y tabla de resultados.md.
3. Incrusta el índice y la lista del piloto en visor_plantilla.html -> visor.html (buscador para cualquier portal de Barcelona).

Uso: python3 piloto/indice.py  (una vez, descarga datos)  y después  python3 piloto/calcular_nota.py
"""

import csv
import json
import math
import re
import unicodedata
from pathlib import Path

import numpy as np

import modelo

AQUI = Path(__file__).parent
INDICE = AQUI / "cache" / "indice.json"
RADIO_SENSOR_DAM = 15  # sensor a menos de 150 m: confianza alta
TOLERANCIA_NUMERO = 4  # un número que no figura en el listado, pero a 4 o menos de un portal del mismo lado, cuenta como encontrado


def normalizar(texto):
    return unicodedata.normalize("NFD", texto.lower()).encode("ascii", "ignore").decode()


def leer_direcciones():
    filas = []
    for linea in (AQUI / "direcciones.txt").read_text(encoding="utf-8").splitlines():
        if not linea.strip() or linea.startswith("#"):
            continue
        partes = [x.strip() for x in linea.split("|")] + ["", "", ""]
        filas.append({"direccion": partes[0], "grupo": partes[1], "barrio": partes[2], "aviso": partes[3]})
    return filas


def rangos(planos, n_campos):
    return [planos[i:i + n_campos] for i in range(0, len(planos), n_campos)]


def buscar(indice, calle, numero):
    """Rango del portal: mismo lado de la calle (paridad) y número dentro del rango; si no, el más próximo."""
    calles = {normalizar(n): pl for n, pl in indice["calles"]}
    rs = rangos(calles[normalizar(calle)], len(indice["campos_rango"]))
    mismos = [r for r in rs if r[0] % 2 == numero % 2] or rs
    exacto = [r for r in mismos if r[0] <= numero <= r[1]]
    if exacto:
        return exacto[0], True
    r = min(mismos, key=lambda r: min(abs(numero - r[0]), abs(numero - r[1])))
    return r, min(abs(numero - r[0]), abs(numero - r[1])) <= TOLERANCIA_NUMERO


def nucleo_calle(nombre):
    """Palabras propias del nombre de una calle (sin tipo de vía, partículas ni número): 'Carrer de Tuset' -> {'tuset'}."""
    tipos = {"carrer", "avinguda", "passeig", "placa", "plaça", "ronda", "rambla", "passatge", "travessera", "via", "gran", "cami", "camí", "baixada", "pujada", "carretera", "moll"}
    part = {"de", "del", "d", "la", "les", "el", "els", "dels", "l", "i"}
    t = re.sub(r"[^a-z0-9 ]", " ", normalizar(re.sub(r"\s+\d+\s*$", "", nombre))).split()
    return frozenset(w for w in t if w not in tipos and w not in part)


def anclar_sensores(indice, perfiles, radio=60, radio_calle=120):
    """Marca los rangos del mismo tramo que un sensor municipal, a menos de `radio` m: allí se usa lo medido.

    Se toma el rango más cercano al sensor y se anclan los rangos con su mismo tramo del mapa, para no pasar a la
    calle de al lado. Además, los rangos de la MISMA calle que el sensor a menos de `radio_calle` m (Tuset 20 con el
    sensor de Tuset 30). Añade el campo 'sensor' (índice en `perfiles`, o -1) a cada rango del índice.
    """
    campos = indice["campos_rango"]
    n = len(campos)
    ilat, ilon, itr = campos.index("lat_e5"), campos.index("lon_e5"), campos.index("tramo")
    todos = []
    for c, (_, pl) in enumerate(indice["calles"]):
        for k in range(0, len(pl), n):
            todos.append((c, k, 41.3 + pl[k + ilat] / 1e5, 2.0 + pl[k + ilon] / 1e5, pl[k + itr]))
    lat = np.array([t[2] for t in todos]); lon = np.array([t[3] for t in todos]); tr = np.array([t[4] for t in todos])
    nucleos = [nucleo_calle(nombre) for nombre, _ in indice["calles"]]
    calle_de = np.array([t[0] for t in todos])
    asignado = np.full(len(todos), -1); dist = np.full(len(todos), np.inf)
    for si, p in enumerate(perfiles):
        d = np.hypot((lon - p["lon"]) * 83300, (lat - p["lat"]) * 110540)
        j = int(d.argmin())
        if d[j] > 40:
            continue
        cerca = (tr == tr[j]) & (d <= radio) & (d < dist)
        asignado[cerca], dist[cerca] = si, d[cerca]
        propia = nucleo_calle(p["calle"])
        if propia:
            misma = np.array([nucleos[c] == propia for c in calle_de]) & (d <= radio_calle) & (d < dist)
            asignado[misma], dist[misma] = si, d[misma]
    # Reconstruir los planos con el campo nuevo al final de cada rango.
    nuevos = {}
    for (c, k, *_), si in zip(todos, asignado):
        nuevos.setdefault(c, []).append((k, int(si)))
    for c, lst in nuevos.items():
        pl = indice["calles"][c][1]
        out = []
        for k, si in sorted(lst):
            out += pl[k:k + n] + [si]
        indice["calles"][c][1] = out
    indice["campos_rango"] = campos + ["sensor"]
    return int((asignado >= 0).sum())


def ajustar_noches(indice):
    """Ajuste por noche de la semana según los locales abiertos de madrugada cerca (horarios_ocio.py).
    Añade 'noches' (índice en indice['ajustes_noche'], o -1 si no hay locales cerca)."""
    import horarios_ocio
    from pyproj import Transformer
    campos = indice["campos_rango"]
    n = len(campos)
    ilat, ilon = campos.index("lat_e5"), campos.index("lon_e5")
    t = Transformer.from_crs("EPSG:4326", "EPSG:25831", always_xy=True)
    puntos = [(c, k) for c, (_, pl) in enumerate(indice["calles"]) for k in range(0, len(pl), n)]
    x, y = t.transform([2.0 + indice["calles"][c][1][k + ilon] / 1e5 for c, k in puntos],
                       [41.3 + indice["calles"][c][1][k + ilat] / 1e5 for c, k in puntos])
    carga = horarios_ocio.carga_en_puntos(np.c_[x, y])
    tabla, idx = [], {}
    nuevos = {}
    for (c, k), cg in zip(puntos, carga):
        i = -1
        if cg.sum() > 0:
            aj = tuple(modelo.ajuste_noches(cg.tolist()))
            if aj not in idx:
                idx[aj] = len(tabla)
                tabla.append(list(aj))
            i = idx[aj]
        nuevos.setdefault(c, []).append((k, i))
    for c, lst in nuevos.items():
        pl = indice["calles"][c][1]
        out = []
        for k, i in lst:
            out += pl[k:k + n] + [i]
        indice["calles"][c][1] = out
    indice["campos_rango"] = campos + ["noches"]
    indice["ajustes_noche"] = tabla
    return sum(1 for _, lst in nuevos.items() for _, i in lst if i >= 0)


def asignar_obras(indice, hoy=None):
    """Obras públicas no terminadas a menos de 100 m de cada rango (obras.py). Añade 'obras' (índice en
    indice['grupos_obras'], lista de [obra, distancia en m], o -1) e indice['obras'] con los datos de cada obra."""
    import datetime as dt
    import obras as mod_obras
    from pyproj import Transformer
    hoy = hoy or dt.date.today()
    vig = mod_obras.vigentes(mod_obras.cargar(hoy), hoy)
    campos = indice["campos_rango"]
    n = len(campos)
    ilat, ilon = campos.index("lat_e5"), campos.index("lon_e5")
    t = Transformer.from_crs("EPSG:4326", "EPSG:25831", always_xy=True)
    puntos = [(c, k) for c, (_, pl) in enumerate(indice["calles"]) for k in range(0, len(pl), n)]
    x, y = t.transform([2.0 + indice["calles"][c][1][k + ilon] / 1e5 for c, k in puntos],
                       [41.3 + indice["calles"][c][1][k + ilat] / 1e5 for c, k in puntos])
    cerca = mod_obras.cerca_de(vig, np.c_[x, y])
    usadas, grupos, idx, nuevos = {}, [], {}, {}
    for (c, k), lst in zip(puntos, cerca):
        i = -1
        if lst:
            g = tuple((usadas.setdefault(o, len(usadas)), d) for o, d in lst)
            i = idx.setdefault(g, len(grupos))
            if i == len(grupos):
                grupos.append([list(p) for p in g])
        nuevos.setdefault(c, []).append((k, i))
    for c, lst in nuevos.items():
        pl = indice["calles"][c][1]
        out = []
        for k, i in lst:
            out += pl[k:k + n] + [i]
        indice["calles"][c][1] = out
    indice["campos_rango"] = campos + ["obras"]
    indice["grupos_obras"] = grupos
    indice["obras"] = [None] * len(usadas)
    a_wgs = Transformer.from_crs("EPSG:25831", "EPSG:4326", always_xy=True)
    for o, j in usadas.items():
        rec, geom, ini, fin = vig[o]
        lon_o, lat_o = a_wgs.transform(geom.centroid.x, geom.centroid.y)
        indice["obras"][j] = {"suma": geom.area <= mod_obras.AREA_MAX_EFECTO, "titulo": rec["titol"], "tipo": rec["tipusobra"], "inicio": ini.isoformat(), "fin": fin.isoformat(),
                              "estado": rec["estat"], "lugar": (rec.get("ubicacio") or "").strip(), "url": rec.get("url_web_obres") or "",
                              "lat": round(lat_o, 5), "lon": round(lon_o, 5)}
    indice["obras_fecha"] = hoy.isoformat()
    indice["obras_radio_efecto"] = mod_obras.RADIO_EFECTO
    return len(usadas), sum(1 for lst in nuevos.values() for _, i in lst if i >= 0)


def asignar_plantas(indice, radio=10):
    """Plantas del edificio de cada portal: la parte de edificio más alta del Catastro a menos de `radio` m del punto
    del rango (piloto/datos/edificios_catastro.json.gz, ver alturas.py). Añade 'plantas' (-1 si no se sabe)."""
    import gzip
    from pyproj import Transformer
    from scipy.spatial import cKDTree
    f = AQUI / "datos" / "edificios_catastro.json.gz"
    campos = indice["campos_rango"]
    n = len(campos)
    puntos = [(c, k) for c, (_, pl) in enumerate(indice["calles"]) for k in range(0, len(pl), n)]
    plantas = np.full(len(puntos), -1)
    if f.exists():
        ed = np.array(json.loads(gzip.open(f, "rt", encoding="utf-8").read()), dtype=float)
        ilat, ilon = campos.index("lat_e5"), campos.index("lon_e5")
        t = Transformer.from_crs("EPSG:4326", "EPSG:25831", always_xy=True)
        x, y = t.transform([2.0 + indice["calles"][c][1][k + ilon] / 1e5 for c, k in puntos],
                           [41.3 + indice["calles"][c][1][k + ilat] / 1e5 for c, k in puntos])
        arbol = cKDTree(ed[:, :2])
        rmax = ed[:, 2].max()
        for i, cerca in enumerate(arbol.query_ball_point(np.c_[x, y], radio + rmax)):
            if not cerca:
                continue
            d = np.hypot(ed[cerca, 0] - x[i], ed[cerca, 1] - y[i]) - ed[cerca, 2]
            ok = np.array(cerca)[d <= radio]
            if len(ok):
                plantas[i] = int(ed[ok, 3].max())
    nuevos = {}
    for (c, k), p in zip(puntos, plantas):
        nuevos.setdefault(c, []).append((k, int(p)))
    for c, lst in nuevos.items():
        pl = indice["calles"][c][1]
        out = []
        for k, p in lst:
            out += pl[k:k + n] + [p]
        indice["calles"][c][1] = out
    indice["campos_rango"] = campos + ["plantas"]
    return int((plantas >= 0).sum()), len(plantas)


def capas_mapa(origen):
    """Puntos para el mapa de la zona (lat y lon en cienmilésimas desde el origen del índice): bares, bares musicales y
    discotecas (censo de locales) y quejas por ruido en la calle (IRIS 2025). Salen de la caché de indice.py."""
    def puntos(nombre, lat, lon):
        f = CACHE_DIR / f"{nombre}.json"
        if not f.exists():
            return []
        out = []
        for r in json.loads(f.read_text()):
            try:
                out += [round((float(r[lat]) - origen["lat"]) * 1e5), round((float(r[lon]) - origen["lon"]) * 1e5)]
            except (TypeError, ValueError, KeyError):
                pass
        return out
    return {"bares": puntos("cens_solo_bares", "Latitud", "Longitud"), "musicales": puntos("cens_musicales", "Latitud", "Longitud"),
            "quejas": puntos("iris2025_soroll", "LATITUD", "LONGITUD")}


def margen_medido(perfiles):
    """Margen de error (dB) donde manda un sensor: diferencia entre dos sensores de la misma calle a menos de 120 m
    (la que no se supera en 2 de cada 3 pares)."""
    dif = {f: [] for f in "DEN"}
    def leq(s, f):
        return 10 * math.log10(np.mean([10 ** (s["db"][d][h] / 10) for d in range(7) for h in modelo.HORAS[f]]))
    for i, a in enumerate(perfiles):
        for b in perfiles[i + 1:]:
            if math.hypot((a["lon"] - b["lon"]) * 83300, (a["lat"] - b["lat"]) * 110540) <= 120 and nucleo_calle(a["calle"]) \
                    and nucleo_calle(a["calle"]) == nucleo_calle(b["calle"]):
                for f in "DEN":
                    dif[f].append(abs(leq(a, f) - leq(b, f)))
    return {f: round(float(np.percentile(dif[f], 68)), 1) if dif[f] else 2.5 for f in "DEN"}


def obra_activa(indice, grupo, hoy=None):
    """True si una obra en curso (no parada, no un gran proyecto) está a menos de obras.RADIO_EFECTO m en la fecha `hoy`."""
    import datetime as dt
    import obras as mod_obras
    if grupo < 0:
        return False
    hoy = (hoy or dt.date.today()).isoformat()
    return any(d <= mod_obras.RADIO_EFECTO and indice["obras"][o]["suma"] and indice["obras"][o]["estado"] != "Aturada"
               and indice["obras"][o]["inicio"] <= hoy <= indice["obras"][o]["fin"] for o, d in indice["grupos_obras"][grupo])


CACHE_DIR = AQUI / "cache"


def redondear(x):
    """Redondeo como el visor (Math.round): las mitades hacia arriba."""
    return math.floor(x + 0.5)


def mapa_tramo(indice, i):
    t = indice["tramos"][i]
    return {campo: indice["bandas"][int(t[k])] for k, campo in enumerate(indice["campos_tramo"])}


def main():
    indice = json.loads(INDICE.read_text(encoding="utf-8"))
    f_sens = AQUI / "perfiles_por_sensor.json"
    perfiles = json.loads(f_sens.read_text(encoding="utf-8")) if f_sens.exists() else []
    print(f"rangos con medición de sensor: {anclar_sensores(indice, perfiles)}")
    print(f"rangos con ajuste por horarios de locales: {ajustar_noches(indice)}")
    print("obras vigentes cerca de algún portal: {} · rangos con obras a menos de 100 m: {}".format(*asignar_obras(indice)))
    print("rangos con altura del edificio (Catastro): {} de {}".format(*asignar_plantas(indice)))
    print("rangos en esquina (portal de otra calle a menos de 20 m): {} de {}".format(
        sum(1 for _, pl in indice["calles"] for k in range(indice["campos_rango"].index("esq_calle"), len(pl), len(indice["campos_rango"])) if pl[k] >= 0),
        sum(len(pl) // len(indice["campos_rango"]) for _, pl in indice["calles"])))
    campos = indice["campos_rango"]
    margen_sensor = margen_medido(perfiles)
    filas = []
    for info in leer_direcciones():
        calle, numero = info["direccion"].rsplit(" ", 1)
        r, exacto = buscar(indice, calle, int(numero))
        v = dict(zip(campos, r))
        mapa = mapa_tramo(indice, v["tramo"])
        medido = perfiles[v["sensor"]]["db"] if v["sensor"] >= 0 else None
        locales = (v["solo_bares"], v["musicales"]) if medido is None else None
        aj = indice["ajustes_noche"][v["noches"]] if v["noches"] >= 0 and medido is None else None
        obra = obra_activa(indice, v["obras"])
        res = modelo.calcular(mapa, {"ocio": v["ocio"], "bares": v["bares"], "quejas": v["quejas"], "turisticos": v["turisticos"]},
                              medido=medido, locales=locales, ajuste_noche=aj, obra=obra)
        interior = None
        if v["patio"] >= 0:
            mp = mapa_tramo(indice, v["patio"])
            interior = modelo.calcular({f"TOTAL_{f}": mp[f"TOTAL_{f}"] for f in "DEN"})
        focos = {"ocio": v["ocio"], "bares": v["bares"], "quejas": v["quejas"], "turisticos": v["turisticos"]}
        noches = {modelo.DIAS[d]: redondear(modelo.calcular(mapa, focos, d, medido, locales, aj, obra)["franjas"]["N"]) for d in range(7)}
        confianza = "alta" if v["sensor_dam"] <= RADIO_SENSOR_DAM else "media"
        if not exacto:
            confianza = "baja"
        elif medido is not None:
            confianza = "medida"
        filas.append({
            "direccion": info["direccion"], "grupo": info["grupo"],
            "nota_global": redondear(res["global"]), "nota_dia": redondear(res["franjas"]["D"]),
            "nota_tarde": redondear(res["franjas"]["E"]), "nota_noche": redondear(res["franjas"]["N"]),
            "nota_global_interior": redondear(interior["global"]) if interior else "",
            "mes_dia": mapa["TOTAL_D"], "mes_tarde": mapa["TOTAL_E"], "mes_noche": mapa["TOTAL_N"],
            "mes_trafico_noche": mapa["TRANSIT_N"], "mes_ocio_noche": mapa["OCI_N"],
            "ocio_nocturno_100m": v["ocio"], "bares_rest_100m": v["bares"], "quejas_ruido_100m": v["quejas"],
            "pisos_turisticos_100m": v["turisticos"], "sensor_mas_cercano_m": v["sensor_dam"] * 10,
            "rango_portales": f'{v["ini"]}-{v["fin"]}', "confianza": confianza,
            "sensor": perfiles[v["sensor"]]["calle"] if medido is not None else "",
            "solo_bares_100m": v["solo_bares"], "musicales_100m": v["musicales"],
            "ancho_m": v["ancho_m"], "quejas_recogida_100m": v["quejas_recogida"],
            "picos_nocturnos": modelo.aviso_picos(v["ancho_m"], v["quejas_recogida"], v["turisticos"]),
            "nota_min": redondear(modelo.entre(res["global"], modelo.margen_puntos(margen_sensor if medido is not None else modelo.INCERTIDUMBRE))[0]),
            "nota_max": redondear(modelo.entre(res["global"], modelo.margen_puntos(margen_sensor if medido is not None else modelo.INCERTIDUMBRE))[1]),
            "obra_activa_25m": "sí" if obra else "",
            "obras_100m": len(indice["grupos_obras"][v["obras"]]) if v["obras"] >= 0 else 0,
            **{f"noche_{d}": n for d, n in noches.items()},
        })

    with open(AQUI / "resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    escribir_tabla_md(filas)
    construir_visor(indice, perfiles)
    # Casos de la corrección por planta para la prueba de paridad con JavaScript (pruebas/paridad.mjs).
    casos = [[p, pe, an] for p in [None, 0, 1, 2, 3, 5, 8, 12, "atico"] for pe in [-1, 2, 5, 8, 12] for an in [-1, 6, 12, 25, 60]]
    margenes = [modelo.INCERTIDUMBRE, {"D": 2.7, "E": 2.3, "N": 2.0}, {"D": 0, "E": 10, "N": 1.5}]
    casos_margen = [[m, f] for m in margenes for f in [None, "D", "E", "N"]]
    (AQUI / "pruebas" / "planta_python.json").write_text(json.dumps({"casos": casos, "db": [modelo.correccion_planta(*c) for c in casos],
        "casos_margen": casos_margen, "margen": [modelo.margen_puntos(m, f) for m, f in casos_margen],
        "esquina": [[50, 60, 70], [55, 58, 75], modelo.combinar_esquina([50, 60, 70], [55, 58, 75])]}))

    for r in sorted(filas, key=lambda r: -r["nota_global"]):
        print(f'{r["nota_global"]:>3}  D{r["nota_dia"]:>3} T{r["nota_tarde"]:>3} N{r["nota_noche"]:>3}  int {str(r["nota_global_interior"]):>3}  '
              f'{r["grupo"]:<11} {r["direccion"]:<46} {r["confianza"]}')


def distribucion_ciudad(indice, perfiles):
    """Percentiles 0-100 de la nota global exterior (media de todos los días) de todos los portales de la ciudad.
    Cada rango pesa por su número de portales. Sirve para "más ruidosa que el X % de los portales de Barcelona"."""
    campos, n = indice["campos_rango"], len(indice["campos_rango"])
    notas, pesos, barrios, cache = [], [], [], {}
    for _, planos in indice["calles"]:
        for r in rangos(planos, n):
            v = dict(zip(campos, r))
            medido = perfiles[v["sensor"]]["db"] if v["sensor"] >= 0 else None
            locales = (v["solo_bares"], v["musicales"]) if medido is None else None
            clave = (v["tramo"], v["sensor"], locales)
            if clave not in cache:
                cache[clave] = modelo.calcular(mapa_tramo(indice, v["tramo"]), medido=medido, locales=locales)["global"]
            notas.append(cache[clave])
            pesos.append(max(1, (v["fin"] - v["ini"]) // 2 + 1))
            barrios.append(v["barrio"])
    orden = sorted(range(len(notas)), key=notas.__getitem__)
    total, acum, k, cortes = sum(pesos), 0, 0, []
    for p in range(101):
        while k < len(orden) - 1 and acum + pesos[orden[k]] < p / 100 * total:
            acum += pesos[orden[k]]
            k += 1
        cortes.append(round(notas[orden[k]], 2))
    # Media de cada barrio (ponderada por portales), para comparar la calle con su barrio.
    suma, peso = {}, {}
    for nota, w, b in zip(notas, pesos, barrios):
        suma[b] = suma.get(b, 0) + nota * w
        peso[b] = peso.get(b, 0) + w
    medias = {str(b): round(suma[b] / peso[b], 1) for b in suma}
    return cortes, medias, round(sum(n * w for n, w in zip(notas, pesos)) / sum(pesos), 1)


def construir_visor(indice, perfiles):
    piloto = [{"direccion": d["direccion"], "grupo": d["grupo"], "aviso": d["aviso"]} for d in leer_direcciones()]
    sensores = [{"calle": p["calle"], "tipo": p["tipo"], "dias": p["dias"], "db": p["db"], "lat": p["lat"], "lon": p["lon"]} for p in perfiles]
    cortes, medias_barrio, media_ciudad = distribucion_ciudad(indice, perfiles)
    datos = json.dumps({"indice": indice, "piloto": piloto, "perfiles": modelo.PERFILES, "sensores": sensores,
                        "coef_locales": modelo.COEF_LOCALES, "percentiles_ciudad": cortes,
                        "medias_barrio": medias_barrio, "media_ciudad": media_ciudad,
                        "incertidumbre": {"estimado_db": modelo.INCERTIDUMBRE, "medido_db": margen_medido(perfiles)},
                        "capas": capas_mapa(indice["origen"])},
                       ensure_ascii=False, separators=(",", ":"))
    motor = (AQUI / "motor.js").read_text(encoding="utf-8")
    html = (AQUI / "visor_plantilla.html").read_text(encoding="utf-8").replace("/*DATOS*/null", datos).replace("/*MOTOR*/", motor)
    (AQUI / "visor.html").write_text(html, encoding="utf-8")
    # Paquete para otras páginas (la web): el mismo motor y los mismos datos, en un solo fichero.
    # Uso: <script src="decibhello.js"></script> y después window.DecibHello.buscar("Tuset 20").
    (AQUI / "paquete").mkdir(exist_ok=True)
    (AQUI / "paquete" / "decibhello.js").write_text(
        "// Generado por piloto/calcular_nota.py a partir de piloto/motor.js. No lo edites a mano.\n"
        "(function () {\n\"use strict\";\nconst DATOS = " + datos + ";\n" + motor + "\nwindow.DecibHello = DecibHello;\n})();\n",
        encoding="utf-8")


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
    cab = "| Dirección | " + " | ".join(d[:3].capitalize() for d in modelo.DIAS) + " | Vie − lun |"
    semana = [cab, "|---|" + "---|" * 8]
    for r in sorted(filas, key=lambda r: -(r["noche_viernes"] - r["noche_lunes"])):
        semana.append(f'| {r["direccion"]} | ' + " | ".join(str(r[f"noche_{d}"]) for d in modelo.DIAS) + f' | {r["noche_viernes"] - r["noche_lunes"]:+d} |')
    picos = ["| Dirección | Anchura | Quejas recogida y limpieza (100 m, 2023-26) | Picos nocturnos |", "|---|---|---|---|"]
    orden = {"alto": 0, "medio": 1, "bajo": 2}
    for r in sorted(filas, key=lambda r: (orden[r["picos_nocturnos"]], r["ancho_m"])):
        ancho = f'{r["ancho_m"]} m' if r["ancho_m"] >= 0 else "—"
        picos.append(f'| {r["direccion"]} | {ancho} | {r["quejas_recogida_100m"]} | {r["picos_nocturnos"]} |')
    texto = re.sub(r"<!-- picos:inicio -->.*<!-- picos:fin -->", "<!-- picos:inicio -->\n" + "\n".join(picos) + "\n<!-- picos:fin -->", texto, flags=re.S)
    texto = re.sub(r"<!-- semana:inicio -->.*<!-- semana:fin -->", "<!-- semana:inicio -->\n" + "\n".join(semana) + "\n<!-- semana:fin -->", texto, flags=re.S)
    md.write_text(texto, encoding="utf-8")


if __name__ == "__main__":
    main()
