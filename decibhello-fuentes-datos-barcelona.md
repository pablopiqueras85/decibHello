# DecibHello — Fuentes de datos de ruido en Barcelona

Estado: investigación de octubre de 2026. Las fuentes 1–6 están **comprobadas directamente en Open Data BCN** (columnas, número de registros y fechas; cómo acceder en la sección 3). El resto sale de búsquedas web y está por comprobar.

Licencia general de Open Data BCN: **CC BY 4.0**. Se puede usar comercialmente citando al Ajuntament de Barcelona como fuente.

## 1. Resumen

| # | Fuente | Qué aporta a la nota | Detalle espacial | Detalle temporal | Prioridad |
|---|---|---|---|---|---|
| 1 | Mapa estratégico de ruido (MES) — por tramo de calle | Base de la nota en toda la ciudad | 17.958 tramos entre cruces | Día, tarde, noche y Lden (media anual, **2017**) | **Imprescindible** |
| 2 | MES 2022 — ráster | Versión más reciente del mapa | Celda de rejilla | Día, tarde, noche y Lden | Alta |
| 3 | Red municipal de sensores de ruido | Patrones reales de noche y fin de semana | 176 sensores activos | Minuto a minuto desde 2024 | **Imprescindible** |
| 4 | Censo de locales en planta baja | Bares, restaurantes y ocio cerca del piso | 44.000 locales con coordenadas | Foto fija (2024) | Alta |
| 5 | Quejas IRIS | Quejas de vecinos por ruido en la calle | Dirección con coordenadas | Anual, actualizado durante el año | Alta |
| 6 | Viviendas de uso turístico (HUT) | Densidad de pisos turísticos | 10.721 pisos con coordenadas | Trimestral | Media |
| 7 | Obras en el espacio público | Avisos de obras activas | Obra georreferenciada | Con fechas de inicio y fin | Media |
| 8 | Estado del tráfico por tramos | Intensidad de tráfico por hora | Tramo de vía principal | Tiempo real + histórico | Baja–media |
| 9 | Aeropuerto de El Prat (MER fase IV) | Ruido de aviones | Isófonas | Día, tarde, noche y Lden | Baja en Barcelona ciudad |
| 10 | Ferrocarril (ADIF, FGC, metro) vía SICA | Ruido de trenes | Isófonas | Día, tarde, noche y Lden | Baja–media |
| 11 | OpenStreetMap | Colegios, discotecas, mercados, hospitales | Punto | Foto fija | Alta |
| 12 | Observatori del Soroll (Xavecs) | Análisis ya hechos; posible socio | Sensores | Minuto a minuto | Contacto |

## 2. Detalle por fuente

### 2.1 Mapa estratégico de ruido de Barcelona (MES)

Es la fuente principal. El vigente es el de la **fase 4** (datos de 2022, válido para 2022–2027, método europeo CNOSSOS-EU), pero **por tramo de calle solo está publicada la versión de 2017**.

Conjuntos publicados en Open Data BCN (comprobado):
- **Por tramo de calle** (`tramer-mapa-estrategic-soroll`): versiones de 2009, 2012 y **2017**; la de 2022 no está. 17.958 tramos, legibles por la API del portal. Columnas, para día (`_D`), tarde (`_E`), noche (`_N`) y Lden (`_DEN`):
  - `TOTAL`, `TRANSIT` (tráfico), `GI_TR` (grandes infraestructuras de transporte), `FFCC` (ferrocarril), `INDUST` (industria);
  - `VIANANTS_D/E` (zonas peatonales), `OCI_N` (ocio de noche), `PATIS_D/E` (patios escolares);
  - `GEOM_WKT` con la geometría del tramo.
  - **Los valores vienen en franjas de 5 dB** como texto ("60 - 65 dB(A)"), no como cifra exacta.
- **Ráster 2022** (`rasters-mapa-estrategic-soroll`): 24 ficheros GeoPackage de unos 97 MB cada uno: tráfico, ferrocarril, industria, ocio, total y total obligatorio, cada uno en día, tarde, noche y Lden. Es el dato más reciente, pero hay que leerlo como rejilla y no por calle.
- **Por fachada** (`facanes-mapa-estrategic-soroll`): solo 2017, en GeoPackage. Sirve para distinguir un piso que da a la calle de uno que da al patio de manzana.
- **Población expuesta y mapa de capacidad acústica** (zonificación acústica de la ciudad).

