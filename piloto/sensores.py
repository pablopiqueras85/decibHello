"""DecibHello: perfiles reales de ruido a partir de la red municipal de sensores (datos por hora).

Entrada: piloto/sensores/*_XarxaSoroll_EqMonitor_Dades_1Hora.csv (Open Data BCN, dataset
xarxasoroll-equipsmonitor-dades; se descargan a mano porque el portal pide verificación anti-robots).

Salidas:
- piloto/perfiles_sensores.json: forma horaria y pesos por día de la semana (tráfico y ocio), que usa modelo.py.
- piloto/perfiles_por_sensor.json: nivel medido por día de la semana y hora en cada sensor (el visor lo usa cerca de los sensores).
- piloto/validacion_sensores.md: comparación entre lo medido por cada sensor y el mapa oficial de ruido 2017.

Detalle importante de los datos: de 7:00 a 23:59 la fecha registrada es la del día SIGUIENTE (de 0:00 a 6:59 es
correcta). Comprobado con Sant Joan (la verbena del 23 de junio aparece como día 24), Navidad y Semana Santa.

Uso: python3 piloto/sensores.py
"""

import glob
import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer
from shapely import wkt
from shapely.geometry import Point
from shapely.strtree import STRtree

AQUI = Path(__file__).parent
CACHE = AQUI / "cache"
API = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/"
RES_SENSORS = "f4562942-1fd8-48fb-9e9d-d41088f97a03"
FESTIVOS_2023 = ["2023-01-01", "2023-01-06", "2023-04-07", "2023-04-10", "2023-05-01", "2023-06-05", "2023-06-24", "2023-08-15",
                 "2023-09-11", "2023-09-25", "2023-10-12", "2023-11-01", "2023-12-06", "2023-12-08", "2023-12-25", "2023-12-26"]
FRANJA = np.array(["N"] * 7 + ["D"] * 12 + ["E"] * 4 + ["N"])
DIAS_MINIMOS = 150


def instalaciones():
    f = CACHE / "sensors_todos.json"
    if not f.exists():
        url = API + f"datastore_search?resource_id={RES_SENSORS}&limit=5000"
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "DecibHello/0.1"}), timeout=120) as r:
            CACHE.mkdir(exist_ok=True)
            f.write_text(json.dumps(json.load(r)["result"]["records"]))
    ins = pd.DataFrame(json.loads(f.read_text()))
    ins["Id_Instal"] = ins.Id_Instal.astype(float).astype(int)
    return ins[["Id_Instal", "Font", "Nom_Carrer", "Num_Carrer", "Nom_Barri", "Latitud", "Longitud"]].drop_duplicates("Id_Instal")


def cargar():
    ficheros = sorted(glob.glob(str(AQUI / "sensores" / "*_1Hora.csv")))
    if not ficheros:
        raise SystemExit("Faltan los CSV en piloto/sensores/")
    df = pd.concat([pd.read_csv(f) for f in ficheros])
    df = df[(df.Nivell_LAeq_1h >= 25) & (df.Nivell_LAeq_1h <= 110)].copy()
    df["h"] = df.Hora.astype(str).str.split(":").str[0].astype(int)
    registrada = pd.to_datetime(dict(year=df.Any, month=df.Mes, day=df.Dia))
    real = registrada - pd.to_timedelta((df.h >= 7).astype(int), unit="D")  # corrección de fecha (ver arriba)
    momento = real + pd.to_timedelta(df.h, unit="h")
    df["logico"] = (momento - pd.Timedelta(hours=7)).dt.normalize()  # día de 7:00 a 7:00, como el visor
    df["dia"] = df.logico.dt.weekday
    df["f"] = FRANJA[df.h]
    df["e"] = 10 ** (df.Nivell_LAeq_1h / 10)
    df = df.merge(instalaciones(), on="Id_Instal", how="left")
    n = df.groupby("Id_Instal").size()
    return df[df.Id_Instal.isin(n[n >= 24 * DIAS_MINIMOS].index)], ficheros


def perfiles(df):
    fest = pd.to_datetime(FESTIVOS_2023)
    lab = df[~df.logico.isin(fest) & ~(df.logico + pd.Timedelta(days=1)).isin(fest)]  # sin festivos ni vísperas
    base = lab.groupby(["Id_Instal", "f"]).e.mean().rename("eb")
    g = lab.groupby(["Id_Instal", "Font", "dia", "h", "f"]).e.mean().reset_index().join(base, on=["Id_Instal", "f"])
    g["r"] = g.e / g.eb
    out = {}
    for clave, font in (("trafico", "TRÀNSIT"), ("ocio", "OCI")):
        x = g[g.Font == font]
        forma = lab[lab.Font == font].groupby(["Id_Instal", "h"]).e.mean()
        forma = 10 * np.log10(forma.div(forma.groupby("Id_Instal").transform("max"))).groupby("h").median()
        pesos = x.groupby(["Id_Instal", "f", "dia"]).r.mean().groupby(["f", "dia"]).median().unstack()
        pesos = pesos.div(pesos.mean(axis=1), axis=0)
        # Pesos por día y hora: cada hora del día d respecto a la media de los 7 días a esa misma hora.
        e = lab[lab.Font == font].groupby(["Id_Instal", "dia", "h"]).e.mean()
        rel = e / e.groupby(["Id_Instal", "h"]).transform("mean")
        dh = rel.groupby(["dia", "h"]).median().unstack()
        dh = dh / dh.mean(axis=0)
        out[clave] = {"sensores": int(x.Id_Instal.nunique()), "forma_horaria_db": [round(v, 1) for v in forma.tolist()],
                      "pesos_dia": {f: [round(v, 3) for v in pesos.loc[f].tolist()] for f in "DEN"},
                      "pesos_dia_hora": [[round(float(v), 3) for v in dh.loc[d].tolist()] for d in range(7)]}
    return out


