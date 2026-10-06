# DecibHello — Siguiente ciudad: Madrid, Valencia o el área metropolitana

Investigación del 6 de octubre de 2026. Agente "Siguiente ciudad".

Todo lo que lleva una cifra se ha comprobado hoy: consultando la API o descargando el fichero (o un trozo). Lo que no se pudo comprobar dice **sin comprobar**. Ninguna fuente pidió captcha ni verificación anti-robots. Algunas webs bloquearon la conexión por red o por IP; están en la sección 6, con lo que habría que descargar a mano.

La comparación centrada solo en Madrid y Valencia, con la nota de 0 a 10 y la estimación de trabajo, está en [siguiente-ciudad-madrid-valencia.md](siguiente-ciudad-madrid-valencia.md).

## 1. Conclusión

**La siguiente ciudad debería ser Madrid.**

- Tiene casi todo lo que usa Barcelona, y en algunas cosas más: mapa de ruido de 2021 en dB exactos cada 5 m, censo de locales **con horario**, terrazas con horario y anchura de calle medida.
- Su gran hueco: los sensores **no publican datos por hora**. Solo publican un dato por franja (día, tarde y noche) y por día, desde 1998 hasta ayer. Con eso salen los pesos por día de la semana, pero no la forma de cada hora.
- Valencia queda lejos: no tiene censo de locales, su mapa son manchas de 5 dB y solo hay 16 sensores, todos en Russafa y con un dato al día.
- El área metropolitana tiene un mapa de ruido muy bueno (de la Generalitat, por tramo de calle) y está pegada a Barcelona, pero le faltan bares, obras y quejas. Sirve para **ampliar Barcelona** a L'Hospitalet y Badalona más adelante, no como "siguiente ciudad" con el mismo nivel de detalle.

| | Barcelona (referencia) | **Madrid** | Valencia | L'Hospitalet + Badalona | Sant Cugat |
|---|---|---|---|---|---|
| Nota de datos (0–10) | 9,5 | **8** | 5 | 3,5 | 1 |

Cómo sale la nota, con las 10 fuentes de la tabla de la sección 2:
- Cada fuente puntúa 1 si es como Barcelona o mejor, 0,5 si es parcial o pide trabajo extra, y 0 si no hay.
- Mapa, sensores y locales cuentan doble, porque son los que mueven la noche (el 50 % de la nota).
- Total sobre 13 puntos, pasado a una escala de 10. Barcelona pierde medio punto porque su mapa por tramo es de 2017 y va en franjas de 5 dB.
- Valencia: los sensores cuentan 0,25 porque solo cubren un barrio. Área metropolitana: Badalona y L'Hospitalet juntos (el mapa cuenta 0,75).

## 2. Tabla comparativa

Leyenda: **sí** = equivalente a Barcelona o mejor; **parcial** = existe pero falta algo; **no** = no hay en abierto.

