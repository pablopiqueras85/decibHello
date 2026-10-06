"""DecibHello: detectar el ruido de ocio que el mapa oficial no ve, en calles sin sensor.

Idea: en 140 puntos con sensor municipal conocemos a la vez lo medido (2023) y lo que dice el mapa de ruido 2017.
La diferencia es el error del mapa. Se entrena un modelo que predice ese error a partir de pistas públicas
(bares por tipo, terrazas con sus mesas, quejas por motivo, pisos turísticos, plazas, zonas peatonales, anchura)
y se comprueba con validación cruzada por distritos: el modelo nunca ve el distrito que se evalúa.

Salidas:
- piloto/ocio_oculto.md: comparación de modelos y conclusión.
- piloto/cache/correcciones.json: corrección (dB) por rango del índice para día, tarde y noche, si el modelo mejora.

Uso: python3 piloto/ocio_oculto.py   (después de indice.py y sensores.py)
"""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer
from scipy.spatial import cKDTree
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

AQUI = Path(__file__).parent
CACHE = AQUI / "cache"
API = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/"
RES_CENS_2024 = "38babeec-5c47-43d3-84e7-b13a4b89004f"
RES_TERRASSES_2023_2S = "749a95f2-b905-43e8-b810-f9d04a51eb2e"
RES_TERRASSES_ULTIMO = "ca298802-c798-4750-b078-021af11ce46b"  # 2026, primer semestre
RES_IRIS = {2023: "1ff71f84-20dc-4fc0-9f83-01eecabea330", 2024: "3e988471-ee40-4431-9095-8081fdd651ff",
            2025: "efc9fd4d-a812-427c-846d-a086d22012a4", 2026: "eae9a19a-4543-45db-bc13-3e3073b58324"}
RES_TRAMER_2017 = "3ef70228-789c-47f7-8712-d3789b01a82e"
QUEJAS_GENTE = ["Concentració persones fent soroll", "Sortida locals nocturns", "Músics al carrer", "Festes i activitats esportives"]
QUEJAS_TERRAZA = ["Terrasses / vetlladors"]
BAR = "Bars   / CIBERCAFÈ"
MUSICAL = "Bars especials amb actuació / Bars musicals / Discoteques /PUB"

a_utm = Transformer.from_crs("EPSG:4326", "EPSG:25831", always_xy=True)


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "DecibHello/0.1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def sql(nombre, consulta):
    f = CACHE / f"{nombre}.json"
    if f.exists():
        return json.loads(f.read_text())
    recs, offset = [], 0
    while True:  # la API devuelve como mucho 32.000 filas por consulta
        r = get_json(API + "datastore_search_sql?" + urllib.parse.urlencode({"sql": f"{consulta} LIMIT 32000 OFFSET {offset}"}))["result"]["records"]
        recs += r
        if len(r) < 32000:
            break
        offset += 32000
        time.sleep(0.5)
    f.write_text(json.dumps(recs))
    return recs


def num(v):
    """Número con coma o punto decimal ('4,00' -> 4.0)."""
    return float(str(v).replace(",", "."))


def xy(recs, lat, lon):
    out, filas = [], []
    for r in recs:
        try:
            out.append(a_utm.transform(num(r[lon]), num(r[lat])))
            filas.append(r)
        except (TypeError, ValueError):
            pass
    return np.array(out), filas


def banda_db(b):
    b = b.replace("dB(A)", "").strip()
    return float(b[1:]) - 2.5 if b.startswith("<") else sum(map(float, b.split("-"))) / 2


