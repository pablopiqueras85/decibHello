# DecibHello — Primera nota del piloto (v0)

Escala 0–100: **100 = muy ruidoso**. Calculado con `calcular_nota.py`; datos completos en `resultados.csv`.

Es una **primera versión para aprender**, no una nota definitiva: los pesos y umbrales son una propuesta y hay que ajustarlos con la validación sobre el terreno.

## Cómo se calcula (v0)

1. **Base**: nivel del mapa estratégico de ruido de 2017 en el tramo de **fachada a la calle** de la dirección.
   - Para elegir el tramo se usa la geometría de la propia calle (OpenStreetMap), no solo el tramo más cercano, porque en las esquinas el más cercano suele ser la calle de al lado.
   - Los tramos de **patio interior de manzana** (código `P`) se separan y se muestran aparte.
2. **Nota por franja**: 50 puntos en el umbral de referencia (noche 45 dB, que es la recomendación de la OMS; tarde 50 dB; día 55 dB). Cada dB de más suma 1,7 puntos.
3. **Focos intermitentes** en 100 m (suman hasta 25 puntos de noche y la mitad de tarde):
   - locales de ocio nocturno;
   - bares y restaurantes;
   - quejas por ruido en la calle (IRIS 2025);
   - pisos turísticos.
4. **Nota global** = 30 % día + 20 % tarde + 50 % noche.
5. **Confianza**:
   - alta: hay sensor a menos de 150 m;
   - media: no hay sensor cerca;
   - baja: el tramo encontrado está a más de 40 m o no coincide con la calle.

## Resultados

| Nota | Día | Tarde | Noche | Dirección | Hipótesis | Ruido noche (mapa) | Patio noche | Ocio / bares / quejas / HUT (100 m) | Confianza |
|---|---|---|---|---|---|---|---|---|---|
| 95 | 88 | 93 | 99 | Gran Via de les Corts Catalanes 600 | ruidosa | 65–70 | 40–45 | 1 / 23 / 0 / 43 | media |
| 93 | 79 | 95 | 100 | Travessera de Gràcia 81 | control | 65–70 | 50–55 | 1 / 13 / 8 / 4 | alta |
| 92 | 79 | 93 | 99 | Ronda del General Mitre 150 | ruidosa | 65–70 | 40–45 | 1 / 5 / 5 / 3 | media |
| 91 | 88 | 90 | 93 | Carrer d'Aragó 300 | ruidosa | 65–70 | 55–60 | 0 / 7 / 1 / 5 | alta |
| 91 | 79 | 92 | 97 | Carrer de Sants 100 | intermedia | 65–70 | 40–45 | 0 / 12 / 5 / 15 | media |
| 88 | 79 | 87 | 94 | Travessera de Gràcia 150 | control | 60–65 | < 40 | 1 / 30 / 3 / 29 | alta |
| 87 | 79 | 82 | 93 | Carrer del Consell de Cent 250 | intermedia | 65–70 | 40–45 | 0 / 12 / 0 / 15 | media |
| 85 | 62 | 83 | 100 | Carrer dels Escudellers 20 | ruidosa | 65–70 | 40–45 | 4 / 47 / 12 / 43 | alta |
| 85 | 62 | 81 | 100 | Carrer de Tuset 20 | control | 65–70 | 40–45 | 7 / 26 / 4 / 4 | alta |
| 83 | 62 | 73 | 99 | Carrer Nou de la Rambla 30 | ruidosa | 60–65 | < 40 | 2 / 21 / 5 / 45 | media |
| 82 | 54 | 81 | 100 | Plaça del Sol 12 | ruidosa | 65–70 | 45–50 | 3 / 30 / 2 / 16 | alta |
| 80 | 54 | 79 | 96 | Carrer de Verdi 20 | ruidosa | 60–65 | < 40 | 1 / 29 / 11 / 10 | alta |
| 80 | 71 | 82 | 84 | Travessera de Gràcia 300 | control | 60–65 | < 40 | 0 / 6 / 0 / 45 | media |
| 78 | 62 | 75 | 88 | Carrer d'Enric Granados 50 | intermedia | 60–65 | 40–45 | 0 / 13 / 1 / 53 | alta |
| 76 | 54 | 69 | 92 | Carrer de Blai 20 | ruidosa | 60–65 | < 40 | 0 / 31 / 7 / 35 | baja |
| 76 | 62 | 77 | 83 | Passeig de Joan de Borbó 50 | ruidosa | 55–60 | — | 0 / 17 / 13 / 16 | media |
| 75 | 62 | 76 | 82 | Carrer del Parlament 30 | intermedia | 55–60 | < 40 | 0 / 24 / 2 / 48 | alta |
| 75 | 62 | 76 | 82 | Rambla del Poblenou 60 | intermedia | 55–60 | < 40 | 0 / 14 / 8 / 6 | alta |
| 74 | 71 | 73 | 76 | Carrer Gran de Sant Andreu 200 | intermedia | 55–60 | 40–45 | 0 / 2 / 3 / 0 | baja |
| 70 | 62 | 73 | 74 | Carrer de la Mare de Déu del Coll 50 | tranquila | 55–60 | 40–45 | 0 / 0 / 2 / 4 | media |
| 62 | 62 | 62 | 62 | Carrer de Campoamor 30 | tranquila | 50–55 | < 40 | 0 / 0 / 0 / 0 | media |
| 61 | 54 | 64 | 64 | Carrer de les Agudes 20 | tranquila | 50–55 | — | 0 / 0 / 1 / 0 | media |
| 60 | 54 | 62 | 62 | Carrer de Pere II de Montcada 10 | tranquila | 50–55 | — | 0 / 0 / 0 / 0 | media |
| 47 | 46 | 47 | 48 | Carrer de Pomaret 20 | tranquila | 40–45 | — | 0 / 0 / 1 / 0 | media |

