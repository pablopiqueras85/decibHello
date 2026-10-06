# DecibHello — Nota del piloto (v1, calibrada con sensores)

Escala 0–100: **100 = muy ruidoso**. Calculado con `calcular_nota.py`; datos completos en `resultados.csv`.

Es una **primera versión para aprender**, no una nota definitiva: los pesos y umbrales son una propuesta y hay que ajustarlos con la validación sobre el terreno.

## Cómo se calcula (v1)

1. **Base**: nivel del mapa estratégico de ruido de 2017 en el tramo de **fachada a la calle** de la dirección (día, tarde y noche, en franjas de 5 dB).
   - El índice de toda la ciudad (`indice.py`) asigna a cada portal oficial de Barcelona (172.000) su tramo. No basta con el tramo más cercano, porque en las esquinas suele ser la calle de al lado: se elige el tramo cercano que va en la misma dirección que la calle del portal. Coincide con el método anterior basado en OpenStreetMap en 21 de 22 direcciones comprobadas.
   - Los focos se cuentan alrededor del punto central de cada grupo de portales del mismo tramo.
   - Los tramos de **patio interior de manzana** (código `P`) dan la nota "interior".
2. **Hora a hora**: el nivel de cada franja se reparte en sus horas con la forma del tráfico y, de noche, del ocio nocturno **medida por los sensores municipales en 2023** (`sensores.py`). La media energética de cada franja sigue siendo la del mapa oficial; solo se suaviza el salto de las 18–19 h y de las 22–23 h.
3. **Nota de cada hora**: lineal entre los extremos reales de Barcelona en su franja. Día y tarde: 45 dB = 0 y 75 dB = 100. Noche: 35 dB = 0 y 70 dB = 100 (Tuset un viernes de madrugada). De noche el mismo ruido puntúa más. Cada dB suma 3,3 puntos de día y 2,9 de noche. El visor añade la posición en la ciudad: "más ruidosa que el X % de los portales de Barcelona".
4. **Una sola forma de medir**: todas las notas salen del nivel en dB de cada hora con la misma fórmula, sea medido (sensor) o estimado (mapa + patrones medidos). Los bares, quejas y pisos turísticos ya no suman puntos fijos a la nota: comparado con 140 sensores, esos puntos fijos no aportaban nada (error mediano de 4,9 a 4,3 puntos). Los bares y discotecas suman en dB, en proporción a cuántos hay (punto 9), y los horarios de los locales reparten el ruido por noches. Los pisos turísticos no suben la media horaria que miden los sensores, así que cuentan en el aviso de picos nocturnos.
5. **Sin saturar**: por encima de 70 y por debajo de 30 la nota se comprime suavemente, para que las calles muy ruidosas no empaten todas en 100.
6. **Día de la semana (medido)**: el mapa oficial es una media anual. Cada día se reparte con pesos semanales **medidos por 62 sensores de tráfico y 73 de ocio** (2023, sin festivos ni vísperas), que conservan esa media:
   - tráfico de día: sábado −1,2 dB, domingo −2,2 dB;
   - ocio de noche: viernes +2,7 dB y sábado +2,4 dB; lunes −2,6, martes −2,5 y domingo −3,0 (el jueves queda en la media);
   - el ruido de noche no atribuido a ninguna fuente sigue la mezcla de tráfico y ocio de la calle.
