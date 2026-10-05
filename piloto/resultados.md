# DecibHello — Primera nota del piloto (v0)

Escala 0–100: **100 = muy ruidoso**. Calculado con `calcular_nota.py`; datos completos en `resultados.csv`.

Es una **primera versión para aprender**, no una nota definitiva: los pesos y umbrales son una propuesta y hay que ajustarlos con la validación sobre el terreno.

## Cómo se calcula (v0)

1. **Base**: nivel del mapa estratégico de ruido de 2017 en el tramo de **fachada a la calle** de la dirección (día, tarde y noche, en franjas de 5 dB).
   - El índice de toda la ciudad (`indice.py`) asigna a cada portal oficial de Barcelona (172.000) su tramo. No basta con el tramo más cercano, porque en las esquinas suele ser la calle de al lado: se elige el tramo cercano que va en la misma dirección que la calle del portal. Coincide con el método anterior basado en OpenStreetMap en 21 de 22 direcciones comprobadas.
   - Los focos se cuentan alrededor del punto central de cada grupo de portales del mismo tramo.
   - Los tramos de **patio interior de manzana** (código `P`) dan la nota "interior".
2. **Hora a hora (estimado)**: el nivel de cada franja se reparte en sus horas con la forma típica del tráfico urbano y, de noche, del ocio nocturno (pico entre las 23 y la 1). La media energética de cada franja sigue siendo la del mapa oficial; solo se suaviza el salto entre franjas.
3. **Nota de cada hora**: 50 puntos en el umbral de su franja (noche 45 dB, que es la recomendación de la OMS; tarde 50 dB; día 55 dB). Es la misma penalización que el indicador europeo Lden: de noche el mismo ruido puntúa más. Cada dB de más suma 1,7 puntos.
4. **Focos intermitentes** en 100 m: locales de ocio nocturno, bares y restaurantes, quejas por ruido en la calle (IRIS 2025) y pisos turísticos.
   - Suman hasta 25 puntos en las horas punta del ocio (23–1 h), menos de 19 a 22 h y de 2 a 4 h, y nada de día.
   - En el interior no se suman.
5. **Sin saturar**: por encima de 70 y por debajo de 30 la nota se comprime suavemente, para que las calles muy ruidosas no empaten todas en 100.
6. **Notas por franja** = media de sus horas. **Nota global** = 30 % día + 20 % tarde + 50 % noche.
7. **Confianza**:
   - alta: hay sensor a menos de 150 m;
   - media: no hay sensor cerca;
   - baja: el tramo encontrado está a más de 40 m o no coincide con la calle.

El visor interactivo (`visor.html`) tiene un buscador para cualquier portal de Barcelona (dirección o enlace de Google Maps) y muestra la curva de 24 horas, exterior e interior, y la calle tramo a tramo. Usa una copia en JavaScript de `modelo.py`; da las mismas notas que este informe.

## Resultados

