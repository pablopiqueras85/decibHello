# DecibHello — Ruido de ocio que el mapa no ve

Puntos de entrenamiento: 140 sensores municipales (2023) con medición y tramo del mapa a menos de 30 m.
Objetivo: diferencia entre lo medido y el mapa 2017 (dB), por franja.
Validación: se deja fuera un distrito cada vez (10 rondas); el modelo nunca ha visto el distrito que se evalúa.

**Conclusión.** Un modelo con todas las pistas parece mejorar mucho, pero casi toda la mejora sale del nivel del propio mapa, y eso es un efecto de dónde están puestos los sensores (por quejas), no algo aplicable a toda la ciudad. Lo que sí se sostiene es una regla sencilla: en zonas con 10 o más bares a menos de 100 m, el mapa se queda corto de día y por la tarde. Se corrige con una estimación prudente (+6 dB de día, +8,8 dB por la tarde). De noche, ninguna pista pública predice el error: hacen falta mediciones (sensores, móviles, vecinos).

## Día (7-19 h)

| Método | Error mediano | Error medio | Dentro de ±3 dB | Dentro de ±5 dB | Error medio donde el mapa falla > 8 dB |
|---|---|---|---|---|---|
| Solo el mapa (sin corrección) | 3.0 dB | 4.5 dB | 51% | 66% | 11.7 dB (24 sensores) |
| Corrección constante (mediana) | 3.4 dB | 4.7 dB | 40% | 64% | 10.9 dB (24 sensores) |
| Ridge (lineal) | 2.9 dB | 3.3 dB | 52% | 78% | 5.2 dB (24 sensores) |
| Árboles (gradient boosting) | 2.7 dB | 3.2 dB | 56% | 76% | 5.2 dB (24 sensores) |
| Bosque aleatorio | 2.5 dB | 3.0 dB | 59% | 81% | 6.3 dB (24 sensores) |

## Tarde (19-23 h)

| Método | Error mediano | Error medio | Dentro de ±3 dB | Dentro de ±5 dB | Error medio donde el mapa falla > 8 dB |
|---|---|---|---|---|---|
| Solo el mapa (sin corrección) | 4.3 dB | 5.9 dB | 40% | 56% | 12.8 dB (39 sensores) |
| Corrección constante (mediana) | 4.5 dB | 5.6 dB | 34% | 56% | 10.5 dB (39 sensores) |
| Ridge (lineal) | 3.0 dB | 3.5 dB | 49% | 78% | 4.3 dB (39 sensores) |
| Árboles (gradient boosting) | 3.2 dB | 3.8 dB | 46% | 70% | 5.2 dB (39 sensores) |
| Bosque aleatorio | 3.1 dB | 3.7 dB | 48% | 77% | 6.2 dB (39 sensores) |

## Noche (23-7 h)

| Método | Error mediano | Error medio | Dentro de ±3 dB | Dentro de ±5 dB | Error medio donde el mapa falla > 8 dB |
|---|---|---|---|---|---|
| Solo el mapa (sin corrección) | 2.9 dB | 4.3 dB | 52% | 71% | 14.0 dB (20 sensores) |
| Corrección constante (mediana) | 2.6 dB | 4.1 dB | 58% | 71% | 12.5 dB (20 sensores) |
| Ridge (lineal) | 2.7 dB | 3.5 dB | 56% | 78% | 6.8 dB (20 sensores) |
| Árboles (gradient boosting) | 3.2 dB | 3.7 dB | 49% | 76% | 7.5 dB (20 sensores) |
| Bosque aleatorio | 2.8 dB | 3.6 dB | 52% | 76% | 8.6 dB (20 sensores) |

## La trampa: de dónde sale la mejora

| Franja | Solo el mapa | Modelo con todo | Solo el nivel del mapa | Solo pistas de ocio (sin intercepto) |
|---|---|---|---|---|
| D | 4.5 dB | 3.3 dB | 4.1 dB | 4.1 dB |
| E | 5.9 dB | 3.5 dB | 4.8 dB | 4.6 dB |
| N | 4.3 dB | 3.5 dB | 3.2 dB | 4.6 dB |

Error del mapa de noche según lo que dice el propio mapa:

| Mapa (noche) | Sensores | Diferencia mediana |
|---|---|---|
| (0, 50] dB | 11 | +13.3 dB |
| (50, 55] dB | 10 | +4.7 dB |
| (55, 60] dB | 31 | +3.3 dB |
| (60, 65] dB | 62 | +0.6 dB |
| (65, 80] dB | 26 | -0.6 dB |

Casi toda la mejora viene del nivel del propio mapa: donde el mapa marca poco ruido, el sensor mide mucho más. Pero los sensores no están puestos al azar: los de zonas "tranquilas" en el mapa se instalaron por quejas. Aplicar esa regla a toda la ciudad subiría el ruido de calles de verdad tranquilas, así que **no se aplica**.

## Pistas como aviso (sin el nivel del mapa)

AUC: 0,5 = azar, 1 = perfecto. Objetivo: el mapa se queda corto más de 5 dB.

| Pista | Tarde | Noche |
|---|---|---|
| bares_100 | 0.78 | 0.61 |
| bares_50 | 0.75 | 0.58 |
| quejas_gente_100 | 0.71 | 0.64 |
| mesas_50 | 0.68 | 0.61 |
| musicales_100 | 0.63 | 0.49 |
| plaza_30 | 0.65 | 0.53 |

De noche ninguna pista supera claramente el azar. Por la tarde, el número de bares sí.

## Corrección adoptada: proporcional al número de bares y discotecas

Suma en dB = a · log(1 + bares) + b · log(1 + bares musicales y discotecas) + c · log(1 + pisos turísticos), con a, b, c ≥ 0 y sin término fijo (una calle sin locales no suma nada). Bares sin contar restaurantes; todo a menos de 100 m. Ajustado por mínimos cuadrados no negativos y validado dejando fuera cada distrito.

| Franja | Bares (a) | Musicales y discotecas (b) | Pisos turísticos (c) | Error medio, solo mapa → con corrección (validado por distritos) |
|---|---|---|---|---|
| D | 1.32 | 1.68 | 0.00 | 4.47 → 4.43 dB |
| E | 2.90 | 0.72 | 0.00 | 5.91 → 4.99 dB |
| N | 1.93 | 0.00 | 0.00 | 4.33 → 4.16 dB |

**Margen de error de una calle sin sensor** (error que no se supera en 2 de cada 3 sensores): D ±4.9 dB, E ±6.1 dB, N ±4.6 dB. Se guarda en `incertidumbre.json` y el visor lo muestra como "entre X y Y".

Los coeficientes se usan tal cual en `modelo.py` (`COEF_LOCALES`). Ejemplos de día / tarde / noche: 10 bares ≈ +3,2 / +7,0 / +4,6 dB; 10 bares y 5 musicales ≈ +6,2 / +8,2 / +4,6 dB.
Los pisos turísticos salen con coeficiente 0 en todas las franjas: no suben el nivel medio de la hora que miden los sensores. Sí cuentan en el aviso de picos nocturnos (20 o más a menos de 100 m: llegadas y salidas a deshoras).
Donde hay sensor no se aplica: la medición ya lo recoge.