Primer dato útil (MES 2017, noche): el **76 % de los tramos** está en 45 dB o más, por encima de la recomendación nocturna de la OMS para tráfico. Solo el 15 % está por debajo de 40 dB. La escala 0–100 tendrá que repartir bien la franja de 45–65 dB, que es donde está la mayoría de calles.

Fuentes de ruido separadas: tráfico, ferrocarril, industria y ocio. Según el Ajuntament, el tráfico es la fuente principal en toda la ciudad, y de noche, en algunas zonas, aparece el ruido por uso intensivo del espacio público, que no es el más alto pero sí el que más molesta. El mapa de 2022 muestra una bajada media del 5–6 % frente al de cinco años antes.

Limitaciones:
- Son niveles **modelizados y promediados en el año**. No reflejan los picos de un viernes por la noche ni el verano.
- Se actualiza cada cinco años; el próximo corresponde a 2027.

### 2.2 Red de sensores de ruido (Sentilo)

- **Instalaciones** (`xarxasoroll-equipsmonitor-instal`, comprobado): 989 ubicaciones históricas, de las que **176 están activas** (sin fecha de retirada), en **39 barrios**. Cada una tiene dirección, coordenadas y el motivo de la medición:
  - ocio: 80;
  - tráfico: 79;
  - zona peatonal: 13;
  - otros: 4.
- Reparto por distrito de los sensores activos:

  | Distrito | Sensores |
  |---|---|
  | Eixample | 45 |
  | Ciutat Vella | 37 |
  | Sant Martí | 27 |
  | Gràcia | 21 |
  | Sants-Montjuïc | 16 |
  | Sant Andreu | 14 |
  | Horta-Guinardó | 6 |
  | Sarrià-Sant Gervasi | 6 |
  | Les Corts | 3 |
  | Nou Barris | 1 |
- **Mediciones** (`xarxasoroll-equipsmonitor-dades`): datos **por hora de 2015 a 2023** (un ZIP por semestre) y **por minuto desde enero de 2024** (un ZIP por mes, el último de junio de 2026).
- **Datos por hora de 2023 ya analizados** (`piloto/sensores.py`, octubre de 2026), descargados a mano:
  - columnas: año, mes, día, hora, sensor y nivel LAeq de la hora;
  - **cuidado con la fecha**: de 7:00 a 23:59 la fecha registrada es la del día siguiente; de 0:00 a 6:59 es correcta. Se comprobó con la verbena de Sant Joan, Navidad y Semana Santa, y el script lo corrige;
  - de ahí salen la forma horaria y los pesos por día de la semana del tráfico (62 sensores) y del ocio (73 sensores), y el nivel medido en cada sensor, que el visor usa en 352 tramos;
  - comparación con el mapa oficial en `piloto/validacion_sensores.md`: acierta en el tráfico (+0,9 dB de noche) y se queda corto en el ocio (+2,6 dB de mediana, hasta +27 dB en algunas plazas).
- **Sesgo importante**: los sensores se ponen donde hay problemas (ocio y tráfico) y apenas los hay en zonas tranquilas. Sirven para calibrar la nota en calles ruidosas, pero no como muestra representativa de la ciudad.
- Es la única fuente con el ruido real hora a hora. Sirve para:
  - calibrar la nota calculada con el MES;
  - mostrar el patrón real de noche, fin de semana y verano en las calles con sensor;
  - medir el efecto de fiestas y eventos.
- Limitación: 176 puntos no cubren todas las calles. Fuera de ellos, la nota se apoya en el MES con confianza menor.

### 2.3 Locales en planta baja

- `cens-locals-planta-baixa-act-economica` (comprobado): censo de 2024 con **44.000 locales**, revisados entre octubre de 2021 y octubre de 2024. Cada local tiene coordenadas, dirección, actividad y estado.
- Trae un indicador directo, `SN_Oci_Nocturn`, que marca **212 locales de ocio nocturno**. Además hay **7.729 locales** en el grupo "restaurantes, bares y hoteles".
- Para DecibHello: contar bares, restaurantes y locales de ocio en un radio de 50–100 m del piso. Es el mejor indicador de ruido intermitente nocturno.
- Hay una tabla de códigos de actividad aparte (`cens-activitats-economiques-class-bcn`).

### 2.4 Terrazas

- El conjunto de terrazas excepcionales (decreto 21/5, del periodo COVID) está **discontinuado desde 2022**: esas terrazas pasaron a ser ordinarias.
- Pendiente: localizar el conjunto actualizado de terrazas ordinarias con su ubicación y número de mesas. También existe el padrón de la tasa por uso privativo de la vía pública.

