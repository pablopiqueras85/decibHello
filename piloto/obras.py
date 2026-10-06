"""Obras públicas en la calle: ruido extra temporal (Open Data BCN, "Obres a l'espai públic").

1. cargar(): todas las obras del recurso (con fechas, tipo, estado y polígono), en caché por día.
2. validar(): mide con los sensores municipales de 2023 cuánto ruido añade una obra cercana. Compara, en cada
   sensor, los días laborables con obra activa cerca frente a los días sin obra, de día (8-18 h) y de noche
   (0-5 h, cuando no se trabaja, como control) -> obras_validacion.md.
3. cerca_de(puntos): obras activas o previstas a menos de RADIO_AVISO m de cada punto, con su distancia.

Resultado de la validación: a menos de 25 m, +2 dB de mediana de día laborable durante toda la obra (hasta +8 dB
en una reurbanización); a 25-75 m, +0,4 dB; más lejos, nada. Por eso el modelo solo suma a menos de 25 m.
"""
import datetime as dt
import json
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).parent
CACHE = AQUI / "cache"
sys.path.insert(0, str(AQUI))
from indice import API, get_json  # noqa: E402

RES_OBRAS = "4e6b3bfe-2f47-4d35-aa7d-3e4bcc930cea"
RADIO_EFECTO = 25   # m: solo aquí se suma ruido (validado)
RADIO_AVISO = 100   # m: se muestran en el informe
# Proyectos muy grandes (túneles, estaciones, el estadio): el ruido se concentra en pocos puntos de un área enorme,
# así que se muestran pero no suman (p95 del área de las obras vigentes ≈ 1,7 ha).
AREA_MAX_EFECTO = 20000  # m²


def cargar(hoy=None):
    hoy = hoy or dt.date.today()
    f = CACHE / f"obras_{hoy:%Y%m%d}.json"
    if f.exists():
        return json.loads(f.read_text())
    recs = get_json(API + f"datastore_search?resource_id={RES_OBRAS}&limit=10000")["result"]["records"]
    CACHE.mkdir(exist_ok=True)
    for viejo in CACHE.glob("obras_*.json"):
        viejo.unlink()
    f.write_text(json.dumps(recs))
    return recs


def _geom(recs):
    from shapely import wkt
    out = []
    for o in recs:
        if not (o.get("data_inici") and o.get("data_fi") and o.get("geometria_etrs89")):
            continue
        try:
            g = wkt.loads(o["geometria_etrs89"]).buffer(0)
        except Exception:
            continue
        out.append((o, g, dt.date.fromisoformat(o["data_inici"][:10]), dt.date.fromisoformat(o["data_fi"][:10])))
    return out


def vigentes(recs, hoy=None):
    """Obras no terminadas (en curso, paradas o previstas) a fecha `hoy`."""
    hoy = hoy or dt.date.today()
    return [x for x in _geom(recs) if x[3] >= hoy and x[0]["estat"] != "Finalitzada"]


def cerca_de(obras, xy):
    """Para cada punto (UTM ETRS89), lista de (índice de obra, distancia en m) a menos de RADIO_AVISO."""
    from shapely import STRtree, points
    arbol = STRtree([g for _, g, *_ in obras])
    pts = points(xy)
    res = [[] for _ in range(len(xy))]
    ip, io = arbol.query(pts, predicate="dwithin", distance=RADIO_AVISO)
    for p, o in zip(ip, io):
        res[p].append((int(o), round(float(obras[o][1].distance(pts[p])))))
    return [sorted(r, key=lambda t: t[1]) for r in res]


def validar():
    import pandas as pd
    from pyproj import Transformer
    from shapely.geometry import Point
    import sensores
    df, _ = sensores.cargar()
    df = df[df.logico.dt.year == 2023].copy()
    obras = [x for x in _geom(cargar()) if x[2] <= dt.date(2023, 12, 31) and x[3] >= dt.date(2023, 1, 1)]
    dia = df[df.h.between(8, 17)].groupby(["Id_Instal", "logico"]).e.mean()
    noche = df[df.h.between(0, 4)].groupby(["Id_Instal", "logico"]).e.mean()
    dd = pd.concat([10 * np.log10(dia).rename("D"), 10 * np.log10(noche).rename("N")], axis=1).dropna().reset_index()
    dd = dd[dd.logico.dt.weekday < 5]
    t = Transformer.from_crs(4326, 25831, always_xy=True)
    filas = []
    for _, s in df.drop_duplicates("Id_Instal").iterrows():
        p = Point(*t.transform(float(s.Longitud), float(s.Latitud)))
        dist = [(o, g.distance(p), i, f) for o, g, i, f in obras]
        d_s = dd[dd.Id_Instal == s.Id_Instal]
        fechas = d_s.logico.dt.date.values
        for lo, hi in [(0, 25), (25, 75), (75, 150), (300, 600)]:
            act, tipos = np.zeros(len(d_s), bool), set()
            for o, d, i, f in dist:
                if lo <= d < hi:
                    m = (fechas >= i) & (fechas <= f)
                    if m.any():
                        tipos.add(o["tipusobra"])
                    act |= m
            if act.sum() >= 10 and (~act).sum() >= 10:
                a, b = d_s[act], d_s[~act]
                filas.append({"sensor": s.Nom_Carrer, "banda": f"{lo}–{hi} m", "dias": int(act.sum()),
                              "dD": a.D.mean() - b.D.mean(), "dN": a.N.mean() - b.N.mean(), "tipos": ", ".join(sorted(tipos))})
    r = pd.DataFrame(filas)
    r["efecto"] = r.dD - r.dN
    out = ["# DecibHello — Ruido de las obras públicas (validación con sensores)", "",
           f"Obras de Open Data BCN activas en algún momento de 2023: {len(obras)}. Sensores municipales con datos por hora de 2023.",
           "Para cada sensor: días laborables con una obra activa a esa distancia frente a días laborables sin ella. "
           "Efecto = diferencia de día (8–18 h) menos diferencia de noche (0–5 h, sin obras), para quitar cambios de temporada.", "",
           "| Distancia de la obra | Sensores | Día | Noche | Efecto (mediana) | Efecto (media) |", "|---|---|---|---|---|---|"]
    for banda, x in r.groupby("banda", sort=False):
        out.append(f"| {banda} | {len(x)} | {x.dD.median():+.1f} dB | {x.dN.median():+.1f} dB | {x.efecto.median():+.1f} dB | {x.efecto.mean():+.1f} dB |")
    out += ["", "Sensores con obra a menos de 25 m:", "", "| Sensor | Días con obra | Tipo | Efecto |", "|---|---|---|---|"]
    for _, x in r[r.banda == "0–25 m"].sort_values("efecto", ascending=False).iterrows():
        out.append(f"| {x.sensor} | {x.dias} | {x.tipos} | {x.efecto:+.1f} dB |")
    out += ["", "Conclusión: el efecto se concentra a menos de 25 m (mediana ≈ +2 dB de día laborable de media durante toda la obra, "
            "con fases mucho más fuertes: hasta +8 dB de media en una reurbanización). A partir de 25 m es casi nulo, "
            "y a 300–600 m (control) no hay efecto. El modelo suma +2 dB de 8 a 18 h, de lunes a viernes, mientras la obra está "
            "activa y a menos de 25 m del portal. Las obras a menos de 100 m se muestran en el informe.", ""]
    (AQUI / "obras_validacion.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    validar()
