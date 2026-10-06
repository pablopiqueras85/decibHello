# DecibHello — Ruido de las obras públicas (validación con sensores)

Obras de Open Data BCN activas en algún momento de 2023: 458. Sensores municipales con datos por hora de 2023.
Para cada sensor: días laborables con una obra activa a esa distancia frente a días laborables sin ella. Efecto = diferencia de día (8–18 h) menos diferencia de noche (0–5 h, sin obras), para quitar cambios de temporada.

| Distancia de la obra | Sensores | Día | Noche | Efecto (mediana) | Efecto (media) |
|---|---|---|---|---|---|
| 300–600 m | 45 | +0.2 dB | +0.1 dB | +0.2 dB | -0.1 dB |
| 25–75 m | 31 | +0.2 dB | -0.1 dB | +0.4 dB | +0.4 dB |
| 75–150 m | 69 | +0.2 dB | -0.1 dB | +0.1 dB | +0.6 dB |
| 0–25 m | 18 | +1.2 dB | -0.5 dB | +2.1 dB | +2.4 dB |

Sensores con obra a menos de 25 m:

| Sensor | Días con obra | Tipo | Efecto |
|---|---|---|---|
| Enric Granados | 139 | Urbanització | +8.2 dB |
| Escudellers | 73 | Pavimentacions | +5.8 dB |
| Escudellers | 73 | Pavimentacions | +5.6 dB |
| Escudellers | 72 | Pavimentacions | +5.1 dB |
| Masadas | 175 | Urbanització | +3.6 dB |
| Sicília | 58 | Entorns Escolars | +3.1 dB |
| Comte Borrell | 64 | Entorns Escolars | +2.9 dB |
| Consell de Cent | 17 | Urbanització | +2.6 dB |
| Arc del Teatre | 97 | Edificació, Urbanització | +2.2 dB |
| Gràcia | 25 | Mobilitat | +2.1 dB |
| Consell de Cent | 18 | Urbanització | +1.2 dB |
| Sicília | 193 | Urbanització | +1.0 dB |
| Provença | 236 | Serveis | +0.8 dB |
| Corts Catalanes | 142 | Urbanització | +0.6 dB |
| Vall d'Hebron | 53 | Urbanització | +0.4 dB |
| Aragó | 49 | Infraestructura del transport | -0.2 dB |
| Mallorca | 238 | Mobilitat, Urbanització | -0.3 dB |
| Comte d'Urgell | 40 | Urbanització | -0.8 dB |

Conclusión: el efecto se concentra a menos de 25 m (mediana ≈ +2 dB de día laborable de media durante toda la obra, con fases mucho más fuertes: hasta +8 dB de media en una reurbanización). A partir de 25 m es casi nulo, y a 300–600 m (control) no hay efecto. El modelo suma +2 dB de 8 a 18 h, de lunes a viernes, mientras la obra está activa y a menos de 25 m del portal. Las obras a menos de 100 m se muestran en el informe.