7. **Donde hay sensor, manda la medición**: los portales del mismo tramo que un sensor municipal a menos de 60 m, o de la misma calle a menos de 120 m (933 tramos), usan su nivel medido en 2023, día por día y hora por hora, en lugar del mapa y el modelo (352 tramos de la ciudad). Ahí no se suman focos, porque la medición ya los incluye.
8. **Horarios de los locales de noche**: discotecas, bares musicales y coctelerías a menos de 150 m, con los días que abren de madrugada (Open Data BCN, espacios de música y copas). Las noches con más locales abiertos suben y las demás bajan, sin cambiar la media de la semana: unos 2,8 dB por cada vez que se duplica la carga de esa noche, ajustado con los sensores (ver `ocio_oculto.md`).
9. **Bares y discotecas suman en proporción**: en tramos sin sensor, cada franja suma a · log(1 + bares) + b · log(1 + bares musicales y discotecas), todo a menos de 100 m y sin contar restaurantes. Coeficientes ajustados con los sensores y validados dejando fuera cada distrito: día 1,32 y 1,68; tarde 2,90 y 0,72; noche 1,93 y 0. Por ejemplo, 10 bares suman ≈ +3,2 dB de día, +7,0 por la tarde y +4,6 de noche; con 5 musicales más, ≈ +6,2 / +8,2 / +4,6. Sin locales no se suma nada. Los pisos turísticos salen con coeficiente 0 y cuentan en el aviso de picos (20 o más a menos de 100 m). Ver `ocio_oculto.md`.
10. **Notas por franja** = media de sus horas. **Nota global** = 30 % día + 20 % tarde + 50 % noche.
11. **Confianza**:
   - medida: el dato sale de un sensor del mismo tramo;
   - alta: hay sensor a menos de 150 m;
   - media: no hay sensor cerca;
   - baja: el tramo encontrado está a más de 40 m o no coincide con la calle.

El visor interactivo (`visor.html`) tiene un buscador para cualquier portal de Barcelona (dirección o enlace de Google Maps) y muestra la curva de 24 horas, exterior e interior, y la calle tramo a tramo. Usa una copia en JavaScript de `modelo.py`; da las mismas notas que este informe.

## Resultados

<!-- tabla:inicio -->
| Nota | Día | Tarde | Noche | Interior | Dirección | Hipótesis | Ruido noche (mapa) | Ocio / bares / quejas / HUT (100 m) | Confianza |
|---|---|---|---|---|---|---|---|---|---|
| 99 | 100 | 100 | 99 | — | Carrer de Sants 100 | intermedia | 65–70 | 0 / 17 / 4 / 4 | media |
| 99 | 100 | 100 | 97 | 45 | Travessera de Gràcia 81 | control | 65–70 | 1 / 13 / 8 / 4 | alta |
| 98 | 100 | 100 | 97 | 19 | Gran Via de les Corts Catalanes 600 | ruidosa | 65–70 | 0 / 21 / 0 / 43 | media |
| 97 | 97 | 97 | 97 | 61 | Carrer d'Aragó 300 | ruidosa | 65–70 | 0 / 7 / 1 / 5 | medida |
| 95 | 95 | 97 | 95 | 25 | Ronda del General Mitre 150 | ruidosa | 65–70 | 0 / 2 / 2 / 2 | media |
| 95 | 100 | 99 | 91 | 3 | Travessera de Gràcia 150 | control | 60–65 | 1 / 29 / 3 / 50 | alta |
| 86 | 85 | 89 | 85 | 6 | Travessera de Gràcia 300 | control | 60–65 | 0 / 7 / 0 / 25 | media |
| 84 | 78 | 73 | 92 | 10 | Carrer d'Escudellers 20 | ruidosa | 65–70 | 3 / 45 / 12 / 43 | medida |
| 79 | 60 | 83 | 88 | 3 | Carrer de Verdi 20 | ruidosa | 60–65 | 0 / 35 / 8 / 26 | alta |
| 79 | 79 | 84 | 77 | 3 | Carrer de Martínez de la Rosa 20 | control | 55–60 | 3 / 27 / 5 / 57 | media |
| 78 | 71 | 67 | 86 | 3 | Carrer Nou de la Rambla 30 | ruidosa | 60–65 | 1 / 21 / 5 / 44 | media |
| 76 | 75 | 88 | 71 | 3 | Carrer de Blai 20 | ruidosa | 60–65 | 0 / 31 / 4 / 51 | medida |
| 75 | 68 | 65 | 84 | 25 | Carrer de Tuset 20 | control | 65–70 | 7 / 26 / 3 / 4 | medida |
| 73 | 71 | 82 | 70 | 3 | Rambla del Poblenou 60 | intermedia | 55–60 | 0 / 12 / 6 / 5 | medida |
| 69 | 67 | 66 | 72 | 14 | Carrer del Consell de Cent 250 | intermedia | 65–70 | 0 / 14 / 0 / 18 | medida |
| 68 | 58 | 87 | 66 | 20 | Plaça del Sol 12 | ruidosa | 65–70 | 3 / 29 / 2 / 16 | medida |
| 68 | 65 | 75 | 68 | 25 | Carrer del Parlament 30 | intermedia | 55–60 | 0 / 25 / 5 / 57 | medida |
| 67 | 63 | 66 | 70 | 14 | Carrer d'Enric Granados 50 | intermedia | 60–65 | 0 / 13 / 1 / 53 | medida |
| 66 | 75 | 60 | 63 | 41 | Carrer Gran de Sant Andreu 200 | intermedia | 55–60 | 0 / 2 / 5 / 0 | media |
| 61 | 58 | 58 | 63 | 19 | Carrer de la Mare de Déu del Coll 50 | tranquila | 55–60 | 0 / 0 / 2 / 3 | media |
| 53 | 48 | 54 | 56 | — | Passeig de Joan de Borbó Comte de Barcelona 50 | ruidosa | 50–55 | 0 / 15 / 13 / 10 | media |
| 50 | 58 | 43 | 49 | — | Carrer de Campoamor 30 | tranquila | 50–55 | 0 / 0 / 0 / 0 | media |
| 45 | 42 | 41 | 49 | — | Carrer de Pere II de Montcada 10 | tranquila | 50–55 | 0 / 0 / 0 / 0 | media |
| 45 | 42 | 41 | 49 | — | Carrer de les Agudes 20 | tranquila | 50–55 | 0 / 0 / 1 / 0 | media |
| 19 | 25 | 10 | 20 | — | Carrer de Pomaret 20 | tranquila | 40–45 | 0 / 0 / 1 / 0 | media |
<!-- tabla:fin -->