def por_sensor(df):
    """Perfil medido de cada sensor: nivel (dB) por día de la semana (7:00 a 7:00) y hora del reloj, sin festivos."""
    fest = pd.to_datetime(FESTIVOS_2023)
    lab = df[~df.logico.isin(fest) & ~(df.logico + pd.Timedelta(days=1)).isin(fest)]
    out = []
    for sid, x in lab.groupby("Id_Instal"):
        tabla = 10 * np.log10(x.groupby(["dia", "h"]).e.mean().unstack())
        if tabla.shape != (7, 24) or tabla.isna().any().any():
            continue
        s = x.iloc[0]
        out.append({"id": int(sid), "tipo": s.Font, "calle": f"{s.Nom_Carrer} {s.Num_Carrer}", "barrio": s.Nom_Barri,
                    "lat": float(s.Latitud), "lon": float(s.Longitud), "dias": int(x.logico.nunique()),
                    "db": [[round(float(v), 1) for v in tabla.loc[d].tolist()] for d in range(7)]})
    return out


def validar(df):
    """Compara el nivel medido (media anual por franja) con la banda del mapa oficial 2017 en el tramo más cercano."""
    tramer = json.loads((CACHE / "tramer2017_v2.json").read_text())
    geoms = [wkt.loads(t["GEOM_WKT"]) for t in tramer]
    calle = [i for i, t in enumerate(tramer) if not t["TRAM"].startswith("P")]
    arbol = STRtree([geoms[i] for i in calle])
    a_utm = Transformer.from_crs("EPSG:4326", "EPSG:25831", always_xy=True)
    medido = df.groupby(["Id_Instal", "f"]).e.mean().unstack()
    medido = 10 * np.log10(medido)
    info = df.drop_duplicates("Id_Instal").set_index("Id_Instal")
    filas = []
    for sid, fila in medido.iterrows():
        s = info.loc[sid]
        try:
            p = Point(*a_utm.transform(float(s.Longitud), float(s.Latitud)))
        except (TypeError, ValueError):
            continue
        j = calle[int(arbol.nearest(p))]
        if geoms[j].distance(p) > 30:
            continue
        banda = lambda b: float(b.replace("dB(A)", "").strip()[1:]) - 2.5 if "<" in b else sum(map(float, b.replace("dB(A)", "").split("-"))) / 2
        filas.append({"sensor": sid, "tipo": s.Font, "calle": f"{s.Nom_Carrer} {s.Num_Carrer}", "barrio": s.Nom_Barri,
                      **{f"med_{f}": round(fila[f], 1) for f in "DEN"},
                      **{f"mapa_{f}": banda(tramer[j][f"TOTAL_{f}"]) for f in "DEN"}})
    return pd.DataFrame(filas)


def main():
    df, ficheros = cargar()
    p = perfiles(df)
    p["origen"] = {"ficheros": [Path(f).name for f in ficheros], "nota": "Sin festivos ni vísperas. Fecha corregida (7:00-23:59 = día siguiente)."}
    (AQUI / "perfiles_sensores.json").write_text(json.dumps(p, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in p.items() if k != "origen"}, ensure_ascii=False)[:1500])

    ps = por_sensor(df)
    (AQUI / "perfiles_por_sensor.json").write_text(json.dumps(ps, ensure_ascii=False, separators=(",", ":")))
    print(f"perfiles por sensor: {len(ps)}")

    v = validar(df)
    for f in "DEN":
        v[f"dif_{f}"] = v[f"med_{f}"] - v[f"mapa_{f}"]
    nombres = {"D": "Día (7-19 h)", "E": "Tarde (19-23 h)", "N": "Noche (23-7 h)"}
    lineas = ["# DecibHello — Sensores frente al mapa oficial", "",
              f"Sensores municipales con al menos {DIAS_MINIMOS} días de datos en 2023 y a menos de 30 m de un tramo del mapa de ruido 2017: **{len(v)}**.",
              "Diferencia = nivel medido en 2023 (media energética anual) − punto medio de la banda del mapa 2017 en el tramo más cercano.", "",
              "| Franja | Diferencia media | Mediana | Error típico (abs.) | Dentro de ±5 dB |", "|---|---|---|---|---|"]
    for f in "DEN":
        d = v[f"dif_{f}"].dropna()
        lineas.append(f"| {nombres[f]} | {d.mean():+.1f} dB | {d.median():+.1f} dB | {d.abs().median():.1f} dB | {(d.abs() <= 5).mean():.0%} |")
    lineas += ["", "Por tipo de sensor (noche):", "", "| Tipo | Sensores | Diferencia mediana noche |", "|---|---|---|"]
    for tipo, x in v.groupby("tipo"):
        lineas.append(f"| {tipo} | {len(x)} | {x.dif_N.median():+.1f} dB |")
    lineas += ["", "Detalle por sensor (noche), ordenado por diferencia:", "", "| Sensor | Tipo | Ubicación | Barrio | Medido noche | Mapa noche | Diferencia |", "|---|---|---|---|---|---|---|"]
    for _, r in v.sort_values("dif_N").iterrows():
        lineas.append(f"| {r.sensor} | {r.tipo} | {r.calle} | {r.barrio} | {r.med_N:.1f} | {r.mapa_N:.1f} | {r.dif_N:+.1f} |")
    (AQUI / "validacion_sensores.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas[:14]))
    v.to_csv(AQUI / "cache" / "validacion_sensores.csv", index=False)


if __name__ == "__main__":
    main()
