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
6. **Día de la semana (supuesto v0)**: el mapa oficial es una media anual. Para cada día se reparte con pesos semanales, que conservan esa media:
   - el tráfico baja de día el fin de semana y sube de noche el viernes y el sábado;
   - el ocio nocturno y los focos son mucho más fuertes de jueves a sábado (de lunes a viernes, unas 5 veces más energía a la 1:00);
   - el ruido de noche no atribuido a ninguna fuente sigue la mezcla de tráfico y ocio de la calle.

   Los pesos son una estimación inicial y hay que calibrarlos con los datos por hora de los sensores municipales.
7. **Notas por franja** = media de sus horas. **Nota global** = 30 % día + 20 % tarde + 50 % noche.
8. **Confianza**:
   - alta: hay sensor a menos de 150 m;
   - media: no hay sensor cerca;
   - baja: el tramo encontrado está a más de 40 m o no coincide con la calle.

El visor interactivo (`visor.html`) tiene un buscador para cualquier portal de Barcelona (dirección o enlace de Google Maps) y muestra la curva de 24 horas, exterior e interior, y la calle tramo a tramo. Usa una copia en JavaScript de `modelo.py`; da las mismas notas que este informe.

## Resultados

<!-- tabla:inicio -->
| Nota | Día | Tarde | Noche | Interior | Dirección | Hipótesis | Ruido noche (mapa) | Ocio / bares / quejas / HUT (100 m) | Confianza |
|---|---|---|---|---|---|---|---|---|---|
| 84 | 83 | 85 | 84 | 68 | Carrer d'Aragó 300 | ruidosa | 65–70 | 0 / 7 / 1 / 5 | alta |
| 84 | 83 | 85 | 85 | 45 | Gran Via de les Corts Catalanes 600 | ruidosa | 65–70 | 0 / 21 / 0 / 43 | media |
| 84 | 78 | 86 | 87 | 60 | Travessera de Gràcia 81 | control | 65–70 | 1 / 13 / 8 / 4 | alta |
| 83 | 78 | 85 | 85 | — | Carrer de Sants 100 | intermedia | 65–70 | 0 / 17 / 4 / 4 | media |
| 82 | 78 | 84 | 84 | 48 | Ronda del General Mitre 150 | ruidosa | 65–70 | 0 / 2 / 2 / 2 | media |
| 82 | 78 | 84 | 84 | 43 | Carrer del Consell de Cent 250 | intermedia | 65–70 | 0 / 14 / 0 / 18 | media |
| 81 | 78 | 83 | 82 | 35 | Travessera de Gràcia 150 | control | 60–65 | 1 / 29 / 3 / 50 | alta |
| 78 | 63 | 81 | 86 | 39 | Carrer d'Escudellers 20 | ruidosa | 65–70 | 3 / 45 / 12 / 43 | alta |
| 78 | 63 | 80 | 86 | 48 | Carrer de Tuset 20 | control | 65–70 | 7 / 26 / 3 / 4 | alta |
| 77 | 71 | 79 | 79 | 37 | Travessera de Gràcia 300 | control | 60–65 | 0 / 7 / 0 / 25 | media |
| 74 | 54 | 79 | 84 | 46 | Plaça del Sol 12 | ruidosa | 65–70 | 3 / 29 / 2 / 16 | alta |
| 74 | 63 | 75 | 81 | 43 | Carrer d'Enric Granados 50 | intermedia | 60–65 | 0 / 13 / 1 / 53 | alta |
| 74 | 63 | 79 | 79 | 35 | Carrer de Martínez de la Rosa 20 | control | 55–60 | 3 / 27 / 5 / 57 | media |
| 73 | 62 | 73 | 80 | 31 | Carrer Nou de la Rambla 30 | ruidosa | 60–65 | 1 / 21 / 5 / 44 | media |
| 72 | 63 | 76 | 76 | 48 | Carrer del Parlament 30 | intermedia | 55–60 | 0 / 25 / 5 / 57 | alta |
| 72 | 71 | 74 | 73 | 56 | Carrer Gran de Sant Andreu 200 | intermedia | 55–60 | 0 / 2 / 5 / 0 | media |
| 71 | 55 | 76 | 79 | 31 | Carrer de Verdi 20 | ruidosa | 60–65 | 0 / 35 / 8 / 26 | alta |
| 71 | 63 | 75 | 74 | 35 | Rambla del Poblenou 60 | intermedia | 55–60 | 0 / 12 / 6 / 5 | alta |
| 69 | 54 | 70 | 78 | 35 | Carrer de Blai 20 | ruidosa | 60–65 | 0 / 31 / 4 / 51 | alta |
| 69 | 63 | 72 | 72 | 45 | Carrer de la Mare de Déu del Coll 50 | tranquila | 55–60 | 0 / 0 / 2 / 3 | media |
| 64 | 54 | 67 | 68 | — | Passeig de Joan de Borbó Comte de Barcelona 50 | ruidosa | 50–55 | 0 / 15 / 13 / 10 | media |
| 62 | 62 | 63 | 62 | — | Carrer de Campoamor 30 | tranquila | 50–55 | 0 / 0 / 0 / 0 | media |
| 60 | 54 | 62 | 62 | — | Carrer de Pere II de Montcada 10 | tranquila | 50–55 | 0 / 0 / 0 / 0 | media |
| 60 | 54 | 63 | 63 | — | Carrer de les Agudes 20 | tranquila | 50–55 | 0 / 0 / 1 / 0 | media |
| 46 | 46 | 47 | 46 | — | Carrer de Pomaret 20 | tranquila | 40–45 | 0 / 0 / 1 / 0 | media |
<!-- tabla:fin -->

