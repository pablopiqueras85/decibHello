# DecibHello — Fuentes de datos de ruido en Barcelona

Estado: primera investigación (octubre 2026). Basada en búsquedas web: los portales de datos no se han podido abrir directamente desde el entorno de trabajo, así que **los nombres de columnas, la cobertura exacta y la fecha del último fichero están por comprobar** descargando cada conjunto.

Licencia general de Open Data BCN: **CC BY 4.0**. Se puede usar comercialmente citando al Ajuntament de Barcelona como fuente.

## 1. Resumen

| # | Fuente | Qué aporta a la nota | Detalle espacial | Detalle temporal | Prioridad |
|---|---|---|---|---|---|
| 1 | Mapa estratégico de ruido (MES) — por tramo de calle | Base de la nota en toda la ciudad | Tramo entre dos cruces | Día, tarde, noche y Lden (media anual) | **Imprescindible** |
| 2 | MES — fachadas, ráster e isófonas | Afinar el lado del edificio y el patio interior | Fachada / celda | Igual que 1 | Alta |
| 3 | Red municipal de sensores de ruido | Patrones reales de noche y fin de semana | Unos 200 puntos | Continuo; publicación mensual | **Imprescindible** |
| 4 | Censo de locales en planta baja | Bares, restaurantes y ocio cerca del piso | Local | Foto fija | Alta |
| 5 | Quejas IRIS | Molestia percibida por los vecinos | Por confirmar | Trimestral | Media |
| 6 | Viviendas de uso turístico (HUT) | Densidad de pisos turísticos | Dirección con coordenadas | Trimestral | Media |
| 7 | Obras en el espacio público | Avisos de obras activas | Obra georreferenciada | Con fechas de inicio y fin | Media |
| 8 | Estado del tráfico por tramos | Intensidad de tráfico por hora | Tramo de vía principal | Tiempo real + histórico | Baja–media |
| 9 | Aeropuerto de El Prat (MER fase IV) | Ruido de aviones | Isófonas | Día, tarde, noche y Lden | Baja en Barcelona ciudad |
| 10 | Ferrocarril (ADIF, FGC, metro) vía SICA | Ruido de trenes | Isófonas | Día, tarde, noche y Lden | Baja–media |
| 11 | OpenStreetMap | Colegios, discotecas, mercados, hospitales | Punto | Foto fija | Alta |
| 12 | Observatori del Soroll (Xavecs) | Análisis ya hechos; posible socio | Sensores | Minuto a minuto | Contacto |

## 2. Detalle por fuente

### 2.1 Mapa estratégico de ruido de Barcelona (MES)

Es la fuente principal. El vigente es el de la **fase 4**: datos de 2022, válido para 2022–2027, y hecho con el método europeo común CNOSSOS-EU.

Conjuntos publicados en Open Data BCN:
- **Por tramo de calle** (`tramer-mapa-estrategic-soroll`): nivel medio que llega a las fachadas entre dos cruces, por tipo de fuente y franja horaria. Hay versiones de 2009, 2012, 2017 y 2022, en CSV (geometría en la columna `GEOM_WKT`) y GeoPackage.
- **Por fachada** (`facanes-mapa-estrategic-soroll`): nivel en cada fachada. Sirve para distinguir un piso que da a la calle de uno que da al patio de manzana.
- **Ráster** (`rasters-mapa-estrategic-soroll`): rejilla continua en GeoPackage, 2022, con ruido industrial, de ocio y total, en día, tarde, noche y Lden.
- **Isófonas, población expuesta y mapa de capacidad acústica** (zonificación acústica de la ciudad).

Fuentes de ruido separadas: tráfico, ferrocarril, industria y ocio. Según el Ajuntament, el tráfico es la fuente principal en toda la ciudad, y de noche, en algunas zonas, aparece el ruido por uso intensivo del espacio público, que no es el más alto pero sí el que más molesta. El mapa de 2022 muestra una bajada media del 5–6 % frente al de cinco años antes.

Limitaciones:
- Son niveles **modelizados y promediados en el año**. No reflejan los picos de un viernes por la noche ni el verano.
- Se actualiza cada cinco años; el próximo corresponde a 2027.

### 2.2 Red de sensores de ruido (Sentilo)

- Open Data BCN publica las **instalaciones** de la red de monitorización del ruido ambiental y los **datos de medición**, con actualización mensual y un histórico que arranca al menos en 2016. Está clasificado como conjunto de datos de alto valor.
- Los sensores envían datos a Sentilo, la plataforma de sensores del Ajuntament. Según la prensa, hay **más de 200 sonómetros**.
- Es la única fuente con el ruido real hora a hora. Sirve para:
  - calibrar la nota calculada con el MES;
  - mostrar el patrón real de noche, fin de semana y verano en las calles con sensor;
  - medir el efecto de fiestas y eventos.
- Limitación: unos 200 puntos no cubren todas las calles. Fuera de ellos, la nota se apoya en el MES con confianza menor.

### 2.3 Locales en planta baja