### 2.5 Quejas IRIS

- Conjunto `iris`: incidencias, quejas y sugerencias de la ciudadanía, con tipo, tema, fechas, ubicación y canal. Se publica cada trimestre.
- El ruido en el espacio público encabeza las quejas en algunos periodos.
- Comprobado: cada petición trae **calle, número, sección censal y coordenadas**, así que sirve por calle y no solo por barrio.
- En 2025 hubo **3.625 quejas** del tipo "molestias por ruido en la vía pública", casi todas con coordenadas. Hay un fichero por año desde 2023 y el de 2026 se va actualizando.

### 2.6 Viviendas de uso turístico

- `habitatges-us-turistic` (comprobado): **10.721 pisos turísticos** con dirección (hasta planta y puerta), número de plazas y coordenadas WGS84. Publicación trimestral, histórico desde 2018.
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

### 2.13 Recogida de residuos y limpieza (picos nocturnos)

El paso de camiones de basura y de limpieza de madrugada da picos cortos e intensos, sobre todo en calles estrechas. El mapa oficial no los recoge porque es una media anual.

**Qué hay (comprobado):**
- **Quejas IRIS** con el detalle "Serveis neteja i recollida": unas 1.200 entre 2023 y 2026, con dirección y coordenadas. Ya las usa el aviso de "picos nocturnos" del visor. Que una calle no tenga quejas no significa que no haya molestia (Martínez de la Rosa no tiene ninguna, pero hay 5 a menos de 100 m).
- **Anchura de la calle**: no es un dato publicado, pero se estima con el listado oficial de portales (distancia a los portales de enfrente). Ejemplos: Martínez de la Rosa ≈ 8 m, Escudellers ≈ 7 m, Tuset ≈ 23 m, Passeig de Gràcia ≈ 63 m.
- **Recogida de muebles y trastos**: cada calle tiene un día asignado y se deja entre las 20 y las 22 h. El buscador de residus del Ajuntament lo consulta por dirección, pero no está publicado como datos abiertos. La síndica de greuges señaló en 2021 esta recogida como la principal queja por ruido de los servicios municipales.
- **Horarios por zona, sueltos en prensa**: por ejemplo, en Ciutat Vella se concentró la recogida a la 1:45 y en Joaquín Costa se adelantó a las 3:00 (betevé); en el Poble-sec se recogía entre las 0:00 y las 4:30 (Zona Sec, 2016).

**Qué no hay (en abierto):** la ubicación de los contenedores de calle, y las rutas y horarios de los camiones por calle. Open Data BCN solo publica puntos verdes, contenedores de ropa y de sal; la wiki de OpenStreetMap recoge importaciones municipales de contenedores de pilas y aceite, no de los de calle.

**Cómo conseguirlo:**
1. **Solicitud de acceso a la información pública** (Ley 19/2014 de transparencia de Cataluña) al Ajuntament, por la sede electrónica. Tiene plazo legal de respuesta de un mes. Borrador listo para enviar más abajo.
2. **Pedir a Open Data BCN que lo publique** (tienen un formulario de sugerencias de datos).
3. **OpenStreetMap**: hay voluntarios que mapean contenedores (`amenity=recycling`, `amenity=waste_disposal`). Falta medir la cobertura en Barcelona: el servidor de consultas (Overpass) no responde desde el entorno de trabajo.
4. **Vecinos**: que los usuarios marquen "aquí pasa el camión a las 2:00" y el contenedor de su calle. Es el dato más preciso y además genera comunidad.
5. **Sensores**: los datos minuto a minuto desde 2024 sí recogen el pico del camión donde hay sensor (pendientes de descarga manual).

**Borrador de solicitud (castellano; se puede enviar también en catalán):**

> Al amparo de la Ley 19/2014, de 29 de diciembre, de transparencia, acceso a la información pública y buen gobierno, solicito la siguiente información en formato reutilizable (CSV, JSON o SHP), referida al servicio municipal de recogida de residuos y limpieza viaria de Barcelona:
>
> 1. Ubicación georreferenciada de los contenedores de calle de todas las fracciones (resto, orgánica, envases, papel y cartón, vidrio), con su fracción.
> 2. Rutas o sectores de recogida y, para cada calle o tramo, la franja horaria y los días de la semana en que pasa el camión de cada fracción.
> 3. Calendario de recogida de muebles y trastos por calle (el día asignado a cada calle).
> 4. Franjas horarias de los servicios nocturnos de limpieza viaria (barrido mecánico y baldeo) por calle o sector.
>
> La finalidad es elaborar un servicio informativo sobre el ruido urbano para la ciudadanía. Solicito además, si es posible, que esta información se publique en Open Data BCN.