## La noche según el día de la semana

Nota media de la noche (23–7 h) que empieza cada día: la del viernes va del viernes a las 23:00 al sábado a las 7:00. Ordenado por la diferencia entre viernes y lunes.

<!-- semana:inicio -->
| Dirección | Lun | Mar | Mié | Jue | Vie | Sáb | Dom | Vie − lun |
|---|---|---|---|---|---|---|---|---|
| Carrer de Tuset 20 | 60 | 64 | 80 | 87 | 93 | 93 | 57 | +33 |
| Carrer d'Enric Granados 50 | 60 | 65 | 66 | 72 | 78 | 74 | 60 | +18 |
| Plaça del Sol 12 | 57 | 54 | 63 | 63 | 73 | 69 | 57 | +16 |
| Carrer Nou de la Rambla 30 | 77 | 79 | 82 | 88 | 93 | 92 | 77 | +16 |
| Carrer de Verdi 20 | 78 | 79 | 86 | 89 | 93 | 93 | 81 | +15 |
| Rambla del Poblenou 60 | 60 | 63 | 65 | 65 | 74 | 77 | 64 | +14 |
| Carrer d'Escudellers 20 | 84 | 86 | 89 | 91 | 96 | 97 | 85 | +12 |
| Carrer de Blai 20 | 64 | 63 | 67 | 64 | 76 | 74 | 63 | +12 |
| Travessera de Gràcia 81 | 89 | 90 | 98 | 99 | 100 | 99 | 96 | +11 |
| Travessera de Gràcia 150 | 86 | 87 | 91 | 93 | 96 | 94 | 86 | +10 |
| Carrer de Martínez de la Rosa 20 | 73 | 75 | 76 | 78 | 82 | 80 | 73 | +9 |
| Carrer del Consell de Cent 250 | 67 | 70 | 71 | 72 | 75 | 74 | 66 | +8 |
| Carrer Gran de Sant Andreu 200 | 60 | 61 | 62 | 64 | 67 | 65 | 59 | +7 |
| Carrer de Pomaret 20 | 17 | 18 | 19 | 20 | 24 | 22 | 16 | +7 |
| Passeig de Joan de Borbó Comte de Barcelona 50 | 54 | 55 | 56 | 57 | 60 | 58 | 54 | +6 |
| Carrer de Pere II de Montcada 10 | 46 | 47 | 48 | 49 | 52 | 50 | 46 | +6 |
| Carrer de Campoamor 30 | 46 | 47 | 48 | 49 | 52 | 50 | 46 | +6 |
| Carrer de les Agudes 20 | 46 | 47 | 48 | 49 | 52 | 50 | 46 | +6 |
| Carrer del Parlament 30 | 66 | 65 | 64 | 66 | 71 | 71 | 61 | +5 |
| Carrer de la Mare de Déu del Coll 50 | 61 | 61 | 62 | 63 | 66 | 64 | 60 | +5 |
| Travessera de Gràcia 300 | 83 | 84 | 85 | 86 | 88 | 86 | 82 | +5 |
| Carrer d'Aragó 300 | 95 | 95 | 97 | 97 | 99 | 99 | 96 | +4 |
| Gran Via de les Corts Catalanes 600 | 95 | 96 | 96 | 97 | 99 | 97 | 95 | +4 |
| Ronda del General Mitre 150 | 92 | 93 | 94 | 95 | 96 | 95 | 92 | +4 |
| Carrer de Sants 100 | 97 | 98 | 98 | 99 | 100 | 99 | 97 | +3 |
<!-- semana:fin -->

