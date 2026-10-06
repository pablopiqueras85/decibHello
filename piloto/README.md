# DecibHello — piloto de Barcelona

Prototipo que calcula una nota de ruido de 0 a 100 (100 = muy ruidoso) para cualquier portal de Barcelona, hora a hora y por día de la semana, con un visor web que funciona sin servicios externos.

## Ficheros

| Fichero | Qué es |
|---|---|
| `modelo.py` | El modelo de la nota (franjas, horas, días, focos, picos nocturnos). El visor tiene una copia en JavaScript. |
| `indice.py` | Construye el índice de toda la ciudad: cada portal oficial con su tramo del mapa de ruido, su patio, focos cercanos, anchura de calle y quejas. |
| `ocio_oculto.py` | Prueba si las pistas públicas (bares, terrazas, quejas…) predicen dónde el mapa se queda corto; de ahí sale la suma proporcional por bares y discotecas (`ocio_oculto.md`). |
| `horarios_ocio.py` | Lee los horarios de discotecas, bares musicales y coctelerías y calcula qué noches abren de madrugada cerca de cada portal. |
| `obras.py` | Obras públicas de Open Data BCN: validación con sensores (`obras_validacion.md`) y obras cerca de cada portal. |
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
python3 piloto/obras.py         # validación del ruido de las obras (informe)
python3 piloto/calcular_nota.py # notas del piloto + visor.html (descarga las obras vigentes del día)
```

Los CSV de sensores (`2023_1S_…_1Hora.csv`, `2023_2S_…_1Hora.csv`) se descargan a mano de [Open Data BCN](https://opendata-ajuntament.barcelona.cat/data/es/dataset/xarxasoroll-equipsmonitor-dades) porque el portal pide verificación anti-robots. No se suben al repositorio (unos 50 MB); van en `piloto/sensores/`.

## Actualización diaria

Una tarea programada ("DecibHello: actualizar obras del visor", de lunes a viernes a las 6:47, hora de Madrid) regenera el índice y el visor con las obras públicas del día (Open Data BCN las actualiza a diario) y republica el visor en el mismo enlace. Si algo falla, no publica. Las obras que empiezan o terminan entre dos actualizaciones ya se tienen en cuenta en el visor, porque compara sus fechas con el día en que se mira. Las quejas IRIS se publican cada trimestre, así que no sirven para avisos del día.

## Comprobaciones

- La nota del visor (JavaScript) y la de `calcular_nota.py` (Python) coinciden en las direcciones del piloto: nota global, las 7 noches y el aviso de picos. Se comprueba con `cd piloto/pruebas && npm install && node paridad.mjs` (0 diferencias).
- Datos de sensores: de 7:00 a 23:59 la fecha registrada es la del día siguiente; `sensores.py` lo corrige.
