# Madrid: fuentes de datos abiertos para DecibHello

Comprobado el 6 de octubre de 2026 con descargas reales desde aquí. Las descargas están en
`scratchpad/descargas-madrid/` (sensores, callejero, locales, mer, obras, avisos, syr, vut, trafico, residuos, inspecc).

## Lo importante en cinco líneas

1. **Mapa de ruido 2021 (fase 4) en ráster de 5 m, con valores en dB continuos** (no en franjas de 5 dB como Barcelona), para Ld, Le, Ln y Lden. Descarga directa de 44 MB. Incluye los patios de manzana (unos 35 dB frente a 55–67 dB en la calle): sirve para separar exterior de interior. Solo cuenta el tráfico.
2. **Sensores: 31 estaciones fijas con datos diarios desde 1998 hasta ayer**, pero **solo por franja (día, tarde, noche y total)**, no por hora. Con ellos salen perfiles por día de la semana y franja, pero no perfiles por hora.
3. **Portales: 160.615 portales con coordenadas** (214.697 direcciones en total).
4. **Censo de locales con epígrafe y horario**: 203.701 locales, 225.751 actividades, horarios de apertura y cierre en 32.516 locales, 1.300 locales de ocio nocturno abiertos (discotecas, bares especiales, salas de fiesta y café espectáculo) y 6.591 terrazas con horario.
5. **Quejas por ruido con dirección (sin coordenadas)**: 7.060 sugerencias y reclamaciones sobre ruido desde 2023 y 1.626 inspecciones ambientales "RUIDOS" en 2026. Avisa Madrid (430.596 avisos) **no tiene ruido**.

Licencia de datos.madrid.es: **CC BY 4.0** (`license_id: cc-by`, comprobado en la API). Es la misma que en Barcelona.
Ningún recurso pidió captcha ni verificación anti-robots. Lo único que bloqueó fue el cortafuegos (WAF) de `sigma.madrid.es`: devuelve "Request Rejected" en consultas con `LIKE '%…%'`. Se evita consultando por rectángulo de coordenadas. Ese servidor también devuelve a veces respuestas vacías; reintentando funciona.

---

## 1. Mapa estratégico de ruido (MER)