## Picos nocturnos: camiones de recogida y limpieza

El paso de un camión de basura o de limpieza de madrugada es un pico corto que apenas mueve la media anual del mapa oficial, pero despierta a los vecinos, sobre todo en calles estrechas donde el sonido rebota entre fachadas. Por eso va como **aviso aparte**, no dentro de la nota:

- **Anchura de la calle**: distancia entre portales de lados opuestos (listado oficial de portales). Estrecha: menos de 12 m.
- **Quejas** al Ajuntament (IRIS 2023–2026) por ruido de "servicios de limpieza y recogida", a menos de 100 m.
- **Aviso alto**: calle estrecha con alguna queja cerca, o 5 quejas o más. **Medio**: calle estrecha, o alguna queja. **Bajo**: el resto.

Falta lo más importante, que no es público: la ubicación de los contenedores y las rutas y horarios de los camiones.

<!-- picos:inicio -->
| Dirección | Anchura | Quejas recogida y limpieza (100 m, 2023-26) | Picos nocturnos |
|---|---|---|---|
| Carrer d'Escudellers 20 | 7 m | 7 | alto |
| Travessera de Gràcia 150 | 8 m | 0 | alto |
| Carrer de Martínez de la Rosa 20 | 8 m | 5 | alto |
| Carrer de Verdi 20 | 10 m | 2 | alto |
| Carrer Nou de la Rambla 30 | 11 m | 1 | alto |
| Carrer de Blai 20 | 12 m | 3 | alto |
| Carrer Gran de Sant Andreu 200 | 14 m | 5 | alto |
| Carrer d'Enric Granados 50 | 22 m | 1 | alto |
| Carrer del Parlament 30 | 22 m | 3 | alto |
| Gran Via de les Corts Catalanes 600 | — | 0 | medio |
| Carrer de Pomaret 20 | 12 m | 1 | medio |
| Carrer de la Mare de Déu del Coll 50 | 13 m | 1 | medio |
| Rambla del Poblenou 60 | 22 m | 3 | medio |
| Travessera de Gràcia 81 | 23 m | 4 | medio |
| Travessera de Gràcia 300 | 23 m | 0 | medio |
| Carrer de Sants 100 | 24 m | 1 | medio |
| Plaça del Sol 12 | 25 m | 1 | medio |
| Carrer de Pere II de Montcada 10 | 13 m | 0 | bajo |
| Carrer de Campoamor 30 | 18 m | 0 | bajo |
| Carrer del Consell de Cent 250 | 22 m | 0 | bajo |
| Carrer de Tuset 20 | 23 m | 0 | bajo |
| Carrer d'Aragó 300 | 32 m | 0 | bajo |
| Ronda del General Mitre 150 | 32 m | 0 | bajo |
| Passeig de Joan de Borbó Comte de Barcelona 50 | 81 m | 0 | bajo |
| Carrer de les Agudes 20 | 102 m | 0 | bajo |
<!-- picos:fin -->