## 3. Cómo se accede a los datos

- **Ficheros tabulares (CSV)**: se leen sin problema por la API del portal (`datastore_search` y `datastore_search_sql`), con consultas y filtros. Así funcionan el MES por tramo, el censo de locales, los pisos turísticos, IRIS y la lista de sensores.
- **Descargas directas (ZIP y GeoPackage)**: el portal las protege con una **verificación anti-bots (hCaptcha)**, así que no se pueden descargar de forma automática. Afecta a las mediciones de los sensores y al ráster de 2022. Opciones:
  - descargarlas a mano desde el navegador para el piloto;
  - pedir acceso al Ajuntament (Open Data BCN) para un uso continuado.
- datos.gob.es también rechaza los accesos automáticos.

## 4. Área metropolitana (para más adelante)

- Badalona, Santa Coloma de Gramenet y Sant Adrià de Besòs tienen un mapa estratégico de ruido común, la "aglomeración del Barcelonès", de fase 4 (2022–2027). La Generalitat lo aprobó en enero de 2025 (Resolució TER/4750/2024).
- Otras aglomeraciones del área (Baix Llobregat, Vallès) también tienen mapas de fase 4.
- Pendiente: comprobar el formato de descarga (¿datos SIG o solo PDF?) y el mapa de L'Hospitalet.

## 5. Cómo encajan en la nota 0–100 (100 = muy ruidoso)

1. **Base**: nivel del MES por tramo de calle (2017, en franjas de 5 dB) en día, tarde y noche → nota por franja. Más adelante, actualizarlo con el ráster de 2022.
2. **Corrección con sensores**: si hay sensor cerca, ajustar con el patrón real (noches de fin de semana, verano).
3. **Suma por focos intermitentes**: bares y ocio cercanos, terrazas, densidad de pisos turísticos, colegios.
4. **Avisos aparte, sin entrar en la nota**: obras activas, fiestas mayores, eventos.
5. **Confianza**:
   - alta: MES + sensor cercano;
   - media: solo MES;
   - baja: datos antiguos o tramo sin datos.

## 6. Huecos que ningún dato público cubre

- Ruido dentro del edificio: vecinos, ascensor, instalaciones, calidad del aislamiento.
- Diferencias entre plantas (un 1.º y un 7.º en la misma fachada).
- Ruido puntual de pocos días (fiestas) más allá de los puntos con sensor.

Las mediciones colaborativas y las valoraciones de vecinos de las fases siguientes servirían para cubrir estos huecos.

## 7. Próximos pasos

1. Elegir las 20 direcciones del piloto y calcular una primera nota con el MES 2017 por tramo, los locales de ocio, los pisos turísticos y las quejas IRIS. Todo eso ya es accesible por la API.
2. Descargar a mano un mes de datos de sensores (minuto a minuto) y el ráster de noche de 2022, para comparar con el MES 2017.
3. Escribir a Open Data BCN para saber si hay MES 2022 por tramo de calle y cómo acceder sin la verificación anti-bots.
4. Localizar el conjunto de terrazas ordinarias.
5. Contactar con Xavecs.

## Fuentes consultadas

- [Cercador de residus — mobles i trastos (Ajuntament)](https://ajuntament.barcelona.cat/cercador-de-residus/ca/fra/VO)
- [Sabeu quin dia es recullen els mobles i trastos vells al vostre carrer? (Ajuntament)](https://www.barcelona.cat/infobarcelona/ca/sabeu-quin-dia-es-recullen-els-mobles-i-trastos-vells-al-vostre-carrer_1343837.html)
- [Canvi d'horaris de neteja a Ciutat Vella (betevé)](https://beteve.cat/societat/canvi-horari-neteja-ciutat-vella-soroll-nocturn/)
- [La síndica vol avançar la recollida de residus pel soroll (betevé)](https://beteve.cat/societat/sindica-demana-avancar-recollida-residus-voluminosos-pel-soroll-barcelona/)
- [La recollida de brossa al barri genera queixes pel soroll (Zona Sec)](https://zona-sec.cat/2016/05/21/la-recollida-de-brossa-al-barri-genera-queixes-pel-soroll-i-lhorari/)
- [Importació Ajuntament de Barcelona (wiki OpenStreetMap)](https://wiki.openstreetmap.org/wiki/Ca:Importaci%C3%B3_Ajuntament_de_Barcelona)

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