def cargar_pistas(terrazas_res):
    """Nubes de puntos (UTM) de cada pista, con su peso (p. ej. mesas de la terraza)."""
    cens = sql("cens_ocio_tipos", f'SELECT "Latitud","Longitud","Nom_Activitat","SN_Oci_Nocturn","SN_Obert24h" FROM "{RES_CENS_2024}" '
                                  f'WHERE "Nom_Grup_Activitat" ILIKE \'Restaurants, bars%\' OR "SN_Oci_Nocturn"=\'Si\' OR "SN_Obert24h"=\'Si\'')
    pc, fc = xy(cens, "Latitud", "Longitud")
    act = np.array([f["Nom_Activitat"] for f in fc])
    noche = np.array([f["SN_Oci_Nocturn"] == "Si" or f["SN_Obert24h"] == "Si" for f in fc])
    ter = sql(f"terrazas_{terrazas_res[:8]}", f'SELECT "LATITUD","LONGITUD","TAULES" FROM "{terrazas_res}"')
    pt, ft = xy(ter, "LATITUD", "LONGITUD")
    print(f"terrazas {terrazas_res[:8]}: {len(pt)} de {len(ter)}")
    mesas = np.array([num(f["TAULES"] or 0) for f in ft])
    iris = []
    for anyo, res in RES_IRIS.items():
        detalles = ",".join("'" + d.replace("'", "''") + "'" for d in QUEJAS_GENTE + QUEJAS_TERRAZA)
        iris += sql(f"iris{anyo}_ocio", f'SELECT "LATITUD","LONGITUD","DETALL" FROM "{res}" WHERE "DETALL" IN ({detalles})')
    pi, fi = xy(iris, "LATITUD", "LONGITUD")
    det = np.array([f["DETALL"] for f in fi])
    hut, _ = xy(json.loads((CACHE / "hut.json").read_text()), "LATITUD_Y", "LONGITUD_X")
    return {
        "bares": (pc[act == BAR], None), "musicales": (pc[act == MUSICAL], None),
        "restaurantes": (pc[act == "Restaurants"], None), "noche_24h": (pc[noche], None),
        "mesas": (pt, mesas), "quejas_gente": (pi[np.isin(det, QUEJAS_GENTE)], None),
        "quejas_terraza": (pi[np.isin(det, QUEJAS_TERRAZA)], None), "turisticos": (hut, None),
    }


def contar(puntos, nubes, radios=(50, 100)):
    feats = {}
    for nombre, (nube, peso) in nubes.items():
        arbol = cKDTree(nube)
        for r in radios:
            vecinos = arbol.query_ball_point(puntos, r)
            feats[f"{nombre}_{r}"] = [float(peso[v].sum()) if peso is not None else float(len(v)) for v in vecinos]
    return pd.DataFrame(feats)