- `cens-locals-planta-baixa-act-economica`: ubicación y tipo de actividad de cada local en planta baja, con su estado (activo, inactivo, en alquiler, en venta). Última actualización encontrada: diciembre de 2024.
- Para DecibHello: contar bares, restaurantes y locales de ocio en un radio de 50–100 m del piso. Es el mejor indicador de ruido intermitente nocturno.
- Hay una tabla de códigos de actividad aparte (`cens-activitats-economiques-class-bcn`).

### 2.4 Terrazas

- El conjunto de terrazas excepcionales (decreto 21/5, del periodo COVID) está **discontinuado desde 2022**: esas terrazas pasaron a ser ordinarias.
- Pendiente: localizar el conjunto actualizado de terrazas ordinarias con su ubicación y número de mesas. También existe el padrón de la tasa por uso privativo de la vía pública.

### 2.5 Quejas IRIS

- Conjunto `iris`: incidencias, quejas y sugerencias de la ciudadanía, con tipo, tema, fechas, ubicación y canal. Se publica cada trimestre.
- El ruido en el espacio público encabeza las quejas en algunos periodos.
- Pendiente: comprobar si la ubicación viene por dirección o solo por barrio. Si es por barrio, sirve como indicador de molestia por zona, no por calle.

### 2.6 Viviendas de uso turístico

- `habitatges-us-turistic`: registro de pisos turísticos con dirección, número de plazas y coordenadas WGS84. Publicación trimestral, histórico desde 2018.
- Para DecibHello: densidad de pisos turísticos en el edificio y en la manzana (ruido de entradas, salidas y maletas a deshoras).

### 2.7 Obras en el espacio público

- Catálogo "Open Data Obres": cada obra georreferenciada con tipo, duración e impactos, en CSV, JSON y XML.
- Para DecibHello: mejor como **aviso** ("obra prevista hasta marzo a 80 m") que dentro de la nota, porque es temporal.

### 2.8 Estado del tráfico

- `trams` e `itineraris`: estado del tráfico por tramo de las vías principales (de muy fluido a cortado), en tiempo real y con histórico mensual en CSV.
- Para DecibHello: secundario, porque el MES ya incluye el tráfico. Puede ayudar a estimar cómo cambia el tráfico por hora en las vías principales.

### 2.9 Aeropuerto de El Prat

- Mapa estratégico de ruido de fase IV, aprobado el 23 de enero de 2023 y publicado por el Ministerio de Transportes, con mapas de Lden, Ld, Le y Ln. AENA también publica mapas y planes de acción.
- En Barcelona ciudad el impacto es pequeño. Ganará peso al ampliar al área metropolitana (Baix Llobregat).

### 2.10 Ferrocarril

- El SICA del Ministerio (sicaweb.cedex.es) reúne los mapas estratégicos y planes de acción de ADIF (Rodalies), FGC y metro.
- El MES municipal ya recoge el ferrocarril como fuente. El SICA sirve para comprobar y, sobre todo, para el área metropolitana.

### 2.11 OpenStreetMap

- Colegios (ruido del patio), discotecas, mercados, hospitales (sirenas), estaciones, parques.
- Licencia **ODbL**: si mezclamos datos de OSM en una base de datos que se distribuya, esa base tiene que compartirse con la misma licencia. Conviene usarlo para cálculos internos o revisarlo antes de ofrecer una API.

### 2.12 Observatori del Soroll — Xarxa Veïnal Contra el Soroll (Xavecs)

- Plataforma vecinal (xavecs.org, "Barcelona Ruidosa") que muestra en tiempo real los datos de los sensores de Sentilo, con gráficos diarios y semanales y registros minuto a minuto. Tiene análisis de terrazas, patios escolares y macroconciertos por distrito y barrio.
- No es una fuente que convenga copiar, pero sí un **posible aliado**: ya han resuelto parte del tratamiento de datos de los sensores y tienen contacto con vecinos afectados, útil para las entrevistas de validación.

## 3. Área metropolitana (para más adelante)

- Badalona, Santa Coloma de Gramenet y Sant Adrià de Besòs tienen un mapa estratégico de ruido común, la "aglomeración del Barcelonès", de fase 4 (2022–2027). La Generalitat lo aprobó en enero de 2025 (Resolució TER/4750/2024).
- Otras aglomeraciones del área (Baix Llobregat, Vallès) también tienen mapas de fase 4.
- Pendiente: comprobar el formato de descarga (¿datos SIG o solo PDF?) y el mapa de L'Hospitalet.

## 4. Cómo encajan en la nota 0–100 (100 = muy ruidoso)

1. **Base**: nivel del MES por tramo de calle (o por fachada) en día, tarde y noche → nota por franja.
2. **Corrección con sensores**: si hay sensor cerca, ajustar con el patrón real (noches de fin de semana, verano).
3. **Suma por focos intermitentes**: bares y ocio cercanos, terrazas, densidad de pisos turísticos, colegios.
4. **Avisos aparte, sin entrar en la nota**: obras activas, fiestas mayores, eventos.
5. **Confianza**:
   - alta: MES + sensor cercano;
   - media: solo MES;
   - baja: datos antiguos o tramo sin datos.