- **MER 2021 (fase 4)**: aprobado el 9 de febrero de 2023. Ficha en el geoportal: https://geoportal.madrid.es/IDEAM_WBGEOPORTAL/dataset.iam?id=470b89af-5d64-41d3-8bdb-2fe6badd0364
  - Descarga directa (HTTP 200, 44.610.714 bytes, fecha 12/03/2023): https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/MEDIO_AMBIENTE/INFORMACION_ACUSTICA/Mapa_Estrategico_Ruido_2021/MER2021.zip
  - Contenido: `Madrid_Ld_2021.tif`, `Madrid_Le_2021.tif`, `Madrid_Ln_2021.tif` y `Madrid_Lden_2021.tif` (184 MB cada uno sin comprimir), más dos estilos de QGIS (.qml).
  - Comprobado con el fichero Ln: GeoTIFF de números decimales (float32) de 6.254 × 7.358 píxeles, **píxel de 5 m**, sistema EPSG:25830 (ETRS89 UTM 30N) y esquina en (424755, 4499365). NoData = 0, que coincide con las **huellas de los edificios**. Los valores son continuos (unos 7.000 valores distintos en una muestra), entre −30 y 81 dB. La mediana de los píxeles con dato es 48,8 dB.
  - **Patios**: en una ventana de 200 × 200 m alrededor de Gaztambide 3, la calle da 55–71 dB de noche y el interior de las manzanas, 35–38 dB. Basta con mirar el valor justo delante de cada fachada para saber si da a la calle o al patio.
  - **Contraste con los sensores (2021)**: mediana de 3×3 píxeles en cada estación frente a la media energética anual del sensor. Ld: el mapa da 1,1 dB menos de media (dispersión de 4,2 dB, 30 estaciones). Ln: 1,9 dB menos (dispersión de 5,3 dB). Casa de Campo sale muy baja en el mapa (24 dB frente a 43,5 dB medidos), porque el mapa solo cuenta el tráfico.
  - Fuente del ruido: según la memoria, solo tráfico rodado (https://www.madrid.es/UnidadesDescentralizadas/Sostenibilidad/Ruido/MapaRuido/MapaRuido2021/Ficheros/MemoriaMER2021.pdf). La altura de cálculo no la he comprobado.
- **MER 2016 (fase 3)**: https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/MEDIO_AMBIENTE/INFORMACION_ACUSTICA/Mapa_Estrategico_Ruido_2016/MER2016.zip (HTTP 200, 31,5 MB, fecha 15/07/2019). Contiene `Ld/Le/Ln/Lden_Madrid.tif` con **píxel de 10 m** (3.128 × 3.680) y `*_Centro.tif` con píxel de 5 m solo para el distrito Centro. Valores continuos.
- La ficha del geoportal del MER 2016 (id 3d9d561c…) da "Error en la aplicación"; el ZIP sí se descarga.
- Ediciones anteriores: MER 2006 y 2011 (según el portal de transparencia). No hay enlaces de descarga; no lo he comprobado.
- **No encontré un mapa por tramo de calle ni por fachada** publicado por el Ayuntamiento. MITECO (SICA) tiene isófonas de la fase 3 en SHP/GML; para Madrid no lo he comprobado.
- No hay servicio WMS o WFS del MER en `sigma.madrid.es/hosted/rest/services/MEDIO_AMBIENTE` (lo listé: hay ZPAE, AREAS_ACUSTICAS_2018, ZAP… pero no MER).
- Licencia: la ficha del geoportal no la indica. El resto del geoportal está publicado en datos.madrid.es con CC BY 4.0. No lo he comprobado para el MER.

**Frente a Barcelona**: Madrid es **mejor** en resolución (ráster continuo de 5 m frente a franjas de 5 dB por tramo) y es más reciente (2021 frente a 2017). Le falta la capa vectorial por tramo y la de fachadas, y solo cuenta el tráfico (sin ocio ni industria).

## 2. Sensores municipales (SIVCA, red fija)

- Estaciones: https://datos.madrid.es/dataset/211346-0-estaciones-acusticas (CSV de 31 filas con código RF-xx, nombre, ubicación, distrito, barrio, longitud/latitud, X/Y en ETRS89 y fecha de alta). Las más antiguas son de 1998 y la más reciente, RF-01 Recoletos, de 2011 (en el CSV; los datos diarios de la estación "1" empiezan en 1998).
  - Ojo: la longitud y la latitud vienen con puntos de miles (`-3.691.877`). Mejor usar X/Y.
  - También funciona la API `datastore_search` de CKAN (`resource_id=211346-4-estaciones-acusticas-csv`).
- **Datos diarios**: https://datos.madrid.es/dataset/215885-0-contaminacion-ruido. El fichero es https://www.madrid.es/UnidadesDescentralizadas/Sostenibilidad/Ruido/Publicaciones/Ruido_diario_acumulado.csv (HTTP 200, 44,7 MB, codificación latin-1, separador `;`).
  - Columnas: `Estación;Año;Mes;Día;Periodo;LAeq;L1;L10;L50;L90;L99`. Periodo: D (día), E (tarde), N (noche) o T (total).
  - 1.037.224 filas, de 1998-11-01 a **2026-10-05** (ayer). 36 códigos de estación en total (31 activas).
  - Se actualiza a diario, excepto fines de semana y festivos (lo dice el PDF de estructura, versión julio de 2026).
- **Datos mensuales**: https://datos.madrid.es/dataset/211356-0-contaminacion-acustica (9.843 filas: `Estación;Nombre;Año;Mes;Ld;Le;Ln;LAeq;L1…L99`).
- **No hay datos horarios publicados.** La página "Consulta avanzada de los datos de la red fija" solo da índices diarios. Busqué "tiempo real" y "horario" en el catálogo y solo aparecen la calidad del aire y el tráfico. La red se renovó en 2021 para medir en tiempo real, pero ese dato no se publica. Si hiciera falta, habría que pedirlo por transparencia.
- **Perfil por día de la semana: sí sale.** Ejemplo de 2025 (media energética):
  - RF-03 Plaza del Carmen, noche: lunes 57,3 dB, martes 59,2, miércoles 59,5, jueves 58,6, viernes 58,9, sábado 61,6 y domingo 62,3.
  - RF-04 Plaza de España, tarde: de lunes a miércoles 62–64 dB y de jueves a domingo 71–74 dB.
  - **Falta comprobar** a qué fecha se asigna la noche: si la noche que empieza el sábado a las 23 h se apunta al sábado o al domingo. Hay que preguntarlo o deducirlo.
- **Frente a Barcelona**: hay menos estaciones (31 frente a 176), sin datos horarios (Barcelona tiene datos por hora y por minuto), pero con un histórico más largo (desde 1998) y actualización diaria. Las estaciones están sobre todo en avenidas y plazas. No hay sensores en calles de ocio, salvo Plaza del Carmen.
- Extra: el conjunto COVID (300440) tiene datos diarios y semanales de 2020. No lo he abierto.

## 3. Callejero y portales con coordenadas

- https://datos.madrid.es/dataset/213605-0-callejero-oficial-madrid (actualización semanal). El fichero `direccionesvigentes_20261004.csv` (HTTP 200, 34,7 MB, latin-1) tiene **214.697 direcciones**:
  - Portales: 160.615. Frente de fachada: 25.633. Parcela: 12.883. Garaje: 12.436. Jardín o parque: 3.130.
  - Columnas: `COD_VIA, VIA_CLASE, VIA_PAR, VIA_NOMBRE, VIA_NOMBRE_ACENTOS, CLASE_APP, NUMERO, CALIFICADOR, TIPO_NDP, COD_NDP, DISTRITO, BARRIO, COD_POSTAL, UTMX_ED, UTMY_ED, UTMX_ETRS, UTMY_ETRS, LATITUD, LONGITUD, ANGULO_ROTULACION`.
  - Todas tienen coordenadas en ETRS89 (0 sin coordenadas).
- Otros recursos:
  - Viales, tramero, cruces y numeraciones: https://datos.madrid.es/dataset/200075-0-callejero (incluye parcela catastral y código postal).
  - Servicio web SOAP: https://servpub.madrid.es/CADMA_WSUPD/services/ConsultasCadmaService?wsdl (no lo he probado).
  - Capa ArcGIS `CALLEJERO/CALLEJERO_NDPS_VIGENTES` (respuestas intermitentes desde aquí).
- `COD_NDP` es la clave que usan también el censo de locales y las VUT con licencia.
- **Frente a Barcelona**: equivalente (172.000 portales en Barcelona; aquí 160.615 más los frentes de fachada).

## 4. Locales, ocio nocturno, terrazas y horarios

- https://datos.madrid.es/dataset/200085-0-censo-locales (actualización diaria; ficheros del 06/10/2026):
  - Locales (`…053108.csv`, 89 MB, UTF-8 con BOM, separador `;`): **203.701 locales**. Estado: 139.808 abiertos, 38.887 cerrados, 12.423 de baja, 8.463 usados como vivienda… Acceso: 134.646 a pie de calle, 51.510 interiores, 14.663 agrupados.
    - Columnas útiles: `coordenada_x_local, coordenada_y_local` (ETRS89), `id_ndp_edificio`, `rotulo`, **`hora_apertura1, hora_cierre1, hora_apertura2, hora_cierre2`**.
    - Horario relleno en 32.516 locales. Combinaciones más frecuentes: 00:00–00:00, 09–21, 08–20, 08–02 y 10–02.
  - Actividades (`…053600.csv`, 125 MB): **225.751 filas** con `id_epigrafe, desc_epigrafe`, sección y división.
    - Ocio nocturno: 563002 "bar especial sin actuaciones" (863), 563003 "con actuaciones" (88), 932006 "discotecas y salas de baile" (251), 932005/932004 "salas de fiesta" (76/31) y 563007 "café espectáculo" (169).
    - Bares: 561004 bar restaurante (4.907), 561005 bar con cocina (4.488), 563005 bar sin cocina (1.857), 561006 cafetería (3.596) y 563004 taberna (146).
    - Cruzando con los locales abiertos: **1.300 de ocio nocturno** (448 con hora de cierre; las más frecuentes son 05:30, en 203 casos, y 03:00, en 99) y **13.403 bares** (4.187 con hora de cierre).
  - Terrazas (`…053440.csv`, 5,2 MB): **6.591 terrazas** (6.567 abiertas) con mesas, sillas y **horario de lunes a jueves y de viernes y sábado, en temporada y fuera de ella**. Cierre más frecuente: 01:00 (3.640) y 01:30 (1.733).
  - Licencias (`…053958.csv`, 114 MB): referencia, tipo y estado de la licencia. No lo he analizado.
  - Histórico: https://datos.madrid.es/dataset/209548-0-censo-locales-historico (no lo he abierto).
- Otros:
  - Inspecciones de locales sujetos a la ley de espectáculos (https://datos.madrid.es/dataset/300160-0-inspecciones-industrias-lepar): no lo he abierto.
  - "Locales de diversión" de esmadrid (300035): licencia propia de Madrid Destino, no CC BY.
- **Frente a Barcelona**: Madrid es **mejor**. Tiene el censo completo, no solo la planta baja, con epígrafe fino y el **horario dentro del mismo censo**, además del horario de las terrazas.

## 5. Obras en la vía pública

- **Incidencias de tráfico en tiempo real** (Informo): https://informo.madrid.es/informo/tmadrid/incid_aytomadrid.xml (HTTP 200, 108 KB). Hoy tiene 111 incidencias, 109 con `es_obras=S`: 95 de mantenimiento, 9 de obras en la vía y 5 de larga duración. Cada una trae **punto (UTM y latitud/longitud), inicio y fin, y descripción** (a veces con el horario: "corte… en horario nocturno de 00:00…"). Se actualiza continuamente. Es lo más parecido al dato diario de Barcelona, aunque es un punto, no un polígono.
- **Obras públicas planificadas y en ejecución**: https://datos.madrid.es/dataset/300538-0-obras-planificadas-ejecucion. El CSV https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/OBRAS/OBRA_PUBLICA/CSV/Obra_publica.csv (modificado el 05/10/2026) tiene **solo 17 obras grandes** (14 en ejecución), con viario afectado, fechas, presupuesto y área. Polígono en SHP: `…/OBRA_PUBLICA/SHPZIP/OBRA_PUBLICA.zip` (no lo he abierto).
- **Licencias de obras en vía pública** (calas, canalizaciones, averías): https://datos.madrid.es/dataset/300375-0-licencias-via-publica. Son **obras ya terminadas**, se publican por trimestre y el último fichero es de enero a junio de 2026. No he comprobado las columnas.
- **Autorizaciones de ocupación de vía de otras administraciones**: CSV trimestral (300376) y capa `GEOPORTAL/AUTORIZACION_OCUPACION_VIA/FeatureServer/0` con 50 polígonos, pero con fechas de 2023–2024 (desfasada).
- **Frente a Barcelona**: hay dato diario con fechas, pero como puntos de Informo, no como polígonos. Faltan las obras privadas (licencias urbanísticas: los conjuntos 640505 "Licencias urbanísticas otorgadas" y 133556 "Declaraciones responsables" son mensuales y no los he abierto).

## 6. Quejas y avisos ciudadanos

- **Avisa Madrid** (https://datos.madrid.es/dataset/212411-0-madrid-avisa): el fichero de 2026 tiene 430.596 avisos con categoría, dirección y **coordenadas** (`COORDENADA_OFICIAL_X/Y`), pero **ninguno de ruido**: solo vía pública (limpieza, contenedores, alumbrado…). Útil para contenedores: 18.016 "Vaciado de cubo o contenedor", con su ubicación.
- **Sugerencias y reclamaciones generales (SYR)** (https://datos.madrid.es/dataset/300044-0-syrg-syrt), fichero "Recibidas desde 2023" (`300044_20261006_054617.csv`, 114 MB): 253.149 filas, del 17/01/2023 al 05/10/2026.
  - **7.060 relacionadas con ruido**:
    - 4.272 "Incidencias empresas de limpieza: maquinaria, ruidos, horarios…"
    - 667 "ruido de camión" de recogida
    - 562 "Ruidos por actos y eventos en el exterior"
    - 222 "Ruidos en la vía pública y horario nocturno"
    - 198 "Ruidos de locales y actividades"
    - 99 "Ruidos en local de ocio"
    - 96 "Terrazas: ruidos"
  - Tienen **dirección en texto** (`DESC_DIREC` = "CALLE X NUM 000005") en 5.295 de las 7.060, más barrio y distrito. **No tienen coordenadas**: hay que cruzarlas con el callejero.
- **Inspecciones ambientales** (https://datos.madrid.es/dataset/300172-0-inspecciones-ambientales), fichero de 2026: 3.013 inspecciones, **1.626 de "RUIDOS"** (más 87 mixtas), con fecha, hora, tipo de actividad y **dirección (calle y número)**. Se publican por trimestre y hay ficheros de años anteriores.
- Policía Municipal (212616): solo totales mensuales por distrito; no hay ruido con dirección.
- **Frente a Barcelona**: Madrid tiene menos (sin coordenadas y con menos volumen que IRIS), pero sirve: las quejas por ruido de la limpieza y la recogida son el equivalente de las "quejas de recogida" de Barcelona.

## 7. Viviendas de uso turístico (VUT)

- **Ayuntamiento, VUT con licencia**: https://datos.madrid.es/dataset/300694-0-viviendas-turisticas-geoportal. El XLSX https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/VIVIENDA/VIVIENDAS_TURISTICAS/VIVIENDAS_USO_TURISTICO.xlsx (07/09/2026) tiene unas **1.037 filas** con `COD_NDP` (se enlaza con las coordenadas del portal), dirección, planta y número de unidades. Son solo las que tienen licencia urbanística, que son muy pocas.
- **Comunidad de Madrid, registro de alojamientos turísticos**: https://datos.comunidad.madrid/dataset/alojamientos_turisticos (CSV, 8.701 filas; en Madrid ciudad hay **4.865 "viviendas de uso turístico"**, más hoteles, hostales…). Tiene dirección (vía, número, planta, puerta) **sin coordenadas**. Licencia CC BY.
- Comunidad, declaraciones responsables de VUT: https://datos.comunidad.madrid/dataset/declaraciones_actividad_viviendas_uso_turistico (1.117 en Madrid; dirección sin coordenadas).
- Pendiente de comprobar: Inside Airbnb (anuncios con coordenadas, otra licencia) y el Registro Único de Arrendamientos del Ministerio.
- **Frente a Barcelona**: peor. Hay muchas menos viviendas registradas y sin coordenadas; habría que geocodificarlas con el callejero.

## 8. Patio de manzana o fachada interior

- **Lo resuelve el propio MER 2021**: el ráster de 5 m tiene valor en los patios (unos 35 dB) y 0 en los edificios. Tomando el píxel justo delante de cada fachada se sabe si la ventana da a la calle o al patio, y con qué nivel.
- Apoyos:
  - **Manzanero** (recintos de manzana): https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/CARTOGRAFIA/CARTOGRAFIA_ACTUALIZADA/MANZANERO/MANZANERO.zip (HTTP 200, 10 MB, 22/04/2026; no lo he abierto).
  - **Alturas de edificios**: …/ALTURAS_EDIFICIOS/ALTURAS_EDIFICIOS.ZIP (HTTP 200, 50 MB; no lo he abierto).
  - **Modelo 3D de edificios** (LOD2): …/3D_EDIFICACIONES_CONSTRUCCIONES/01_EDIFICIO_P.zip. Devuelve una redirección 302 que no he seguido.
  - Cartografía 1:1000 por distritos en SHP (213565).
- No encontré un mapa oficial por fachada (el proyecto MAdB de 2020 lo hizo a partir del MER 2016 de 10 m; es de un tercero).

## 9. Anchura de calle

- **Ancho medio de viario** (https://datos.madrid.es/dataset/300715-0-ancho-viario-mapas): capa `sigma.madrid.es/hosted/rest/services/CARTOGRAFIA/ANCHO_MEDIO_VIARIO/MapServer/0`, con **30.267 tramos de calle (subviales)**.
  - Campos: `SVIA_ID, VIAS, MIN_IMPAR, MAX_IMPAR, MIN_PAR, MAX_PAR, Ancho_medio`, es decir, el tramo de numeración y el ancho.
  - Ejemplos: Gaztambide 7,4 m, Marqués de Urquijo 7,9 m, Princesa 12,5 m y Alberto Aguilera 16,1 m.
  - Parece el **ancho de la calzada**, no de fachada a fachada. Se calcula como área / perímetro × 2.
- **Ancho medio de acera**: `CARTOGRAFIA/ANCHO_MEDIO_ACERA`, con 91.403 polígonos.
  - Calzada + aceras ≈ ancho de fachada a fachada (cálculo pendiente).
- **Número de carriles**: `GEOPORTAL/NUMERO_DE_CARRILES`, con 17.023 líneas (`name, N_CARRILES`).
- **Frente a Barcelona**: mejor. En Barcelona se estimaba con los portales; aquí viene medido de la cartografía.

## 10. Extras

- **ZPAE (zonas de protección acústica especial)**: capa `sigma.madrid.es/hosted/rest/services/MEDIO_AMBIENTE/ZPAE/MapServer`, con 4 ámbitos poligonales: **Centro, Gaztambide, Trafalgar-Ríos Rosas y AZCA-Av. de Brasil** (Aurrerá no aparece).
  - La capa 4 ("Detalle clasificación") tiene 2.590 tramos clasificados, pero el campo `ZonaSupera` solo dice "Consultar normativa". La clasificación alta, moderada o baja está en la simbología o en otro campo; pendiente de comprobar.
  - Zonificación acústica: `AREAS_ACUSTICAS_2018`, con 298 polígonos (`NOMBRE, USO, TIPO`).
- **Tráfico con perfil horario**:
  - Histórico desde 2013 (https://datos.madrid.es/dataset/208627-0-transporte-ptomedida-historico): un ZIP por mes. El de septiembre de 2026 pesa 92,6 MB y tiene un CSV de 784 MB con **13.152.123 filas cada 15 minutos**. Columnas: `id;fecha;tipo_elem;intensidad;ocupacion;carga;vmed;error;periodo_integracion`.
  - Ubicación de los puntos (https://datos.madrid.es/dataset/202468-0-intensidad-trafico): **5.083 puntos** con coordenadas UTM y latitud/longitud.
  - Tiempo real cada 5 minutos: https://informo.madrid.es/informo/tmadrid/pm.xml (no lo he abierto).
  - Esto **compensa en parte la falta de sensores de ruido por hora**: da el perfil horario de cada calle con tráfico.
  - También hay intensidad media diaria por tramos (203962) y velocidad media (300340); no los he abierto.
- **Residuos**:
  - Contenedores: https://datos.madrid.es/dataset/300276-0-contenedor-papel-carton-todos (CSV de marzo de 2026: **44.252 contenedores** con coordenadas y tipo de carga). Por tipo: 10.861 resto, 9.169 envases, 8.345 papel, 8.215 orgánica y **7.659 vidrio**.
  - **No he encontrado horarios de recogida por calle**: "Recogida de residuos" (300143) son solo toneladas por trimestre. Habría que pedirlos por transparencia, como en Barcelona.
- **Plan de acción contra el ruido**: no lo he buscado a fondo; pendiente de comprobar.
- **Calidad del aire y meteorología por hora** desde 2001/2019 (201200, 300352): no es ruido; pueden servir de contexto.

## Qué falta frente a Barcelona

- **Sensores por hora**: no se publican. Solo hay día, tarde y noche por día. Opciones: pedirlos por transparencia o modelar la hora con el tráfico cada 15 minutos.
- **Mapa por tramo vectorial o por fachada**: no hay, pero el ráster de 5 m es mejor base.
- **Quejas con coordenadas**: solo con dirección en texto; hay que geocodificar con el callejero.
- **VUT con coordenadas**: solo unas 1.000 con licencia (que sí se ubican); el registro de la Comunidad (4.865) viene sin coordenadas.
- **Horarios de recogida de basura**: no publicados.
- **Obras privadas en curso**: solo licencias mensuales y licencias de calas ya terminadas.

## Sin comprobar

- Convención de fecha de la franja de noche en los datos diarios.
- Altura de cálculo del MER 2021 y licencia escrita en su ficha.
- Datos de MITECO/SICA de Madrid (fase 4).
- Columnas de licencias de obras en vía pública, licencias urbanísticas y declaraciones responsables.
- SHP de obras públicas, Manzanero, alturas y 3D.
- XML de tráfico en tiempo real.
- Clasificación alta, moderada o baja de las ZPAE.
- Inside Airbnb.
- Plan de acción contra el ruido.