## Qué aprendemos

1. **La nota separa bien los grupos.** Las cinco calles "tranquilas" quedan abajo (47–70). Las ruidosas y las de control quedan arriba (76–95).
2. **El tráfico pesa más que el ocio.** Las grandes vías (Gran Via, Ronda del General Mitre, Aragó, Sants) quedan por encima de calles de ocio como Verdi o Blai. Pasa porque el mapa oficial es una media anual, donde el tráfico constante domina, y los focos de ocio solo suman hasta 25 puntos. **Hay que decidir si la molestia del ocio nocturno debe pesar más.** La validación sobre el terreno ayudará a decidirlo.
3. **Travessera de Gràcia baja de forma gradual al alejarse de Tuset**: 93 en el 81, 88 en el 150 y 80 en el 300. Es lo que se esperaba, pero falta encontrar el tramo silencioso.
4. **El patio interior cambia mucho la experiencia.** En casi todas las calles ruidosas, el patio de manzana está en menos de 40–45 dB de noche, 20–25 dB menos que la fachada. El informe debería distinguir siempre "piso exterior" y "piso interior".
5. **Barcelona es ruidosa de noche.** Con la referencia de la OMS (45 dB = 50 puntos), casi ninguna calle baja de 50. Es coherente con los datos (el 76 % de los tramos supera 45 dB de noche), pero quizá convenga una escala relativa a Barcelona además de la absoluta.

## Limitaciones conocidas

- **Mapa de 2017**: no recoge los cambios posteriores. Consell de Cent es hoy un eje verde con mucho menos tráfico; su 87 seguramente está sobrevalorado.
- **Bandas de 5 dB**: el mapa no da cifras exactas, así que dos calles en la misma banda empatan.
- **Ubicación del portal**: la geolocalización a veces cae dentro de la manzana. En Blai y Gran de Sant Andreu el tramo está a más de 40 m (confianza baja).
- **Sensores**: no se usan todavía las mediciones reales, porque su descarga está detrás de una verificación anti-bots.

## Siguiente paso: validación

Para las calles de control (Tuset y Travessera de Gràcia), el vecino puntúa de 0 a 100, de día y de noche, **sin mirar esta tabla**, y se compara con la nota calculada.