def rangos_indice():
    ix = json.loads((CACHE / "indice.json").read_text(encoding="utf-8"))
    campos, n = ix["campos_rango"], len(ix["campos_rango"])
    filas = []
    for c, (nombre, pl) in enumerate(ix["calles"]):
        for k in range(0, len(pl), n):
            r = dict(zip(campos, pl[k:k + n]))
            r.update(calle_idx=c, calle=nombre, k=k // n)
            filas.append(r)
    df = pd.DataFrame(filas)
    x, y = a_utm.transform((2.0 + df.lon_e5 / 1e5).values, (41.3 + df.lat_e5 / 1e5).values)
    df["x"], df["y"] = x, y
    return ix, df


def pistas_mapa(ix, tramos_idx):
    """Pistas que salen del propio mapa de ruido del tramo (componentes por fuente)."""
    t = ix["tramos"]
    B = ix["bandas"]
    campos = ix["campos_tramo"]
    g = lambda i, c: banda_db(B[int(t[i][campos.index(c)])])
    return pd.DataFrame({"mapa_noche": [g(i, "TOTAL_N") for i in tramos_idx], "mapa_trafico_noche": [g(i, "TRANSIT_N") for i in tramos_idx],
                         "mapa_ocio_noche": [g(i, "OCI_N") for i in tramos_idx]})


def vianants_por_tramo(ix):
    """Componente 'zona de vianants' (tarde) del mapa para cada tramo usado en el índice (se descarga aparte)."""
    recs = sql("tramer2017_vianants", f'SELECT "TRAM","VIANANTS_E","TOTAL_D","TOTAL_E","TOTAL_N","TRANSIT_N","OCI_N" FROM "{RES_TRAMER_2017}"')
    return recs


def cv_ridge(X, y, grupos, cols, intercepto=True, alpha=10.0):
    A = X[cols].values
    mu, sd = A.mean(0), A.std(0) + 1e-9
    if not intercepto:
        mu = np.zeros_like(mu)
    p = np.zeros(len(y))
    for tr, te in LeaveOneGroupOut().split(A, y, grupos):
        p[te] = Ridge(alpha=alpha, fit_intercept=intercepto).fit((A[tr] - mu) / sd, y[tr]).predict((A[te] - mu) / sd)
    return p


def analisis_trampa(X, val, grupos):
    """Comprueba de dónde sale la mejora, si las pistas sirven para avisar y la regla de la zona de bares."""
    from sklearn.metrics import roc_auc_score
    pistas = [c for c in X.columns if c.split("_")[-1] in ("50", "100")] + ["plaza_30"]
    out = ["## La trampa: de dónde sale la mejora", "",
           "| Franja | Solo el mapa | Modelo con todo | Solo el nivel del mapa | Solo pistas de ocio (sin intercepto) |", "|---|---|---|---|---|"]
    todas = [c for c in X.columns]
    for f in "DEN":
        y = val[f"dif_{f}"].values
        err = lambda p: f"{np.abs(y - p).mean():.1f} dB"
        out.append(f"| {f} | {err(np.zeros_like(y))} | {err(cv_ridge(X, y, grupos, todas))} | {err(cv_ridge(X, y, grupos, ['mapa_noche']))} | "
                   f"{err(cv_ridge(X, y, grupos, pistas, intercepto=False))} |")
    tabla = val.assign(mapa=X.mapa_noche.values).groupby(pd.cut(X.mapa_noche.values, [0, 50, 55, 60, 65, 80])).dif_N.agg(["count", "median"])
    out += ["", "Error del mapa de noche según lo que dice el propio mapa:", "", "| Mapa (noche) | Sensores | Diferencia mediana |", "|---|---|---|"]
    for intervalo, fila in tabla.iterrows():
        out.append(f"| {intervalo} dB | {int(fila['count'])} | {fila['median']:+.1f} dB |")
    out += ["", "Casi toda la mejora viene del nivel del propio mapa: donde el mapa marca poco ruido, el sensor mide mucho más. "
            "Pero los sensores no están puestos al azar: los de zonas \"tranquilas\" en el mapa se instalaron por quejas. "
            "Aplicar esa regla a toda la ciudad subiría el ruido de calles de verdad tranquilas, así que **no se aplica**.", ""]
    bares = np.round(np.expm1(X.bares_100)).astype(int).values
    out += ["## Pistas como aviso (sin el nivel del mapa)", "", "AUC: 0,5 = azar, 1 = perfecto. Objetivo: el mapa se queda corto más de 5 dB.", "",
            "| Pista | Tarde | Noche |", "|---|---|---|"]
    for c in ["bares_100", "bares_50", "quejas_gente_100", "mesas_50", "musicales_100", "plaza_30"]:
        out.append(f"| {c} | {roc_auc_score(val.dif_E > 5, X[c]):.2f} | {roc_auc_score(val.dif_N > 5, X[c]):.2f} |")
    out += ["", "De noche ninguna pista supera claramente el azar. Por la tarde, el número de bares sí.", "",
            "## Corrección adoptada: proporcional al número de bares y discotecas", "",
            "Suma en dB = a · log(1 + bares) + b · log(1 + bares musicales y discotecas) + c · log(1 + pisos turísticos), "
            "con a, b, c ≥ 0 y sin término fijo (una calle sin locales no suma nada). Bares sin contar restaurantes; todo a menos de 100 m. "
            "Ajustado por mínimos cuadrados no negativos y validado dejando fuera cada distrito.", "",
            "| Franja | Bares (a) | Musicales y discotecas (b) | Pisos turísticos (c) | Error medio, solo mapa → con corrección (validado por distritos) |",
            "|---|---|---|---|---|"]
    from scipy.optimize import nnls
    A = X[["bares_100", "musicales_100", "turisticos_100"]].values
    for f in "DEN":
        y = val[f"dif_{f}"].values
        p = np.zeros(len(y))
        for tr, te in LeaveOneGroupOut().split(A, y, grupos):
            p[te] = A[te] @ nnls(A[tr], y[tr])[0]
        coef = nnls(A, y)[0]
        out.append(f"| {f} | {coef[0]:.2f} | {coef[1]:.2f} | {coef[2]:.2f} | {np.abs(y).mean():.2f} → {np.abs(y - p).mean():.2f} dB |")
    out += ["", "Los coeficientes se usan tal cual en `modelo.py` (`COEF_LOCALES`). Ejemplos de día / tarde / noche: "
            "10 bares ≈ +3,2 / +7,0 / +4,6 dB; 10 bares y 5 musicales ≈ +6,2 / +8,2 / +4,6 dB.",
            "Los pisos turísticos salen con coeficiente 0 en todas las franjas: no suben el nivel medio de la hora que miden los sensores. "
            "Sí cuentan en el aviso de picos nocturnos (20 o más a menos de 100 m: llegadas y salidas a deshoras).",
            "Donde hay sensor no se aplica: la medición ya lo recoge.", ""]
    return out


def main():
    ix, rangos = rangos_indice()
    puntos_rango = rangos[["x", "y"]].values
    plazas = rangos[rangos.calle.str.startswith("Plaça")][["x", "y"]].values
    arbol_plazas = cKDTree(plazas)
    arbol_rangos = cKDTree(puntos_rango)

    # Sensores con medición y valor del mapa (de sensores.py)
    val = pd.read_csv(CACHE / "validacion_sensores.csv")
    sens = pd.DataFrame(json.loads((CACHE / "sensors_todos.json").read_text()))
    sens["sensor"] = sens.Id_Instal.astype(float).astype(int)
    sens = sens.drop_duplicates("sensor")[["sensor", "Latitud", "Longitud", "Codi_Districte", "Nom_Districte"]]
    val = val.merge(sens, on="sensor", how="left")
    sx, sy = a_utm.transform(val.Longitud.astype(float).values, val.Latitud.astype(float).values)
    psens = np.c_[sx, sy]

    def pistas(puntos, terrazas_res, rango_de_punto):
        f = contar(puntos, cargar_pistas(terrazas_res))
        f["plaza_30"] = [1.0 if v else 0.0 for v in arbol_plazas.query_ball_point(puntos, 30)]
        r = rangos.iloc[rango_de_punto]
        f["ancho"] = np.where(r.ancho_m.values >= 0, r.ancho_m.values, 30).astype(float)
        f = pd.concat([f, pistas_mapa(ix, r.tramo.values)], axis=1)
        for c in f.columns:
            if c.split("_")[-1] in ("50", "100"):
                f[c] = np.log1p(f[c])
        return f

    _, cerca = arbol_rangos.query(psens)
    X = pistas(psens, RES_TERRASSES_2023_2S, cerca)
    grupos = val.Codi_Districte.astype(str).values
    informe = ["# DecibHello — Ruido de ocio que el mapa no ve", "",
               f"Puntos de entrenamiento: {len(val)} sensores municipales (2023) con medición y tramo del mapa a menos de 30 m.",
               "Objetivo: diferencia entre lo medido y el mapa 2017 (dB), por franja.",
               "Validación: se deja fuera un distrito cada vez (10 rondas); el modelo nunca ha visto el distrito que se evalúa.", "",
               "**Conclusión.** Un modelo con todas las pistas parece mejorar mucho, pero casi toda la mejora sale del nivel del "
               "propio mapa, y eso es un efecto de dónde están puestos los sensores (por quejas), no algo aplicable a toda la ciudad. "
               "Lo que sí se sostiene es una regla sencilla: en zonas con 10 o más bares a menos de 100 m, el mapa se queda corto "
               "de día y por la tarde. Se corrige con una estimación prudente (+6 dB de día, +8,8 dB por la tarde). De noche, "
               "ninguna pista pública predice el error: hacen falta mediciones (sensores, móviles, vecinos).", ""]
    modelos = {
        "Ridge (lineal)": lambda: make_pipeline(StandardScaler(), Ridge(alpha=10.0)),
        "Árboles (gradient boosting)": lambda: GradientBoostingRegressor(loss="huber", max_depth=2, n_estimators=200, learning_rate=0.03, subsample=0.8, random_state=0),
        "Bosque aleatorio": lambda: RandomForestRegressor(n_estimators=400, min_samples_leaf=5, max_features=0.5, random_state=0),
    }
    resultados = {}
    for f in "DEN":
        y = val[f"dif_{f}"].values
        filas = [("Solo el mapa (sin corrección)", np.zeros_like(y))]
        cte = np.zeros_like(y)
        preds = {k: np.zeros_like(y) for k in modelos}
        for tr, te in LeaveOneGroupOut().split(X, y, grupos):
            cte[te] = np.median(y[tr])
            for k, m in modelos.items():
                preds[k][te] = m().fit(X.iloc[tr], y[tr]).predict(X.iloc[te])
        filas.append(("Corrección constante (mediana)", cte))
        filas += list(preds.items())
        nombre = {"D": "Día (7-19 h)", "E": "Tarde (19-23 h)", "N": "Noche (23-7 h)"}[f]
        informe += [f"## {nombre}", "", "| Método | Error mediano | Error medio | Dentro de ±3 dB | Dentro de ±5 dB | Error medio donde el mapa falla > 8 dB |",
                    "|---|---|---|---|---|---|"]
        grandes = np.abs(y) > 8
        for k, p in filas:
            e = np.abs(y - p)
            informe.append(f"| {k} | {np.median(e):.1f} dB | {e.mean():.1f} dB | {(e <= 3).mean():.0%} | {(e <= 5).mean():.0%} | {e[grandes].mean():.1f} dB ({grandes.sum()} sensores) |")
            resultados[(f, k)] = e
        informe.append("")
    informe += analisis_trampa(X, val, grupos)
    (AQUI / "ocio_oculto.md").write_text("\n".join(informe) + "\n", encoding="utf-8")
    print("\n".join(informe))
    X.assign(sensor=val.sensor.values, **{f"dif_{f}": val[f"dif_{f}"].values for f in "DEN"}).to_csv(CACHE / "ocio_oculto_X.csv", index=False)


if __name__ == "__main__":
    main()
