# DecibHello — piloto de Barcelona

Prototipo que calcula una nota de ruido de 0 a 100 (100 = muy ruidoso) para cualquier portal de Barcelona, hora a hora y por día de la semana, con un visor web que funciona sin servicios externos.

## Ficheros

| Fichero | Qué es |
|---|---|
| `modelo.py` | El modelo de la nota (franjas, horas, días, focos, picos nocturnos). El visor tiene una copia en JavaScript. |
| `indice.py` | Construye el índice de toda la ciudad: cada portal oficial con su tramo del mapa de ruido, su patio, focos cercanos, anchura de calle y quejas. |
| `ocio_oculto.py` | Prueba si las pistas públicas (bares, terrazas, quejas…) predicen dónde el mapa se queda corto; de ahí sale la corrección de la zona de bares (`ocio_oculto.md`). |
| `sensores.py` | Analiza los datos por hora de los sensores municipales: perfiles por hora y día, nivel medido por sensor y comparación con el mapa oficial. |
| `calcular_nota.py` | Calcula el piloto (`direcciones.txt`) y construye el visor. |
| `direcciones.txt` | Direcciones del piloto y de control. |
| `visor_plantilla.html` | Plantilla del visor; `visor.html` es el resultado con los datos dentro. |
| `resultados.md` / `resultados.csv` | Notas del piloto y conclusiones. |
| `validacion_sensores.md` | Sensores frente al mapa oficial. |
| `perfiles_sensores.json`, `perfiles_por_sensor.json` | Perfiles medidos que usan el modelo y el visor. |

## Cómo regenerarlo todo

```bash
pip install pyproj shapely numpy pandas scipy scikit-learn
python3 piloto/indice.py        # descarga datos de Open Data BCN (caché en piloto/cache/) y crea el índice
python3 piloto/sensores.py      # necesita los CSV por hora en piloto/sensores/ (ver abajo)
python3 piloto/ocio_oculto.py   # análisis del ocio que el mapa no ve (informe)
python3 piloto/calcular_nota.py # notas del piloto + visor.html
```

Los CSV de sensores (`2023_1S_…_1Hora.csv`, `2023_2S_…_1Hora.csv`) se descargan a mano de [Open Data BCN](https://opendata-ajuntament.barcelona.cat/data/es/dataset/xarxasoroll-equipsmonitor-dades) porque el portal pide verificación anti-robots. No se suben al repositorio (unos 50 MB); van en `piloto/sensores/`.

## Comprobaciones

- La nota del visor (JavaScript) y la de `calcular_nota.py` (Python) coinciden en las 26 direcciones del piloto: nota global, las 7 noches y el aviso de picos.
- Datos de sensores: de 7:00 a 23:59 la fecha registrada es la del día siguiente; `sensores.py` lo corrige.