## Qué aprendemos

1. **La nota separa bien los grupos.** Las calles "tranquilas" quedan abajo y las ruidosas arriba.
2. **Cambia el orden según la hora.** A la 1:00 encabezan las calles de ocio (Escudellers, Plaça del Sol, Nou de la Rambla). A las 13:00 encabezan las grandes vías de tráfico (Gran Via, Aragó, Ronda del General Mitre). En la nota global de todo el día sigue pesando más el tráfico, porque está presente las 24 horas. Por eso tiene sentido enseñar la curva por horas y no solo una cifra.
3. **El patio interior cambia mucho la experiencia.** La nota interior suele estar entre 50 y 80 puntos por debajo de la exterior. Hay excepciones: en Aragó 300 y Gran de Sant Andreu 200 la diferencia es mucho menor (25–36), porque su patio también es ruidoso. El informe debe distinguir siempre piso exterior e interior.
4. **El día de la semana importa sobre todo en las calles de ocio.** De la noche del lunes a la del viernes, Tuset (medido por su sensor) sube 33 puntos (de 60 a 93); Verdi, Plaça del Sol, Nou de la Rambla o Enric Granados, unos 15–18; Gran Via, Aragó, Sants o Ronda del General Mitre, solo 3–4.
5. **El mapa oficial acierta en las calles de tráfico, pero se queda corto en el ocio.** Comparado con 140 sensores (ver `validacion_sensores.md`): en los de tráfico la diferencia mediana de noche es de +0,9 dB; en los de ocio, +2,6 dB, con casos de +18 a +27 dB en calles pequeñas y plazas de Gràcia, el Born o Sant Antoni (Raspall, Puigmartí, Fonollar, Comte Borrell). Con 140 sensores y validación por distritos (`ocio_oculto.md`): de día y por la tarde, la cantidad de bares sí predice cuánto se queda corto el mapa, y se corrige en las zonas de bares; de noche ninguna pista pública lo predice, así que solo una medición lo resuelve.
6. **Consell de Cent confirma el efecto del eje verde.** El sensor de Consell de Cent 238 mide 6,6 dB menos de noche que el mapa 2017. Con la medición, su nota baja de 82 a 72.
7. **Barcelona es ruidosa de noche, y la escala ahora lo reparte.** Con la referencia de la OMS (45 dB de noche = 50 puntos), el 84 % de los portales salía "ruidoso" o "muy ruidoso" y ninguno bajaba de 33. Con la escala de extremos de Barcelona (octubre de 2026): 35 % tranquilo o muy tranquilo, 23 % moderado y 42 % ruidoso o muy ruidoso. Pega: las grandes avenidas quedan todas cerca de 100 (Gran Via, Aragó, Sants, Travessera 81).

## Limitaciones conocidas

- **Mapa de 2017**: no recoge los cambios posteriores. Donde hay sensor (Consell de Cent, por ejemplo) se corrige con la medición; en el resto, falta pasar al ráster de 2022.
- **Bandas de 5 dB**: el mapa no da cifras exactas, así que dos calles en la misma banda empatan.
- **Ubicación del portal**: la geolocalización a veces cae dentro de la manzana. En Blai y Gran de Sant Andreu el tramo está a más de 40 m (confianza baja).
- **Curva horaria**: fuera de los tramos con sensor, la forma por horas es la media medida de los sensores de su tipo, no la de cada calle.
- **Ocio infravalorado de noche**: en calles pequeñas y plazas con mucha vida nocturna, el mapa puede quedarse 10–25 dB corto de noche, y no hay forma fiable de detectarlo con datos públicos. De día y por la tarde se corrige en las zonas de bares.
- **Picos cortos** (camiones, gritos): los datos por hora no los ven. Hacen falta los datos minuto a minuto (pendiente).
- **Día de la semana**: pesos medidos en 2023; podrían cambiar con los años.

## Siguiente paso: validación

Para las calles de control (Tuset, Travessera de Gràcia y Martínez de la Rosa), el vecino puntúa de 0 a 100, de día y de noche, **sin mirar esta tabla**, y se compara con la nota calculada.
