# DecibHello — Madrid o Valencia: qué ciudad tiene mejores datos

Investigación del 6 de octubre de 2026. Agente "Siguiente ciudad".

Todo lo que lleva una cifra se ha comprobado hoy, consultando la API o descargando el fichero. Lo que no se pudo comprobar dice **sin comprobar**. Ninguna fuente de Madrid ni de Valencia pidió captcha ni verificación anti-robots.

El informe completo, con el área metropolitana de Barcelona y los bloqueos, está en [siguiente-ciudad.md](siguiente-ciudad.md).

## Conclusión

**Madrid primero.** Pablo tenía razón, y ahora hay datos que lo respaldan.

| | Barcelona | **Madrid** | Valencia |
|---|---|---|---|
| Nota de datos (0–10) | 9,5 | **8** | 5 |

Las tres diferencias que más pesan:

1. **Locales de ocio.** Madrid tiene un censo de 203.701 locales con epígrafe y **horario de cierre**, y 6.591 terrazas con horario. Valencia no tiene censo de locales.
2. **Mapa de ruido.** Madrid tiene un ráster de 2021 con píxel de 5 m y dB exactos, que además distingue calle y patio. Valencia solo tiene manchas en franjas de 5 dB, y las recientes (2017 y 2022) no tienen licencia declarada.
3. **Sensores.** Ninguna de las dos publica datos por hora. Madrid tiene 31 estaciones repartidas por la ciudad, con un dato por franja y día desde 1998. Valencia tiene 16, todas en Russafa, desde 2020.

Cómo sale la nota: cada una de las 10 fuentes puntúa 1 si es como Barcelona o mejor, 0,5 si es parcial y 0 si no hay. Mapa, sensores y locales cuentan doble, porque mueven la noche (el 50 % de la nota). Total sobre 13, pasado a una escala de 10. En Valencia, los sensores cuentan 0,25 porque solo cubren un barrio.

## Tabla fuente a fuente