| Fuente | Barcelona | Madrid | Valencia | Área metropolitana (L'H, Badalona, Sant Cugat) |
|---|---|---|---|---|
| 1. Mapa de ruido | Por tramo 2017, franjas de 5 dB; ráster 2022; fachadas 2017 | **Sí, mejor**: ráster 2021 de 5 m, dB exactos, Ld/Le/Ln/Lden. Solo tráfico | **Parcial**: manchas de 5 dB (2012, 2017, 2022). Las de 2017 y 2022 sin licencia declarada | **Sí** en Badalona (tramos 2018 en dB exactos) · **parcial** en L'H (tramos 2012 + manchas 2022) · **no** en Sant Cugat |
| 2. Sensores por hora | 176, por hora y por minuto | **Parcial**: 31, un dato por franja y día desde 1998 | **Parcial**: 16 en Russafa, un dato por franja y día desde 2020 | **No**: solo el último valor; el histórico pide clave |
| 3. Portales con coordenadas | 172.000 | **Sí**: 160.615 | **Sí**: 56.647 (sin nombre de calle; se cruza) | **Sí**: L'H 23.024 · Badalona 28.242 · Sant Cugat 13.968 |
| 4. Locales y horarios de ocio | 44.000 locales, 212 de ocio nocturno; horarios aparte | **Sí, mejor**: 203.701 locales, 1.300 de ocio nocturno, horario en el censo, 6.591 terrazas con horario | **No** (solo OpenStreetMap: 40 discotecas, 262 bares) | **No** |
| 5. Obras en curso | Polígonos, a diario | **Parcial**: puntos con fechas (Informo), a diario | **Sí**: puntos y tramos con fechas, a diario | **No** |
| 6. Quejas por ruido | IRIS con coordenadas | **Parcial**: 7.060 con dirección en texto (sin coordenadas) | **Parcial**: 10.853, solo por barrio | **No** (L'H: 8 incidencias de limpieza por "Soroll") |
| 7. Pisos turísticos | 10.721 con coordenadas | **Parcial**: 4.865 (Comunidad) con dirección; 1.037 con licencia y ubicables | **Sí**: 5.765 con referencia catastral (90 %) | **Parcial**: L'H con coordenadas (707); resto solo dirección |
| 8. Exterior / interior | Tramos de patio y mapa de fachadas | **Sí**: el ráster da nivel en los patios (≈35 dB frente a 55–67 en la calle) | **Parcial**: se puede calcular con fachadas 1:500 y manzanas | **Parcial**: material en Badalona; catastro bloqueado |
| 9. Anchura de calle | Estimada con portales | **Sí, mejor**: ancho de calzada (30.267 tramos) y de aceras | **Sí**: bordillos y fachadas 1:500 | **Parcial**: anchura de aceras en Badalona; resto, con portales |
| 10. Extras | Recogida (solo quejas), tráfico por tramo | Zonas ZPAE en polígono, tráfico cada 15 min desde 2013, 44.252 contenedores | Zonas ZAS (5 polígonos), 23.057 contenedores, tráfico sin histórico | Mapa de capacidad acústica; contenedores en L'H |
| Licencia | CC BY 4.0 | CC BY 4.0 (comprobado en la API) | CC BY 4.0 (catálogo); mapas 2017/2022 sin declarar | Generalitat: "Avís legal" (sin confirmar CC BY); L'H: CC BY-ND (**no permite obras derivadas**) |
| Acceso | API CKAN; ZIP con captcha | API CKAN + descargas directas, sin captcha | API CKAN (sin SQL) + geoportal ArcGIS, sin captcha | WFS de la Generalitat, CKAN de la AOC, geoservidores municipales |

## 3. Madrid

Portal: [datos.madrid.es](https://datos.madrid.es) (API CKAN, `datastore_search` funciona). Geoportal: [geoportal.madrid.es](https://geoportal.madrid.es). Licencia **CC BY 4.0**, la misma que Barcelona (`license_id: cc-by`, comprobado).

### 3.1 Mapa estratégico de ruido 2021

- [Ficha](https://geoportal.madrid.es/IDEAM_WBGEOPORTAL/dataset.iam?id=470b89af-5d64-41d3-8bdb-2fe6badd0364) · [descarga directa, 44,6 MB](https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/MEDIO_AMBIENTE/INFORMACION_ACUSTICA/Mapa_Estrategico_Ruido_2021/MER2021.zip) (HTTP 200).
- Fase 4, aprobado en febrero de 2023. Cuatro GeoTIFF: Ld, Le, Ln y Lden.
- Píxel de **5 m**, valores en dB **continuos** (no franjas). Los edificios valen 0.
- Los **patios de manzana tienen valor propio**. En Gaztambide: 55–71 dB en la calle de noche y 35–38 dB en el patio. Así se separa exterior de interior sin otra capa.
- Contraste con las 30 estaciones de 2021: el mapa da 1,1 dB menos de día y 1,9 dB menos de noche, con una dispersión de 4–5 dB. Parecido a lo que vimos en Barcelona.
- **Solo cuenta el tráfico** ([memoria](https://www.madrid.es/UnidadesDescentralizadas/Sostenibilidad/Ruido/MapaRuido/MapaRuido2021/Ficheros/MemoriaMER2021.pdf)). No hay ocio, a diferencia del mapa de Barcelona (`OCI_N`).
- No hay versión por tramo ni por fachada, ni servicio WMS.
- Mapa de 2016 también descargable ([MER2016.zip](https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/MEDIO_AMBIENTE/INFORMACION_ACUSTICA/Mapa_Estrategico_Ruido_2016/MER2016.zip), píxel de 10 m).
- Sin comprobar: la licencia escrita en la ficha del mapa y la altura de cálculo.

### 3.2 Sensores

- [31 estaciones fijas](https://datos.madrid.es/dataset/211346-0-estaciones-acusticas) con coordenadas. Ojo: la longitud y la latitud traen puntos de miles; mejor usar X/Y.
- [Datos diarios](https://datos.madrid.es/dataset/215885-0-contaminacion-ruido): [`Ruido_diario_acumulado.csv`](https://www.madrid.es/UnidadesDescentralizadas/Sostenibilidad/Ruido/Publicaciones/Ruido_diario_acumulado.csv), 1.037.224 filas, de noviembre de 1998 al 5 de octubre de 2026. Columnas: estación, año, mes, día, franja (D, E, N, T), LAeq, L1, L10, L50, L90 y L99. Se actualiza a diario (no en fines de semana ni festivos).
- [Datos mensuales](https://datos.madrid.es/dataset/211356-0-contaminacion-acustica) con Ld, Le y Ln.
- **No hay datos por hora publicados.** La red mide en tiempo real desde 2021, pero no se publica.
- Sí salen **perfiles por día de la semana y franja**. Ejemplo, Plaza del Carmen de noche (2025): lunes 57,3 dB, sábado 61,6 dB, domingo 62,3 dB.
- Los L10 y L90 diarios dan una idea de los picos, algo que en Barcelona aún no usamos.
- Sin comprobar: si la noche del sábado se apunta al sábado o al domingo. Hay que deducirlo (por ejemplo, con Nochevieja) antes de calcular los pesos por día.
- Están sobre todo en avenidas y plazas. Pocas en calles de ocio (Plaza del Carmen, Plaza de España).

### 3.3 Portales

- [Callejero oficial](https://datos.madrid.es/dataset/213605-0-callejero-oficial-madrid), actualización semanal: 214.697 direcciones, **160.615 portales**, todas con coordenadas.
- La clave `COD_NDP` enlaza con el censo de locales y con los pisos turísticos con licencia.

### 3.4 Locales, ocio nocturno y horarios

- [Censo de locales](https://datos.madrid.es/dataset/200085-0-censo-locales), actualización diaria: 203.701 locales con coordenadas y 225.751 actividades con epígrafe.
- Ocio nocturno abierto: **1.300 locales** (discotecas, bares especiales, salas de fiesta, café espectáculo). Bares: 13.403.
- **Horario de apertura y cierre en el propio censo** (relleno en 32.516 locales; 448 de ocio nocturno, con cierre típico a las 5:30 o a las 3:00).
- **6.591 terrazas** con horario de lunes a jueves y de viernes y sábado.
- Mejor que Barcelona, donde el censo es solo de planta baja y los horarios van aparte.

### 3.5 Obras

- [Incidencias de Informo](https://informo.madrid.es/informo/tmadrid/incid_aytomadrid.xml): hoy 111, de ellas 109 de obras, con punto, fecha de inicio y de fin. Se actualiza continuamente.
- [Obras públicas grandes](https://datos.madrid.es/dataset/300538-0-obras-planificadas-ejecucion): solo 17, con polígono.
- Frente a Barcelona: son puntos, no polígonos. La regla de "+2 dB a menos de 25 m" se puede aplicar, pero habrá que revisar la distancia.

### 3.6 Quejas

- [Avisa Madrid](https://datos.madrid.es/dataset/212411-0-madrid-avisa): 430.596 avisos con coordenadas, pero **ninguno de ruido**.
- [Sugerencias y reclamaciones](https://datos.madrid.es/dataset/300044-0-syrg-syrt) desde 2023: **7.060 de ruido** (4.272 por maquinaria de limpieza, 667 por camión de basura, 562 por eventos, 222 de noche en la calle, 198 por locales). Con **dirección en texto** en 5.295, sin coordenadas: hay que cruzarlas con el callejero.
- [Inspecciones ambientales](https://datos.madrid.es/dataset/300172-0-inspecciones-ambientales) de 2026: 1.626 de ruido, con dirección.
- Las quejas por limpieza y camión son el equivalente al aviso de "recogida" de Barcelona.

### 3.7 Pisos turísticos

- [Comunidad de Madrid](https://datos.comunidad.madrid/dataset/alojamientos_turisticos): 4.865 en la ciudad, con dirección y sin coordenadas. CC BY.
- [Ayuntamiento](https://datos.madrid.es/dataset/300694-0-viviendas-turisticas-geoportal): unas 1.037 con licencia, ubicables por `COD_NDP`.
- Peor que Barcelona: menos pisos registrados y hay que geocodificar.

### 3.8 Anchura de calle

- [Ancho medio de viario](https://datos.madrid.es/dataset/300715-0-ancho-viario-mapas): 30.267 tramos con rango de números. Parece ancho de calzada (Gaztambide 7,4 m, Princesa 12,5 m).
- Ancho de aceras: 91.403 polígonos. Calzada + aceras ≈ fachada a fachada (cálculo pendiente).

### 3.9 Extras

- **ZPAE** (zonas de protección acústica especial) en polígono: Centro, Gaztambide, Trafalgar-Ríos Rosas y AZCA. La clasificación por grado está sin comprobar.
- **Tráfico cada 15 minutos desde 2013** ([histórico](https://datos.madrid.es/dataset/208627-0-transporte-ptomedida-historico)) en 5.083 puntos. Da la forma horaria del tráfico calle a calle. Puede suplir en parte la falta de sensores por hora.
- [Contenedores](https://datos.madrid.es/dataset/300276-0-contenedor-papel-carton-todos): 44.252 con coordenadas (7.659 de vidrio). Horarios de recogida: no publicados.

### 3.10 Qué falta frente a Barcelona

1. **Ruido por hora**: pedirlo por transparencia o modelarlo (ver sección 7).
2. **Ocio en el mapa**: el mapa solo cuenta el tráfico; el ocio tiene que entrar entero por la suma de bares. Hay que recalibrarla, y con 31 estaciones (pocas en calles de ocio) la validación será más débil.
3. **Quejas y pisos turísticos con coordenadas**: hay que geocodificar.
4. **Horarios de recogida**: igual que en Barcelona, no publicados.

## 4. Valencia

Portal: [opendata.vlci.valencia.es](https://opendata.vlci.valencia.es) (CKAN, 279 conjuntos; `datastore_search` sí, `datastore_search_sql` **no**). Casi todo lo geográfico está en el geoportal ArcGIS (`https://geoportal.valencia.es/server/rest/services/OPENDATA/...`), sin clave, 2.000 registros por consulta. El antiguo valencia.opendatasoft.com ya no existe (404). Licencia **CC BY 4.0** en el catálogo.

- **Mapa de ruido**: solo manchas (isófonas) en franjas de 5 dB, sin tramos ni fachadas.
  - El ["Mapa Ruido" del catálogo](https://opendata.vlci.valencia.es/dataset/mapa-soroll-nit-23-7h) es el de **2012** (geometría idéntica a la del servicio de 2012) y su leyenda de noche está mal.
  - 2022 (fase 4): [`Laboratorio/MapaRuido`](https://geoportal.valencia.es/server/rest/services/Laboratorio/MapaRuido/MapServer). 2017: [`Laboratorio/MapaRuido2022`](https://geoportal.valencia.es/server/rest/services/Laboratorio/MapaRuido2022/MapServer) (el nombre está cruzado). Fuera del catálogo y **sin licencia declarada**.
  - Separados por tráfico, tren e industria. No hay ocio. Por debajo de 55 dB de día (50 de noche) no hay mancha.
  - En un sensor de Russafa, el mapa de 2022 da 60–65 dB de noche y el sensor mide 55,2 dB de mediana.
- **Sensores**: 16 en Russafa, un dato por franja y día desde 2020 ([ejemplo](https://opendata.vlci.valencia.es/dataset/t248679-daily); 32.291 filas). Sale el perfil por día de la semana (en Cura Femenía, noche entre semana ≈ 51 dB, viernes y sábado 63–66 dB). **No hay por hora.** Los 22 sonómetros de ocio (Cánovas, Cedro, Honduras, Benimaclet, Polo y Peyrolón) y los 12 de las zonas ZAS no publican mediciones.
- **Portales**: [56.647 con coordenadas](https://opendata.vlci.valencia.es/dataset/portals-dels-carrers-portales-de-las-calles), sin nombre de calle (se cruza con el código de vía).
- **Locales**: **no hay censo** de locales ni de licencias. Solo recibos de terrazas por barrio. OpenStreetMap: 262 bares, 208 pubs, 40 discotecas (licencia ODbL).
- **Obras**: [ocupaciones de vía pública](https://opendata.vlci.valencia.es/dataset/ocupacio-via-publica-ocupacion-via-publica): 653 activas (385 de obras), con calle, número y fechas, a diario. Equivalente a Barcelona.
- **Quejas**: [176.051 quejas](https://opendata.vlci.valencia.es/dataset/total-castellano) de 2020 a mayo de 2026, 10.853 de ruido. **Solo por barrio.**
- **Pisos turísticos**: [registro de la Generalitat Valenciana](https://dadesobertes.gva.es/dataset/tur-gestur-vt), 5.765 en València, a diario, con referencia catastral en el 90 % (se ubican cruzando con las parcelas).
- **Patios y anchura**: no hay capa directa, pero sí fachadas a escala 1:500 (553.586 líneas), bordillos y manzanas. Se pueden calcular con más precisión que en Barcelona.
- **Extras**: 5 polígonos de ZAS (Carmen, Xúquer, Woody, Juan Llorens; Russafa no aparece); 23.057 contenedores; tráfico solo con el último valor.

**Qué falta frente a Barcelona**: censo de locales y horarios, sensores por hora (y fuera de Russafa), mapa por tramo y quejas con ubicación. Para tres de esas cuatro cosas hay que pedir datos por transparencia.

## 5. Área metropolitana de Barcelona

### 5.1 La fuente común: la Generalitat

El servicio [`sig.gencat.cat/ows/ATMOSFERA/wfs`](https://sig.gencat.cat/ows/ATMOSFERA/wfs?service=WFS&request=GetCapabilities) responde sin captcha, en GeoJSON y con filtros.

- **Tramos de calle de 2018 en dB exactos** (`ATMOSFERA_MES_SUPRAMUN_2018`): Ld, Le, Ln y Lden, separados por tráfico, tren, avión, industria y **ocio**. Badalona 2.967 tramos (comprobado), Santa Coloma 822, Sant Adrià 482, Cornellà 1.138, Terrassa 4.674, Sabadell 4.727 y **Barcelona 17.947**. Al incluir Barcelona, se puede medir su desfase con nuestro mapa y con nuestros sensores antes de usarlo fuera.
- **Manchas de 2022** en franjas de 5 dB (`SOROLL_MUNI_*_2023`), por foco (ocio incluido), para L'Hospitalet, el Barcelonès, el Baix Llobregat y el Vallès.
- **L'Hospitalet por tramo**: solo hay de 2012 (1.939 tramos).
- **Sant Cugat no tiene mapa de ruido** (no es aglomeración). Solo el mapa de capacidad acústica, que marca objetivos legales, no niveles.
- Licencia: los metadatos remiten al "Avís legal" de gencat.cat (reutilización citando la fuente). **Sin confirmar** que sea CC BY.

### 5.2 Por municipio

| Fuente | L'Hospitalet | Badalona | Sant Cugat |
|---|---|---|---|
| Mapa | Tramos 2012 + manchas 2022 | **Tramos 2018** + manchas 2022 | No hay |
| Sensores | No hay | 5 de la Diputació, sin dato reciente | 6 de la Diputació, solo el último valor |
| Portales | [23.024](https://dadesobertes.seu-e.cat/api/3/action/package_search?fq=organization:hospitaletdellobregat) (CC BY-ND) | 28.242 ([GeoServer](https://geoportal.badalona.cat/geoserver/ows)) | 13.968 ([geoportal](https://geociutat.santcugat.cat/apps/giscube-admin/layerserver/geojsonlayers/bru_portals_locals)) |
| Locales | No hay | No hay | No hay |
| Obras | Capa parada (2017–2019) | Desfasada (2015) | API pide autorización (401) |
| Quejas | Solo incidencias de limpieza (8 de "Soroll") | No encontradas | No hay |
| Pisos turísticos | 707 con coordenadas | 223, solo dirección ([Generalitat](https://analisi.transparenciacatalunya.cat/resource/t2h3-cgys.json)) | 97, solo dirección |
| Patios / anchura | Sin calcular | Parcelas, edificios y **anchura de aceras** | Sin calcular |

- **Terrassa** tiene 48 sensores de ruido públicos en su propio Sentilo (36 con dato hoy). Es la mejor candidata para comprobar si los perfiles horarios de Barcelona valen fuera, si se consigue el histórico.
- **Reutilizar los perfiles de Barcelona**: razonable en L'Hospitalet, Badalona, Santa Coloma y Sant Adrià (tejido continuo con Barcelona). En Sant Cugat, no sin calibrar antes.

**Qué falta frente a Barcelona**: censo de bares y horarios, obras al día, quejas con ubicación y sensores por hora. Sin bares, la noche (50 % de la nota) quedaría solo con el mapa, que es justo donde más falla en Barcelona.

## 6. Bloqueos (ningún captcha; no se ha intentado saltar ninguno)

| Dónde | Qué pasó | Qué debería descargar Pablo a mano |
|---|---|---|
| Catastro (INSPIRE) | 403 "acceso denegado desde su dirección IP" | Edificios de Valencia: [ES.SDGC.bu.atom_46.xml](https://www.catastro.hacienda.gob.es/INSPIRE/buildings/46/ES.SDGC.bu.atom_46.xml). Provincia de Barcelona: [direcciones](https://www.catastro.hacienda.gob.es/INSPIRE/Addresses/08/ES.SDGC.AD.atom_08.xml), parcelas y edificios. Solo si se hace el área metropolitana o Valencia |
| valencia.es | "Request Rejected" a descargas automáticas | Plan de acción 2023–2027 y presentación del mapa 2017, desde [la página del mapa del ruido](https://www.valencia.es/cas/calidadaire/mapa-del-ruido) |
| SICA (Ministerio) | Fallo de certificado y 503 | [Memoria del mapa 2022 de València](https://sicaweb.cedex.es/docs/mapas/fase4/aglomeracion/Aglomeraci%C3%B3n%20de%20Valencia/Ag_VAL_Valencia_15_Memoria.pdf) |
| badalona.cat | 403 de CloudFront | Mirar en el navegador si [dades obertes de Badalona](https://www.badalona.cat/dadesobertes) tiene censo de actividades, obras o quejas |
| ICGC | La conexión se corta | [Direcciones de Cataluña v2.2](https://datacloud.icgc.cat/datacloud/adreces/gpkg/adreces-v2r2-20260410-gpkg.zip) (CC BY 4.0) |
| sigma.madrid.es | Rechaza consultas con `LIKE`; a veces responde vacío | Nada: se evita consultando por rectángulo de coordenadas |

Para Madrid **no hace falta descargar nada a mano**.

## 7. Cómo encajaría Madrid en el sistema de Barcelona

Las reglas del modelo se mantienen igual: nota 0–100 lineal (día y tarde 45→75 dB, noche 35→70 dB), franjas 7–19, 19–23 y 23–7, y global 30/20/50.

**Se copia tal cual**: la fórmula de la nota, las franjas y los pesos, la compresión de los extremos, el visor y el buscador, la lógica de obras y el aviso de picos.

**Hay que adaptar**:
1. **Índice de portales**: en lugar de buscar el tramo, leer el ráster justo delante de la fachada del portal. Si el píxel cae en un patio, es nota "interior".
2. **Forma horaria**: usar la forma por hora de Barcelona (tráfico y ocio) dentro de cada franja, como ya se hace, y comprobar con los L10/L90 y con el tráfico cada 15 minutos de Madrid que encaja. La media de cada franja sigue saliendo del mapa de Madrid.
3. **Pesos por día de la semana**: sacarlos de los datos diarios de Madrid (31 estaciones), una vez aclarado a qué día se apunta cada noche.
4. **Suma por bares**: recalcular los coeficientes con las estaciones de Madrid. Con 31 puntos, la validación "dejando fuera cada distrito" será débil. Hay que decirlo en el visor (confianza más baja) hasta tener más mediciones.
5. **Horarios de ocio**: leerlos del censo en vez de un dataset aparte.
6. **Obras**: puntos de Informo en vez de polígonos.
7. **Quejas y pisos turísticos**: geocodificar con el callejero.

**Pedir por transparencia** (Ayuntamiento de Madrid):
- Datos por hora (o por minuto) de las 31 estaciones de la red fija, al menos de 2023 a hoy.
- Horarios de recogida de basura y limpieza por calle (como en Barcelona).

## 8. Recomendación

1. **Madrid primero.** Es la única que cumple la regla de "funcionar igual que Barcelona" sin esperar a nadie: el mapa es mejor, el censo de locales es mejor y todo se descarga sin captcha y con CC BY. Lo único serio que falta (datos por hora) tiene un apaño razonable y se puede pedir en paralelo.
2. **Área metropolitana como ampliación de Barcelona**, no como ciudad nueva: L'Hospitalet y Badalona con el mapa de la Generalitat y los perfiles de Barcelona, marcando "confianza baja" mientras no haya bares ni obras. Es poco trabajo porque el visor y los perfiles ya existen.
3. **Valencia, más adelante**, cuando conteste a una solicitud de transparencia sobre locales y sensores. Hoy le faltan las piezas que más pesan de noche.

Esta recomendación se basa en los datos. La votación de la web sobre la próxima ciudad puede añadir otros motivos (dónde está la demanda).

## Fuentes de las notas de trabajo

Los detalles (columnas, cifras, consultas exactas) están en las notas de trabajo: [Madrid](notas/madrid.md), [Valencia](notas/valencia.md) y [área metropolitana](notas/amb.md). Las rutas de descarga que citan eran temporales y no se han guardado. Los enlaces principales están en cada sección. Portales consultados: [datos.madrid.es](https://datos.madrid.es), [geoportal.madrid.es](https://geoportal.madrid.es), [datos.comunidad.madrid](https://datos.comunidad.madrid), [opendata.vlci.valencia.es](https://opendata.vlci.valencia.es), [geoportal.valencia.es](https://geoportal.valencia.es/server/rest/services), [dadesobertes.gva.es](https://dadesobertes.gva.es), [sig.gencat.cat](https://sig.gencat.cat/ows/ATMOSFERA/wfs?service=WFS&request=GetCapabilities), [analisi.transparenciacatalunya.cat](https://analisi.transparenciacatalunya.cat), [dadesobertes.seu-e.cat](https://dadesobertes.seu-e.cat), [geoportal.badalona.cat](https://geoportal.badalona.cat/geoserver/ows), [geociutat.santcugat.cat](https://geociutat.santcugat.cat), [sentilo.diba.cat](https://sentilo.diba.cat), [sentilo.terrassa.cat](https://sentilo.terrassa.cat), [opendata.amb.cat](https://opendata.amb.cat).