<!-- tabla:inicio -->
| Nota | Día | Tarde | Noche | Interior | Dirección | Hipótesis | Ruido noche (mapa) | Ocio / bares / quejas / HUT (100 m) | Confianza |
|---|---|---|---|---|---|---|---|---|---|
| 85 | 83 | 85 | 85 | 46 | Gran Via de les Corts Catalanes 600 | ruidosa | 65–70 | 0 / 21 / 0 / 43 | media |
| 84 | 83 | 85 | 85 | 68 | Carrer d'Aragó 300 | ruidosa | 65–70 | 0 / 7 / 1 / 5 | alta |
| 84 | 78 | 86 | 87 | 60 | Travessera de Gràcia 81 | control | 65–70 | 1 / 13 / 8 / 4 | alta |
| 83 | 78 | 85 | 85 | — | Carrer de Sants 100 | intermedia | 65–70 | 0 / 17 / 4 / 4 | media |
| 82 | 78 | 84 | 84 | 49 | Ronda del General Mitre 150 | ruidosa | 65–70 | 0 / 2 / 2 / 2 | media |
| 82 | 78 | 84 | 84 | 43 | Carrer del Consell de Cent 250 | intermedia | 65–70 | 0 / 14 / 0 / 18 | media |
| 81 | 78 | 83 | 83 | 35 | Travessera de Gràcia 150 | control | 60–65 | 1 / 29 / 3 / 50 | alta |
| 78 | 63 | 81 | 86 | 39 | Carrer d'Escudellers 20 | ruidosa | 65–70 | 3 / 45 / 12 / 43 | alta |
| 78 | 63 | 80 | 86 | 49 | Carrer de Tuset 20 | control | 65–70 | 7 / 26 / 3 / 4 | alta |
| 77 | 71 | 79 | 79 | 37 | Travessera de Gràcia 300 | control | 60–65 | 0 / 7 / 0 / 25 | media |
| 74 | 54 | 79 | 85 | 46 | Plaça del Sol 12 | ruidosa | 65–70 | 3 / 29 / 2 / 16 | alta |
| 74 | 62 | 73 | 81 | 31 | Carrer Nou de la Rambla 30 | ruidosa | 60–65 | 1 / 21 / 5 / 44 | media |
| 74 | 63 | 75 | 81 | 43 | Carrer d'Enric Granados 50 | intermedia | 60–65 | 0 / 13 / 1 / 53 | alta |
| 73 | 71 | 74 | 74 | 58 | Carrer Gran de Sant Andreu 200 | intermedia | 55–60 | 0 / 2 / 5 / 0 | media |
| 72 | 63 | 76 | 76 | 49 | Carrer del Parlament 30 | intermedia | 55–60 | 0 / 25 / 5 / 57 | alta |
| 71 | 54 | 76 | 79 | 31 | Carrer de Verdi 20 | ruidosa | 60–65 | 0 / 35 / 8 / 26 | alta |
| 71 | 62 | 75 | 74 | 35 | Rambla del Poblenou 60 | intermedia | 55–60 | 0 / 12 / 6 / 5 | alta |
| 70 | 54 | 70 | 79 | 35 | Carrer de Blai 20 | ruidosa | 60–65 | 0 / 31 / 4 / 51 | alta |
| 69 | 63 | 72 | 72 | 46 | Carrer de la Mare de Déu del Coll 50 | tranquila | 55–60 | 0 / 0 / 2 / 3 | media |
| 64 | 54 | 67 | 68 | — | Passeig de Joan de Borbó Comte de Barcelona 50 | ruidosa | 50–55 | 0 / 15 / 13 / 10 | media |
| 62 | 62 | 63 | 62 | — | Carrer de Campoamor 30 | tranquila | 50–55 | 0 / 0 / 0 / 0 | media |
| 60 | 54 | 62 | 62 | — | Carrer de Pere II de Montcada 10 | tranquila | 50–55 | 0 / 0 / 0 / 0 | media |
| 60 | 54 | 63 | 63 | — | Carrer de les Agudes 20 | tranquila | 50–55 | 0 / 0 / 1 / 0 | media |
| 47 | 46 | 47 | 47 | — | Carrer de Pomaret 20 | tranquila | 40–45 | 0 / 0 / 1 / 0 | media |
<!-- tabla:fin -->

## Qué aprendemos

1. **La nota separa bien los grupos.** Las calles "tranquilas" quedan abajo y las ruidosas arriba.
2. **Cambia el orden según la hora.** A la 1:00 encabezan las calles de ocio (Escudellers, Plaça del Sol, Nou de la Rambla, Verdi). A las 13:00 encabezan las grandes vías de tráfico (Gran Via, Aragó). En la nota global de todo el día sigue pesando más el tráfico, porque está presente las 24 horas. Por eso tiene sentido enseñar la curva por horas y no solo una cifra.
3. **El patio interior cambia mucho la experiencia.** En las calles ruidosas, la nota interior suele estar entre 25 y 40 puntos por debajo de la exterior. Hay excepciones: en Aragó 300 la diferencia es de solo 16, porque su patio también es ruidoso. El informe debe distinguir siempre piso exterior e interior.
4. **Barcelona es ruidosa de noche.** Con la referencia de la OMS (45 dB = 50 puntos), casi ninguna fachada a la calle baja de 50. Es coherente con los datos (el 76 % de los tramos supera 45 dB de noche), pero quizá convenga una escala relativa a Barcelona además de la absoluta.

## Limitaciones conocidas

- **Mapa de 2017**: no recoge los cambios posteriores. Consell de Cent es hoy un eje verde con mucho menos tráfico; su 87 seguramente está sobrevalorado.
- **Bandas de 5 dB**: el mapa no da cifras exactas, así que dos calles en la misma banda empatan.
- **Ubicación del portal**: la geolocalización a veces cae dentro de la manzana. En Blai y Gran de Sant Andreu el tramo está a más de 40 m (confianza baja).
- **Curva horaria estimada**: la forma por horas es un perfil típico, no medido en cada calle. Las mediciones de los sensores (minuto a minuto desde 2024) servirán para sustituirlo, pero su descarga está detrás de una verificación anti-bots.
- **Laborables y fin de semana**: todavía no se distinguen.

## Siguiente paso: validación

Para las calles de control (Tuset y Travessera de Gràcia), el vecino puntúa de 0 a 100, de día y de noche, **sin mirar esta tabla**, y se compara con la nota calculada.