| # | Fuente | Barcelona | Madrid | Valencia |
|---|---|---|---|---|
| 1 | **Mapa de ruido** (Ld, Le, Ln) | **Sí**. Por tramo 2017 (17.958 tramos, franjas de 5 dB), vectorial por API. Ráster 2022 y fachadas 2017 | **Sí, mejor**. 2021 (fase 4). Ráster GeoTIFF, píxel de 5 m, dB exactos. [Descarga directa, 44,6 MB](https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/MEDIO_AMBIENTE/INFORMACION_ACUSTICA/Mapa_Estrategico_Ruido_2021/MER2021.zip). Solo tráfico. Licencia de la ficha sin comprobar (el portal es CC BY) | **Parcial**. Manchas de 5 dB. [Catálogo](https://opendata.vlci.valencia.es/dataset/mapa-soroll-nit-23-7h) = **2012** (CC BY). 2022: [geoportal `Laboratorio/MapaRuido`](https://geoportal.valencia.es/server/rest/services/Laboratorio/MapaRuido/MapServer), **sin licencia declarada**. Tráfico, tren e industria |
| 2 | **Sensores** | **Sí**. 176, por hora (2015–2023) y por minuto (desde 2024). ZIP con captcha | **Parcial**. [31 estaciones](https://datos.madrid.es/dataset/211346-0-estaciones-acusticas). [Diario por franja](https://datos.madrid.es/dataset/215885-0-contaminacion-ruido) desde 1998 hasta ayer (1.037.224 filas, con L10/L90). Descarga directa. **Sin datos por hora** | **Parcial (débil)**. 16 en Russafa, [diario por franja](https://opendata.vlci.valencia.es/dataset/t248679-daily) desde 2020 (32.291 filas). **Sin datos por hora**. Los 22 de ocio y los 12 de las ZAS no publican mediciones |
| 3 | **Portales** | **Sí**. 172.000 | **Sí**. [160.615 portales](https://datos.madrid.es/dataset/213605-0-callejero-oficial-madrid), semanal | **Sí**. [56.647](https://opendata.vlci.valencia.es/dataset/portals-dels-carrers-portales-de-las-calles), sin nombre de calle (se cruza con el código de vía) |
| 4 | **Locales y horarios de ocio** | **Sí**. 44.000 en planta baja, 212 de ocio nocturno; horarios en un dataset aparte | **Sí, mejor**. [Censo diario](https://datos.madrid.es/dataset/200085-0-censo-locales): 1.300 de ocio nocturno y 13.403 bares abiertos; horario en el censo; terrazas con horario | **No**. Solo terrazas contadas por barrio. OpenStreetMap: 262 bares, 208 pubs, 40 discotecas (ODbL) |
| 5 | **Obras en curso** | **Sí**. Polígonos, a diario | **Parcial**. [Informo](https://informo.madrid.es/informo/tmadrid/incid_aytomadrid.xml): 109 obras hoy, como puntos con fechas, en tiempo real. [17 obras grandes](https://datos.madrid.es/dataset/300538-0-obras-planificadas-ejecucion) con polígono | **Sí**. [Ocupación de vía pública](https://opendata.vlci.valencia.es/dataset/ocupacio-via-publica-ocupacion-via-publica): 385 obras activas, con calle, número y fechas, a diario |
| 6 | **Quejas por ruido** | **Sí**. IRIS con coordenadas | **Parcial**. [Sugerencias y reclamaciones](https://datos.madrid.es/dataset/300044-0-syrg-syrt): 7.060 de ruido desde 2023, con dirección en texto. [Inspecciones](https://datos.madrid.es/dataset/300172-0-inspecciones-ambientales): 1.626 de ruido en 2026. Avisa Madrid no tiene ruido | **Parcial**. [10.853 de ruido](https://opendata.vlci.valencia.es/dataset/total-castellano) (2020 a mayo de 2026), **solo por barrio** |
| 7 | **Pisos turísticos** | **Sí**. 10.721 con coordenadas | **Parcial**. [Comunidad](https://datos.comunidad.madrid/dataset/alojamientos_turisticos): 4.865, con dirección. [Ayuntamiento](https://datos.madrid.es/dataset/300694-0-viviendas-turisticas-geoportal): 1.037 ubicables | **Sí**. [GVA](https://dadesobertes.gva.es/dataset/tur-gestur-vt): 5.765, a diario, referencia catastral en el 90 % |
| 8 | **Exterior / interior** | **Sí**. Tramos de patio y fachadas | **Sí**. El propio ráster da nivel en los patios (≈35 dB frente a 55–67 dB en la calle) | **Parcial**. Hay que calcularlo con fachadas 1:500 (553.586 líneas) y manzanas |
| 9 | **Anchura de calle** | Estimada con portales | **Sí, mejor**. [Ancho de viario](https://datos.madrid.es/dataset/300715-0-ancho-viario-mapas) (30.267 tramos) y aceras | **Sí**. Bordillos y fachadas 1:500 |
| 10 | **Extras** | Recogida solo por quejas | **Sí**. ZPAE en polígono (4 zonas), tráfico cada 15 min desde 2013 en 5.083 puntos, 44.252 contenedores. Sin horarios de recogida | **Parcial**. 5 polígonos de ZAS (falta Russafa), 23.057 contenedores, tráfico sin histórico. Sin horarios de recogida |
| | **Licencia** | CC BY 4.0 | CC BY 4.0 (comprobado en la API) | CC BY 4.0 en el catálogo; mapas 2017/2022 sin declarar |
| | **Acceso** | API CKAN con SQL; ZIP con captcha | API CKAN + descargas directas, sin captcha | API CKAN sin SQL + geoportal ArcGIS (2.000 registros por consulta), sin captcha |

## Qué se copia de Barcelona y qué hay que adaptar (Madrid)

Las reglas del modelo no cambian: nota 0–100 lineal (día y tarde 45→75 dB, noche 35→70 dB), franjas 7–19, 19–23 y 23–7, global 30/20/50, y todo entra como dB validados con sensores.

**Se copia tal cual**
- La fórmula de la nota, las franjas, los pesos y la compresión de los extremos.
- El visor y el buscador (cambiando los datos).
- La regla de obras (+2 dB a menos de 25 m de día laborable) y el aviso de picos nocturnos.

**Se adapta**
1. **Índice de portales**: leer el ráster justo delante de la fachada en lugar de buscar el tramo. Si cae en un patio, nota "interior". Es más simple que en Barcelona.
2. **Forma por hora**: usar la de Barcelona dentro de cada franja, como ya se hace. La media de cada franja sigue saliendo del mapa de Madrid. Comprobarla con el tráfico cada 15 minutos y con los L10/L90 de Madrid.
3. **Pesos por día de la semana**: sacarlos de los datos diarios de Madrid. Antes hay que aclarar si la noche del sábado se apunta al sábado o al domingo (sin comprobar).
4. **Suma por bares**: el mapa de Madrid no incluye el ocio, así que hay que recalcular los coeficientes con las 31 estaciones. Pocas están en calles de ocio, así que la validación será más débil que en Barcelona. Hasta tener más mediciones, el visor lo mostrará con confianza más baja.
5. **Horarios de ocio**: leerlos del censo de locales.
6. **Obras**: puntos de Informo en lugar de polígonos.
7. **Quejas y pisos turísticos**: geocodificar con el callejero.

**Pedir por transparencia** (Ayuntamiento de Madrid)
- Datos por hora o por minuto de las 31 estaciones, de 2023 a hoy.
- Horarios de recogida de basura y limpieza por calle.

**Valencia necesitaría pedir**: datos por hora de todos los sonómetros (16 de Russafa, 22 de ocio, 12 de las ZAS), el censo de licencias de hostelería y ocio con dirección y horario, las quejas de ruido con dirección y la licencia de los mapas de 2017 y 2022. Sin el censo de locales, el piloto no puede funcionar como el de Barcelona.

## Estimación de trabajo para un piloto como el de Barcelona

Estimación orientativa en días de trabajo de un agente, con revisión de Pablo. Sin comprobar en la práctica.

| Tarea | Madrid | Valencia |
|---|---|---|
| Índice de portales con mapa y exterior/interior | 3–4 días | 5–7 días (manchas + cálculo de patios con fachadas) |
| Locales, bares y horarios | 2–3 días | Bloqueado hasta tener datos (OpenStreetMap como apaño: 3 días) |
| Sensores: pesos por día, validación del mapa y de la suma por bares | 4–5 días | 3–4 días (un solo barrio) |
| Obras, quejas y pisos turísticos | 3 días | 3 días |
| Visor, buscador y pruebas (móvil y escritorio) | 3–4 días | 3–4 días |
| **Total** | **≈ 3–4 semanas** | **≈ 4–5 semanas + esperar la respuesta de transparencia (plazo legal de un mes)** |

## Qué necesito de Pablo

1. Confirmar Madrid como siguiente ciudad, teniendo en cuenta también la votación de la web.
2. Enviar la solicitud de transparencia al Ayuntamiento de Madrid (datos por hora de las 31 estaciones y horarios de recogida). Si quiere, preparo el borrador.
3. Para Madrid no hace falta descargar nada a mano: todo se baja de forma automática.