## 5. Huecos que ningún dato público cubre

- Ruido dentro del edificio: vecinos, ascensor, instalaciones, calidad del aislamiento.
- Diferencias entre plantas (un 1.º y un 7.º en la misma fachada).
- Ruido puntual de pocos días (fiestas) más allá de los puntos con sensor.

Las mediciones colaborativas y las valoraciones de vecinos de las fases siguientes servirían para cubrir estos huecos.

## 6. Próximos pasos

1. Descargar el MES 2022 por tramo de calle y por fachada, revisar columnas y cobertura.
2. Descargar el histórico de los sensores y ver cuántas calles quedan cerca de uno.
3. Cruzar las 20 direcciones del piloto con el MES, los locales y los pisos turísticos, y calcular una primera nota.
4. Localizar el conjunto de terrazas ordinarias y comprobar el detalle de ubicación de IRIS.
5. Contactar con Xavecs.

## Fuentes consultadas

- [Open Data BCN — catálogo](https://opendata-ajuntament.barcelona.cat/data/ca/dataset)
- [Mapas de ruido por tramo de calle del MES (datos.gob.es)](https://datos.gob.es/en/catalogo/l01080193-mapas-de-ruido-por-tramo-de-calle-del-mapa-estrategico-de-ruido-de-la-ciudad-de-barcelona)
- [Mapas de ruido de fachadas del MES](https://opendata-ajuntament.barcelona.cat/data/es/dataset/facanes-mapa-estrategic-soroll)
- [Mapas de ruido ráster del MES](https://opendata-ajuntament.barcelona.cat/data/es/dataset/rasters-mapa-estrategic-soroll)
- [Población expuesta del MES (data.europa.eu)](https://data.europa.eu/data/datasets/https-opendata-ajuntament-barcelona-cat-data-dataset-poblacio-exposada-mapa-estrategic-soroll?locale=en)
- [Mapa de capacidad acústica](https://opendata-ajuntament.barcelona.cat/data/ca/dataset/capacitat-mapa-estrategic-soroll)
- [Barcelona tramita el mapa del soroll fins al 2027 (Ajuntament, nov. 2024)](https://ajuntament.barcelona.cat/premsa/2024/11/10/inclou-material-audiovisual-barcelona-tramita-el-mapa-del-soroll-a-la-ciutat-fins-al-2027/)
- [Barcelona redueix el soroll entre un 5 i un 6 % (betevé)](https://beteve.cat/societat/barcelona-redueix-soroll-5-per-cent-reduccio-transit-velocitat/)
- [Instalaciones de la red de monitorización del ruido ambiental (datos.gob.es)](https://datos.gob.es/en/catalogo/l01080193-instalaciones-de-la-red-de-monitorizacion-del-ruido-ambiental-de-la-ciudad-de-barcelona)
- [Sentilo, la red de sensores de Barcelona](https://ajuntament.barcelona.cat/digital/en/technology-service-citizens/technology-sustainable-city/sentilo-barcelona-sensors-network)
- [Observatori del Soroll — Xavecs](https://xavecs.org/)
- [Neix l'Observatori del Soroll (betevé)](https://beteve.cat/societat/neix-observatori-soroll-dades-contaminacio-acustica-barcelona/)
- [Censo de locales en planta baja](https://opendata-ajuntament.barcelona.cat/data/es/dataset/cens-locals-planta-baixa-act-economica)
- [Terrazas excepcionales (decreto 21/5)](https://opendata-ajuntament.barcelona.cat/data/ca/dataset/aut-terrasses-excep-decret-21-5)
- [IRIS — incidencias, quejas y sugerencias](https://opendata-ajuntament.barcelona.cat/data/ca/dataset/iris)
- [Viviendas de uso turístico](https://opendata-ajuntament.barcelona.cat/data/es/dataset/habitatges-us-turistic)
- [Obras en el espacio público (datos.gob.es)](https://datos.gob.es/en/catalogo/l01080193-obras-en-el-espacio-publico-de-la-ciudad-de-barcelona)
- [Estado del tráfico por tramos](https://opendata-ajuntament.barcelona.cat/data/en/dataset/trams)
- [MER Aeropuerto Josep Tarradellas Barcelona-El Prat, fase IV (Ministerio de Transportes)](https://www.transportes.gob.es/aviacion-civil/medioambiente/mapas-estrategicos-ruido/mer-catalunya-fase-iv)
- [AENA — mapas estratégicos de ruido y planes de acción](https://www.aena.es/en/corporative/environment-sustainability/noise/strategic-noise-maps-and-action-plans.html)
- [SICA — planes de acción](https://sicaweb.cedex.es/planes-de-accion/)
- [Aprobado el MES de la aglomeración del Barcelonès, fase 4 (Generalitat)](https://mediambient.gencat.cat/ca/detalls/Noticies/20250116-aprovat-mapa-soroll)
