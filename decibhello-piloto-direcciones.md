# DecibHello — Direcciones del piloto (Barcelona)

Estado: propuesta para revisar. Las 20 direcciones existen y se han geolocalizado con OpenStreetMap (Nominatim). La columna "Hipótesis" es lo que **esperamos** antes de mirar los datos: el piloto sirve para comprobar si la nota 0–100 (100 = muy ruidoso) confirma o desmiente cada hipótesis.

Criterios de selección:
- Los 10 distritos tienen al menos una dirección.
- Están los tipos de ruido que la nota debe distinguir: ocio nocturno, tráfico, turismo, ejes comerciales, calles pacificadas y zonas residenciales tranquilas.
- Se incluyen casos "trampa", donde la intuición puede fallar: calles peatonales con terrazas y supermanzanas.

## Ruidosas (hipótesis: nota alta)

| # | Dirección | Barrio / distrito | Tipo de ruido esperado |
|---|---|---|---|
| 1 | Carrer de Verdi, 20 | Vila de Gràcia, Gràcia | Ocio nocturno, cines y bares |
| 2 | Plaça del Sol, 12 | Vila de Gràcia, Gràcia | Terrazas y gente en la plaza de noche |
| 3 | Carrer Nou de la Rambla, 30 | Raval, Ciutat Vella | Ocio nocturno, turismo |
| 4 | Carrer dels Escudellers, 20 | Gòtic, Ciutat Vella | Ocio nocturno, turismo |
| 5 | Carrer de Blai, 20 | Poble-sec, Sants-Montjuïc | Bares de tapas, calle peatonal muy concurrida |
| 6 | Carrer d'Aragó, 300 | Eixample | Tráfico intenso en una vía de gran capacidad |
| 7 | Gran Via de les Corts Catalanes, 600 | Eixample | Tráfico intenso |
| 8 | Ronda del General Mitre, 150 | Sant Gervasi, Sarrià-Sant Gervasi | Tráfico de ronda en un distrito "tranquilo" |
| 9 | Passeig de Joan de Borbó, 50 | Barceloneta, Ciutat Vella | Turismo, terrazas, paseo marítimo |

## Intermedias o dudosas (hipótesis: nota media)

| # | Dirección | Barrio / distrito | Por qué es interesante |
|---|---|---|---|
| 10 | Carrer d'Enric Granados, 50 | Esquerra de l'Eixample | Calle pacificada, con poco tráfico pero muchas terrazas |
| 11 | Carrer del Parlament, 30 | Sant Antoni, Eixample | Terrazas y ambiente nocturno junto a la supermanzana de Sant Antoni |
| 12 | Carrer del Consell de Cent, 250 | Eixample | Eje verde pacificado: el mapa de 2017 es anterior al cambio |
| 13 | Rambla del Poblenou, 60 | Poblenou, Sant Martí | Rambla peatonal con terrazas |
| 14 | Carrer de Sants, 100 | Sants, Sants-Montjuïc | Eje comercial con tráfico |
| 15 | Carrer Gran de Sant Andreu, 200 | Sant Andreu | Eje comercial de barrio |

## Tranquilas (hipótesis: nota baja)

| # | Dirección | Barrio / distrito | Por qué |
|---|---|---|---|
| 16 | Carrer de Pomaret, 20 | Sant Gervasi, Sarrià-Sant Gervasi | Residencial en ladera, poco tráfico |
| 17 | Carrer de Pere II de Montcada, 10 | Pedralbes, Sarrià-Sant Gervasi | Residencial de baja densidad |
| 18 | Carrer de Campoamor, 30 | Horta, Horta-Guinardó | Calle residencial de barrio |
| 19 | Carrer de la Mare de Déu del Coll, 50 | El Coll, Gràcia | Residencial junto a la montaña |
| 20 | Carrer de les Agudes, 20 | Ciutat Meridiana, Nou Barris | Periferia junto a Collserola; comprobar si llega ruido de vías cercanas |

## Qué se calculará para cada dirección

1. Nivel del mapa de ruido de 2017 en el tramo de calle más cercano: día, tarde, noche y origen (tráfico, ocio, tren...).
2. Locales en un radio de 100 m: ocio nocturno y bares o restaurantes (censo 2024).
3. Pisos turísticos en un radio de 100 m.
4. Quejas por ruido en la calle en un radio de 100 m (IRIS 2025).
5. Distancia al sensor de ruido activo más cercano.
6. Nota 0–100 por franja y global, con su nivel de confianza.
