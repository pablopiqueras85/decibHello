"""DecibHello: nota de ruido del piloto y construcción del visor.

1. Lee el índice de toda la ciudad (indice.py -> cache/indice.json).
2. Calcula la nota hora a hora (modelo.py) de las direcciones de direcciones.txt -> resultados.csv y tabla de resultados.md.
3. Incrusta el índice y la lista del piloto en visor_plantilla.html -> visor.html (buscador para cualquier portal de Barcelona).

Uso: python3 piloto/indice.py  (una vez, descarga datos)  y después  python3 piloto/calcular_nota.py
"""

import csv
import json
import re
import unicodedata
from pathlib import Path

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


def mapa_tramo(indice, i):
    t = indice["tramos"][i]
    return {campo: indice["bandas"][int(t[k])] for k, campo in enumerate(indice["campos_tramo"])}


def main():
    indice = json.loads(INDICE.read_text(encoding="utf-8"))
    campos = indice["campos_rango"]
    filas = []
    for info in leer_direcciones():
        calle, numero = info["direccion"].rsplit(" ", 1)
        r, exacto = buscar(indice, calle, int(numero))
        v = dict(zip(campos, r))
        mapa = mapa_tramo(indice, v["tramo"])
        res = modelo.calcular(mapa, {"ocio": v["ocio"], "bares": v["bares"], "quejas": v["quejas"], "turisticos": v["turisticos"]})
        interior = None
        if v["patio"] >= 0:
            mp = mapa_tramo(indice, v["patio"])
            interior = modelo.calcular({f"TOTAL_{f}": mp[f"TOTAL_{f}"] for f in "DEN"})
        focos = {"ocio": v["ocio"], "bares": v["bares"], "quejas": v["quejas"], "turisticos": v["turisticos"]}
        noches = {modelo.DIAS[d]: round(modelo.calcular(mapa, focos, d)["franjas"]["N"]) for d in range(7)}
        confianza = "alta" if v["sensor_dam"] <= RADIO_SENSOR_DAM else "media"
        if not exacto:
            confianza = "baja"
        filas.append({
            "direccion": info["direccion"], "grupo": info["grupo"],
            "nota_global": round(res["global"]), "nota_dia": round(res["franjas"]["D"]),
            "nota_tarde": round(res["franjas"]["E"]), "nota_noche": round(res["franjas"]["N"]),
            "nota_global_interior": round(interior["global"]) if interior else "",
            "mes_dia": mapa["TOTAL_D"], "mes_tarde": mapa["TOTAL_E"], "mes_noche": mapa["TOTAL_N"],
            "mes_trafico_noche": mapa["TRANSIT_N"], "mes_ocio_noche": mapa["OCI_N"],
            "ocio_nocturno_100m": v["ocio"], "bares_rest_100m": v["bares"], "quejas_ruido_100m": v["quejas"],
            "pisos_turisticos_100m": v["turisticos"], "sensor_mas_cercano_m": v["sensor_dam"] * 10,
            "rango_portales": f'{v["ini"]}-{v["fin"]}', "confianza": confianza,
            "ancho_m": v["ancho_m"], "quejas_recogida_100m": v["quejas_recogida"],
            "picos_nocturnos": modelo.aviso_picos(v["ancho_m"], v["quejas_recogida"]),
            **{f"noche_{d}": n for d, n in noches.items()},
        })

    with open(AQUI / "resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    escribir_tabla_md(filas)
    construir_visor(indice)

    for r in sorted(filas, key=lambda r: -r["nota_global"]):
        print(f'{r["nota_global"]:>3}  D{r["nota_dia"]:>3} T{r["nota_tarde"]:>3} N{r["nota_noche"]:>3}  int {str(r["nota_global_interior"]):>3}  '
              f'{r["grupo"]:<11} {r["direccion"]:<46} {r["confianza"]}')


def construir_visor(indice):
    piloto = [{"direccion": d["direccion"], "grupo": d["grupo"], "aviso": d["aviso"]} for d in leer_direcciones()]
    datos = json.dumps({"indice": indice, "piloto": piloto}, ensure_ascii=False, separators=(",", ":"))
    html = (AQUI / "visor_plantilla.html").read_text(encoding="utf-8").replace("/*DATOS*/null", datos)
    (AQUI / "visor.html").write_text(html, encoding="utf-8")


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