## La noche según el día de la semana

Nota media de la noche (23–7 h) que empieza cada día: la del viernes va del viernes a las 23:00 al sábado a las 7:00. Ordenado por la diferencia entre viernes y lunes.

<!-- semana:inicio -->
| Dirección | Lun | Mar | Mié | Jue | Vie | Sáb | Dom | Vie − lun |
|---|---|---|---|---|---|---|---|---|
| Carrer de Verdi 20 | 71 | 73 | 75 | 81 | 84 | 84 | 74 | +13 |
| Plaça del Sol 12 | 77 | 79 | 81 | 86 | 89 | 89 | 80 | +12 |
| Carrer Nou de la Rambla 30 | 73 | 74 | 77 | 82 | 85 | 85 | 76 | +12 |
| Carrer de Blai 20 | 71 | 72 | 75 | 80 | 83 | 83 | 74 | +12 |
| Carrer de Martínez de la Rosa 20 | 73 | 74 | 76 | 81 | 85 | 85 | 74 | +12 |
| Passeig de Joan de Borbó Comte de Barcelona 50 | 63 | 64 | 65 | 70 | 74 | 74 | 64 | +11 |
| Carrer d'Escudellers 20 | 80 | 81 | 84 | 88 | 90 | 90 | 82 | +10 |
| Carrer del Parlament 30 | 71 | 72 | 73 | 77 | 81 | 81 | 72 | +10 |
| Rambla del Poblenou 60 | 69 | 69 | 71 | 76 | 79 | 79 | 70 | +10 |
| Carrer de Tuset 20 | 80 | 81 | 83 | 87 | 89 | 89 | 82 | +9 |
| Carrer d'Enric Granados 50 | 76 | 77 | 78 | 82 | 84 | 84 | 77 | +8 |
| Travessera de Gràcia 150 | 78 | 79 | 80 | 84 | 86 | 86 | 79 | +8 |
| Carrer Gran de Sant Andreu 200 | 70 | 70 | 71 | 74 | 77 | 77 | 70 | +7 |
| Carrer de Pomaret 20 | 43 | 44 | 45 | 47 | 49 | 50 | 44 | +6 |
| Travessera de Gràcia 81 | 84 | 84 | 85 | 88 | 90 | 90 | 84 | +6 |
| Carrer del Consell de Cent 250 | 82 | 82 | 83 | 85 | 87 | 87 | 83 | +5 |
| Carrer de Sants 100 | 83 | 83 | 84 | 86 | 88 | 88 | 83 | +5 |
| Carrer de la Mare de Déu del Coll 50 | 70 | 70 | 70 | 72 | 75 | 75 | 69 | +5 |
| Carrer de les Agudes 20 | 61 | 61 | 62 | 63 | 66 | 66 | 61 | +5 |
| Travessera de Gràcia 300 | 77 | 77 | 78 | 80 | 82 | 82 | 77 | +5 |
| Gran Via de les Corts Catalanes 600 | 83 | 83 | 84 | 85 | 87 | 87 | 83 | +4 |
| Carrer d'Aragó 300 | 83 | 83 | 83 | 85 | 86 | 87 | 83 | +3 |
| Ronda del General Mitre 150 | 83 | 83 | 83 | 85 | 86 | 86 | 83 | +3 |
| Carrer de Pere II de Montcada 10 | 61 | 61 | 61 | 62 | 63 | 64 | 60 | +2 |
| Carrer de Campoamor 30 | 61 | 61 | 61 | 62 | 63 | 64 | 60 | +2 |
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
| Carrer de Martínez de la Rosa 20 | 8 m | 5 | alto |
| Carrer de Verdi 20 | 10 m | 2 | alto |
| Carrer Nou de la Rambla 30 | 11 m | 1 | alto |
| Carrer Gran de Sant Andreu 200 | 14 m | 5 | alto |
| Travessera de Gràcia 150 | 8 m | 0 | medio |
| Carrer de Blai 20 | 12 m | 3 | medio |
| Carrer de Pomaret 20 | 12 m | 1 | medio |
| Carrer de la Mare de Déu del Coll 50 | 13 m | 1 | medio |
| Carrer d'Enric Granados 50 | 22 m | 1 | medio |
| Carrer del Parlament 30 | 22 m | 3 | medio |
| Rambla del Poblenou 60 | 22 m | 3 | medio |
| Travessera de Gràcia 81 | 23 m | 4 | medio |
| Carrer de Sants 100 | 24 m | 1 | medio |
| Plaça del Sol 12 | 25 m | 1 | medio |
| Gran Via de les Corts Catalanes 600 | — | 0 | bajo |
| Carrer de Pere II de Montcada 10 | 13 m | 0 | bajo |
| Carrer de Campoamor 30 | 18 m | 0 | bajo |
| Carrer del Consell de Cent 250 | 22 m | 0 | bajo |
| Carrer de Tuset 20 | 23 m | 0 | bajo |
| Travessera de Gràcia 300 | 23 m | 0 | bajo |
| Carrer d'Aragó 300 | 32 m | 0 | bajo |
| Ronda del General Mitre 150 | 32 m | 0 | bajo |
| Passeig de Joan de Borbó Comte de Barcelona 50 | 81 m | 0 | bajo |
| Carrer de les Agudes 20 | 102 m | 0 | bajo |
<!-- picos:fin -->

