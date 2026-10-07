"""Altura de los edificios de Barcelona (número de plantas) a partir del Catastro (INSPIRE, edificios).

Fuente: Dirección General del Catastro, conjunto INSPIRE de edificios de Barcelona (municipio 08900), uso libre
citando la fuente. Se descarga a mano o con este script (no pide verificación anti-robots):
https://www.catastro.hacienda.gob.es/INSPIRE/Buildings/08/08900-BARCELONA/A.ES.SDGC.BU.08900.zip

Resultado: piloto/datos/edificios_catastro.json.gz, con una fila por parte de edificio:
[x, y, radio, plantas] (UTM ETRS89 31N en metros; radio equivalente de su planta en metros).
calcular_nota.py lo usa para saber cuántas plantas tiene el edificio de cada portal (corrección por planta).
"""
import gzip
import json
import math
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

AQUI = Path(__file__).parent
CACHE = AQUI / "cache"
SALIDA = AQUI / "datos" / "edificios_catastro.json.gz"
URL = "https://www.catastro.hacienda.gob.es/INSPIRE/Buildings/08/08900-BARCELONA/A.ES.SDGC.BU.08900.zip"

RE_PARTE = re.compile(r"<bu-ext2d:BuildingPart .*?</bu-ext2d:BuildingPart>", re.S)
RE_POS = re.compile(r"<gml:posList[^>]*>([^<]+)</gml:posList>")
RE_PLANTAS = re.compile(r"<bu-ext2d:numberOfFloorsAboveGround>(\d+)<")


def area_centro(coords):
    """Área y centroide de un polígono (lista de x, y)."""
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(coords, coords[1:] + coords[:1]):
        c = x0 * y1 - x1 * y0
        a += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
    a /= 2
    if abs(a) < 1e-9:
        xs, ys = zip(*coords)
        return 0.0, sum(xs) / len(xs), sum(ys) / len(ys)
    return abs(a), cx / (6 * a), cy / (6 * a)


def partes(gml):
    """Recorre el GML de partes de edificio por trozos, sin cargarlo entero en memoria."""
    resto = ""
    with open(gml, encoding="utf-8") as f:
        while True:
            bloque = f.read(8_000_000)
            if not bloque:
                break
            texto = resto + bloque
            fin = 0
            for m in RE_PARTE.finditer(texto):
                fin = m.end()
                yield m.group(0)
            resto = texto[fin:]


def main():
    zip_ = CACHE / "catastro_edificios_08900.zip"
    if not zip_.exists():
        CACHE.mkdir(exist_ok=True)
        print("descargando", URL)
        urllib.request.urlretrieve(URL, zip_)
    gml = CACHE / "A.ES.SDGC.BU.08900.buildingpart.gml"
    if not gml.exists():
        with zipfile.ZipFile(zip_) as z:
            z.extract(gml.name, CACHE)
    filas = []
    for p in partes(gml):
        pl = RE_PLANTAS.search(p)
        pos = RE_POS.search(p)
        if not pl or not pos or int(pl.group(1)) < 1:
            continue
        v = list(map(float, pos.group(1).split()))
        coords = list(zip(v[0::2], v[1::2]))
        area, cx, cy = area_centro(coords)
        filas.append([round(cx), round(cy), round(math.sqrt(area / math.pi), 1), int(pl.group(1))])
    SALIDA.parent.mkdir(exist_ok=True)
    with gzip.open(SALIDA, "wt", encoding="utf-8") as f:
        json.dump(filas, f, separators=(",", ":"))
    plantas = sorted(r[3] for r in filas)
    print(f"partes de edificio: {len(filas)} · plantas mediana {plantas[len(plantas) // 2]} · "
          f"p90 {plantas[int(len(plantas) * 0.9)]} · {SALIDA.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    sys.exit(main())
