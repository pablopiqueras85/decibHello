"""Estudio (8 oct 2026): ¿cómo combinar el censo de locales 2024 y Overture Maps para la suma por bares?

Misma prueba que ocio_oculto.py: en los sensores municipales, diferencia entre lo medido (2023) y el mapa 2017 (dB),
explicada con a·log(1+bares) + b·log(1+musicales y discotecas) + c·log(1+pisos turísticos) a menos de 100 m,
mínimos cuadrados no negativos, validado dejando fuera cada distrito.
Variantes de unión: un local de Overture cuenta como nuevo si no hay ningún local del censo a menos de R metros.

Uso: python3 piloto/estudios/combinado_validacion.py   (después de indice.py, sensores.py y overture.py)
"""
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer
from scipy.optimize import nnls
from scipy.spatial import cKDTree
from sklearn.model_selection import LeaveOneGroupOut

PILOTO = Path(__file__).resolve().parent.parent
CACHE = PILOTO / "cache"
a_utm = Transformer.from_crs("EPSG:4326", "EPSG:25831", always_xy=True)


def utm(pares):
    pares = np.asarray(pares, dtype=float)
    return np.c_[a_utm.transform(pares[:, 1], pares[:, 0])]


def censo(nombre, lat="Latitud", lon="Longitud"):
    out = []
    for r in json.loads((CACHE / f"{nombre}.json").read_text()):
        try:
            out.append((float(r[lat]), float(r[lon])))
        except (TypeError, ValueError, KeyError):
            pass
    return utm(out)


def nuevos(ov, ref, radio):
    """Locales de Overture sin ningún local de referencia a menos de `radio` metros."""
    d, _ = cKDTree(ref).query(ov, distance_upper_bound=radio)
    return ov[np.isinf(d)]


def main():
    val = pd.read_csv(CACHE / "validacion_sensores.csv")
    sens = pd.DataFrame(json.loads((CACHE / "sensors_todos.json").read_text()))
    sens["sensor"] = sens.Id_Instal.astype(float).astype(int)
    val = val.merge(sens.drop_duplicates("sensor")[["sensor", "Latitud", "Longitud", "Codi_Districte"]], on="sensor", how="left")
    S = utm(np.c_[val.Latitud.astype(float), val.Longitud.astype(float)])
    grupos = val.Codi_Districte.astype(str).values

    bares_c, mus_c = censo("cens_solo_bares"), censo("cens_musicales")
    hosteleria_c, oci_c = censo("cens_bars"), censo("cens_oci")
    hut = censo("hut", "LATITUD_Y", "LONGITUD_X")
    ov = json.loads(gzip.open(PILOTO / "datos" / "overture_locales.json.gz", "rt", encoding="utf-8").read())
    bares_o, noche_o = utm(ov["bares"]), utm(ov["noche"])

    def n100(p):
        return np.log1p(np.array([len(v) for v in cKDTree(p).query_ball_point(S, 100)]))

    variantes = {"Censo 2024 (actual)": (bares_c, mus_c), "Solo Overture": (bares_o, noche_o)}
    for radio in (10, 15, 25, 40):
        variantes[f"Censo + Overture nuevos (R = {radio} m, frente a toda la hostelería)"] = (
            np.vstack([bares_c, nuevos(bares_o, hosteleria_c, radio)]),
            np.vstack([mus_c, nuevos(noche_o, np.vstack([mus_c, oci_c]), radio)]))
    variantes["Censo + Overture nuevos (R = 15 m, frente a la misma categoría)"] = (
        np.vstack([bares_c, nuevos(bares_o, bares_c, 15)]), np.vstack([mus_c, nuevos(noche_o, mus_c, 15)]))

    tur = n100(hut)
    print(f"sensores: {len(val)} · Overture {ov['version']}: {len(bares_o)} bares, {len(noche_o)} de noche\n")
    print("| Variante | Bares | Musicales | Día | Tarde | Noche | Media |")
    print("|---|---|---|---|---|---|---|")
    base = [np.abs(val[f"dif_{f}"].values).mean() for f in "DEN"]
    print(f"| Solo el mapa | — | — | {base[0]:.2f} | {base[1]:.2f} | {base[2]:.2f} | {np.mean(base):.2f} |")
    for nombre, (b, m) in variantes.items():
        A = np.c_[n100(b), n100(m), tur]
        errores, coefs = [], []
        for f in "DEN":
            y = val[f"dif_{f}"].values
            p = np.zeros(len(y))
            for tr, te in LeaveOneGroupOut().split(A, y, grupos):
                p[te] = A[te] @ nnls(A[tr], y[tr])[0]
            errores.append(np.abs(y - p).mean())
            coefs.append(nnls(A, y)[0])
        print(f"| {nombre} | {len(b)} | {len(m)} | " + " | ".join(f"{e:.2f}" for e in errores) + f" | {np.mean(errores):.2f} |")
        print("|   coeficientes (bares, musicales, turísticos) | | | " + " | ".join(
            ", ".join(f"{c:.2f}" for c in k) for k in coefs) + " | |")


if __name__ == "__main__":
    main()