## Qué aprendemos

1. **La nota separa bien los grupos.** Las calles "tranquilas" quedan abajo y las ruidosas arriba.
2. **Cambia el orden según la hora.** A la 1:00 encabezan las calles de ocio (Escudellers, Plaça del Sol, Nou de la Rambla, Verdi). A las 13:00 encabezan las grandes vías de tráfico (Gran Via, Aragó). En la nota global de todo el día sigue pesando más el tráfico, porque está presente las 24 horas. Por eso tiene sentido enseñar la curva por horas y no solo una cifra.
3. **El patio interior cambia mucho la experiencia.** La nota interior suele estar entre 25 y 45 puntos por debajo de la exterior. Hay excepciones: en Aragó 300 y Gran de Sant Andreu 200 la diferencia es de solo 16, porque su patio también es ruidoso. El informe debe distinguir siempre piso exterior e interior.
4. **El día de la semana importa sobre todo en las calles de ocio.** De la noche del lunes a la del viernes, Verdi, Plaça del Sol, Nou de la Rambla o Blai suben 12–13 puntos; Gran Via, Aragó o Ronda del General Mitre, solo 3–4. Con pesos supuestos: hay que confirmarlo con los sensores.
5. **Barcelona es ruidosa de noche.** Con la referencia de la OMS (45 dB = 50 puntos), casi ninguna fachada a la calle baja de 50. Es coherente con los datos (el 76 % de los tramos supera 45 dB de noche), pero quizá convenga una escala relativa a Barcelona además de la absoluta.

## Limitaciones conocidas

- **Mapa de 2017**: no recoge los cambios posteriores. Consell de Cent es hoy un eje verde con mucho menos tráfico; su 87 seguramente está sobrevalorado.
- **Bandas de 5 dB**: el mapa no da cifras exactas, así que dos calles en la misma banda empatan.
- **Ubicación del portal**: la geolocalización a veces cae dentro de la manzana. En Blai y Gran de Sant Andreu el tramo está a más de 40 m (confianza baja).
- **Curva horaria estimada**: la forma por horas es un perfil típico, no medido en cada calle. Las mediciones de los sensores (minuto a minuto desde 2024) servirán para sustituirlo, pero su descarga está detrás de una verificación anti-bots.
- **Día de la semana**: los pesos semanales son supuestos, no medidos en Barcelona todavía.

## Siguiente paso: validación

Para las calles de control (Tuset y Travessera de Gràcia), el vecino puntúa de 0 a 100, de día y de noche, **sin mirar esta tabla**, y se compara con la nota calculada.
