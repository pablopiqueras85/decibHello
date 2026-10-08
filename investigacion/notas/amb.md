# Datos abiertos de ruido: Área Metropolitana de Barcelona

Revisado el 6 de octubre de 2026. Todo lo que lleva una cifra se ha comprobado consultando la API o descargando el fichero desde aquí. Si algo no se pudo comprobar, se dice.
Descargas: `scratchpad/descargas-amb/`.

## Resumen en 10 líneas

1. **La gran fuente es la Generalitat**: tiene un servicio WFS abierto (`https://sig.gencat.cat/ows/ATMOSFERA/wfs`) con los **mapas estratégicos de ruido de todas las aglomeraciones** del área. Responde con 200, sin captcha y en GeoJSON.
   - **Por tramo de calle, 2018, en dB exactos** (no en franjas de 5 dB): Ld/Le/Ln para Badalona (2.967 tramos), Santa Coloma (822), Sant Adrià (482), Cornellà (1.138), Terrassa (4.674), Sabadell (4.727)… y también Barcelona (17.947), lo que permite comparar con el mapa de Barcelona que ya usamos.
   - **Isófonas 2022 (publicadas en 2023)**, en franjas de 5 dB: Ld, Le, Ln y Lden, separadas por foco (tráfico, tren, industria, **ocio**, avión y total). Cubren L'Hospitalet, el Barcelonès (Badalona, Santa Coloma y Sant Adrià), el Baix Llobregat I y II y el Vallès Occidental I y II.
   - **L'Hospitalet por tramo**: solo hay datos de 2012 (1.939 tramos, Ld/Le/Ln en dB). Para 2018 no hay tramos; para 2022 hay isófonas.
2. **Sant Cugat no es aglomeración**: no tiene mapa estratégico. Solo tiene el mapa de capacidad acústica (los objetivos de cada zona, no niveles medidos) y 6 sensores de la Diputació.
3. **Sensores con datos en directo**: Terrassa tiene 48 (36 con dato hoy), Sant Cugat 6 (5 con dato hoy) y Badalona 5 (ninguno con dato hoy). Solo se ve el último valor. **No hay histórico por hora abierto**: hay que pedirlo.
4. **Portales con coordenadas**:
   - L'Hospitalet: 23.024 portales (CSV, con referencia catastral).
   - Badalona: 28.242 (WFS, con referencia catastral).
   - Sant Cugat: 13.968 puntos con el número de domicilios (GeoJSON).
   - Toda Cataluña: el geocodificador del ICGC funciona portal a portal.
5. **Locales y bares**: no hay censo a nivel de punto en L'H, Badalona ni Sant Cugat. El censo GIA-DIBA no incluye a ninguno de los tres.
6. **Pisos turísticos**: el registro de la Generalitat cubre todos los municipios, pero **solo con la dirección, sin coordenadas**. L'Hospitalet lo republica con coordenadas (707 de 710).
7. **Obras**: no hay ninguna fuente diaria. La capa de L'H es de 2017–2019. La de Sant Cugat (ocupación de vía pública) pide autorización (401).
8. **Quejas por ruido con ubicación**: no hay nada equivalente a IRIS. Lo más parecido son las incidencias de limpieza de L'H (diarias y con coordenadas; 8 son de "Soroll" y 163 de "Festa popular" en 2026).
9. **Bloqueos** (ninguno es un captcha; son bloqueos de red o de IP):
   - Badalona: la web municipal da 403 de CloudFront.
   - Catastro: 403, "acceso denegado desde su dirección IP".
   - datacloud.icgc.cat: la conexión se corta.
   - Overpass/OSM: 406 y luego corte.
   - En ningún caso se ha intentado saltar el bloqueo.
10. **Perfiles horarios de Barcelona**: parece razonable reutilizarlos en L'H, Badalona y Santa Coloma (tejido denso parecido). En Sant Cugat hay que tener cuidado. Terrassa y Sant Cugat tienen sensores para comprobarlo si se consigue el histórico.

---

## 1. Fuentes supramunicipales

### 1.1 Generalitat: WFS/WMS "ATMOSFERA" (mapas de ruido y de capacidad acústica). **La más importante.**

- **WFS**: `https://sig.gencat.cat/ows/ATMOSFERA/wfs`. Funciona (HTTP 200), es un GeoServer y acepta `outputFormat=application/json`, `CQL_FILTER` y `srsName=EPSG:4326`. El sistema de coordenadas nativo es EPSG:25831.
- **WMS**: `https://sig.gencat.cat/ows/ATMOSFERA/wms` (465 nombres de capa).
- **Ficha IDEC**: `https://catalegs.ide.cat/geonetwork/srv/cat/csw?...&id=atmosfera-wfs`.
- **Licencia**: los metadatos remiten al "Avís legal gencat.cat", que permite reutilizar citando la fuente. Los metadatos no dicen "CC BY 4.0" de forma explícita: **conviene confirmarlo**.
- Ejemplo de consulta:
  `...wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=ATMOSFERA:ATMOSFERA_MES_SUPRAMUN_2018&outputFormat=application/json&srsName=EPSG:4326&CQL_FILTER=CODI_INE='08015'`

| Capa (prefijo `ATMOSFERA:ATMOSFERA_`) | Qué es | Formato | Registros comprobados |
|---|---|---|---|
| `MES_SUPRAMUN_2018` | Mapa estratégico 2018 por **tramo de calle**, aglomeraciones supramunicipales | Líneas. Columnas `TOTDIA`/`TOTVES`/`TOTNIT`/`TOTDEN` = Ld/Le/Ln/Lden en **dB enteros**. Además, desglose por foco: `TVL*` tráfico, `TFL*` tren, `TAL*` avión, `INL*` industria, `OCL*` ocio, `GE*` grandes ejes, `INT*` | 45.853 en total. Barcelona 08019: 17.947 · Sabadell: 4.727 · Terrassa: 4.674 · **Badalona 08015: 2.967** (Ld 47–74, Le 44–72, Ln 33–68; unos 297 km) · Cornellà: 1.138 · Santa Coloma: 822 · Sant Adrià: 482 · El Prat, Esplugues, Sant Joan Despí, Sant Feliu, Sant Boi, Viladecans, Castelldefels, Ripollet, Barberà… · **L'Hospitalet: 0** |
| `MAPA_SOROLL_2018` | Lo mismo, solo para el Baix Llobregat II | Líneas, mismas columnas | 4.101 (Sant Boi, Viladecans, Castelldefels) |
| `MES_MUNICIPAL_2018` | Aglomeraciones municipales | Líneas | 7.062 (solo Lleida, Mataró y Reus) |
| `MAPA_SOR_2012_VW`, `SOROLL_LD_2012`, `SOROLL_LN_2012`, `SOROLL_LDEN_2012` | Mapa 2012 por tramo | Líneas. `TOTDIA`/`TOTVES`/`TOTNIT`/`TOTDEN` en dB y desglose por foco | **L'Hospitalet: 1.939 tramos** · Badalona: 2.799 · Barcelona: 16.242 · Terrassa: 4.702 · Sabadell: 4.694 |
| `SOROLL_MUNI_{T,V,F,I,O,A}_2023` | Isófonas del mapa 2022 (fase 4). T = total, V = tráfico, F = tren, I = industria, **O = ocio**, A = avión | Multipolígonos disueltos, uno por franja e indicador. `INDEX_LD`/`INDEX_LE`/`INDEX_LN`/`INDEX_LDEN` en franjas de 5 dB (Ld/Le/Lden desde 55–60 hasta ≥75; Ln desde 50–55 hasta ≥70). Por debajo de 55 (Ln < 50) no hay polígono | T: 241 polígonos. **L'H tiene los 20** (Ld/Le/Ln/Lden × 5 franjas; unos 7,9 MB en JSON). El Barcelonès (Badalona, Santa Coloma, Sant Adrià) también tiene 20. Se probó con un punto: Badalona junto a la C-31 sale en Ln ≥70 y el centro de Santa Coloma en Ln 55–60 |
| `AGLO_SOROLL_2022` | Límites de las 12 aglomeraciones y enlaces a la memoria y a la aprobación en el DOGC | Polígonos | 12. Barcelona, **l'Hospitalet** (municipal), **Barcelonès** (supramunicipal), Baix Llobregat I y II, Vallès Occidental I y II, Mataró, Gironès, Tarragonès, Lleida y Reus. **Sant Cugat no está en ninguna** |
| `MCA_ZONES_ACUSTICA` | Mapa de capacidad acústica: sensibilidad de cada zona (A alta, B moderada, C baja), con subtipos | Multilíneas disueltas | 2.897 en 593 municipios. L'H: 6 · Badalona: 6 · **Sant Cugat: 8** · Santa Coloma: 6 · Sant Adrià: 6 · Cornellà: 8 · Terrassa: 6 · Sabadell: 7 |
| `MCA_ZONES_SOROLL` | "Zonas de ruido" del mapa de capacidad (alrededor de infraestructuras), con un valor Ln/Ld | Polígonos | 361. Sabadell: 9 · Sant Adrià: 2 · Cornellà: 2. **No hay para L'H, Badalona ni Sant Cugat** |
| `SOROLL_CAR_*17_22` | Carreteras de la Generalitat: tramos con población expuesta | Líneas, **sin dB por punto** | 155 en total; 4 cerca de Sant Cugat (C-58, C-1413a, BP-1413, BP-1503) |
| `ZONA_QUAL_ACUSTICA` | Zonas de especial protección (ZEPQA) | Polígonos | 4 (El Papiol, etc.) |

**Qué falta frente a Barcelona**:
- **Mapa por fachada**: no lo hay.
- **Año**:
  - Los tramos más recientes son de 2018. Para L'H, son de 2012.
  - Las isófonas de 2022 van en franjas de 5 dB y no están asignadas a la calle; hay que cruzar cada portal con los polígonos.
- **Precisión**: los tramos de 2018 dan el valor en dB enteros, más fino que las franjas de 5 dB de Barcelona 2017.
- **Comparación con Barcelona**: la misma capa incluye Barcelona. Así se puede medir el desfase entre el mapa de la Generalitat y el de Barcelona, y validar con nuestros sensores antes de usarlo fuera.

**Memorias (PDF)**, enlazadas en `AGLO_SOROLL_2022`:
- L'Hospitalet: `https://accioclimatica.bibliotecadigital.gencat.cat/handle/20.500.14343/1316`
- Barcelonès: `.../20.500.14343/391`
- Baix Llobregat I: `.../417`
- Vallès Occidental I: `.../316`
- Vallès Occidental II: `.../317`

No las he abierto.

### 1.2 Generalitat: registro de pisos turísticos (Registre de Turisme de Catalunya)

- **Dónde**: `https://analisi.transparenciacatalunya.cat/resource/t2h3-cgys.json` (Socrata, HTTP 200). Se actualizó el 5 de octubre de 2026.
- **Registros**: 112.696 en toda Cataluña, de los que 104.502 son "Habitatges d'ús turístic". Todos están en estado "Alta".
- **Columnas**: tipo, número de inscripción, rótulo, dirección (tipo de vía, nombre, número, piso, puerta), código postal, municipio, `referencia_cadastral`, plazas, titular…
- **Coordenadas: no tiene.** La columna `referencia_cadastral` está casi siempre vacía.

| Municipio | Pisos turísticos | Con referencia catastral |
|---|---|---|
| L'Hospitalet | 520 | 166 |
| Badalona | 223 | 19 |
| Sant Cugat | 97 | 13 |
| Santa Coloma | 56 | 44 |
| Sant Adrià | 267 | 33 |
| Cornellà | 89 | 20 |
| Terrassa | 153 | 21 |
| Sabadell | 65 | 9 |

- **Cómo usarlo**: geocodificar la dirección con los portales municipales o con el ICGC.
- **Licencia**: "See Terms of Use", lo que en Socrata de la Generalitat equivale a reutilización con atribución. Sin comprobar más allá.

### 1.3 Diputació de Barcelona: sensores de ruido (Sentilo)

- **Dónde**: catálogo público en `https://sentilo.diba.cat/sentilo-catalog-web/component/map/json?ct=noise`. Responde 200, pero hace falta primero la cookie de sesión de la página `component/map` y la cabecera `X-Requested-With`.
- **Cuántos**: 205 componentes de ruido en la provincia.
  - **Sant Cugat (08205)**: 6 sonómetros CESVA TA120. 5 dieron un valor el 6 de octubre de 2026, campo `-N` = nivel en dB(A).
  - **Badalona (08015)**: 5 CESVA, en Av. Alfons XIII/Maresme, Rambla Sant Joan 27, Francesc Layret 130, Via Augusta (Hospital) y Pomar de Baix. **Ninguno tenía dato reciente.**
  - L'H, Santa Coloma, Sant Adrià y Cornellà: 0.
- **Último valor de cada sensor**: `/sentilo-catalog-web/component/map/{id}/lastOb`.
- **Histórico por hora**: la API de Sentilo (`api-sentilo.diba.cat`) devuelve 401 (hace falta un token). Hay que **pedirlo a la Diputació** (Smart Region / Gerència d'Habitatge, Urbanisme i Activitats).
- No encontré el histórico en dadesobertes.diba.cat: el buscador funciona con JavaScript y no sirvió. Queda **sin comprobar**.
- **Licencia**: sin comprobar.

### 1.4 Diputació de Barcelona: censo de actividades GIA

- **Dónde**: Socrata `txvw-xc3g`, con 42.084 actividades, coordenadas y código CCAE. Licencia ODC-BY.
- **No sirve aquí**: ninguno de los 189 ayuntamientos que lo usan es L'H, Badalona, Sant Cugat, Santa Coloma, Sant Adrià, Cornellà, Terrassa ni Sabadell.

### 1.5 AMB

- **Geoportal**: `https://geoportal.amb.cat/geoserveis/rest/services?f=json` (ArcGIS 11.5, HTTP 200).
  - **No tiene capas de ruido.**
  - `indicadors_activitat_economica` tiene la capa "Restaurants i bars (BiR/ha), 2017", que es una densidad por zona, no locales sueltos.
  - `topografia_1000` (consulta activada, 2.000 registros por petición) tiene polígonos de edificación ("Poblament") de toda el AMB. Serviría para estimar patios y anchura de calle, pero los datos vienen de CAD y la codificación por `Nivell` está sin estudiar.
- **API de datos abiertos**: `https://opendata.amb.cat/{colección}/search` (JSON, 279 conjuntos).
  - `projectes_obres` tiene 210 proyectos metropolitanos (parques, urbanización), con fichas pero sin fechas diarias. **No sirve como "obras en curso".**
  - Licencia: "Autorització segons Llei 37/2007".

### 1.6 ICGC

- **Geocodificador**: `https://eines.icgc.cat/geocodificador/cerca?text=...` (HTTP 200, JSON). Devuelve las coordenadas del portal, el código INE de la vía y el código postal.
  - Probado con Progrés 56 y Francesc Layret 130 de Badalona, Rambla del Celler 50 de Sant Cugat y Rambla Just Oliveras 10 de L'H. Todos dan un punto en el portal.
- **Adreces municipals v2.2** (abril de 2026, licencia CC BY 4.0): toda Cataluña en GPKG, GDB, SHP y GML.
  - Enlace: `https://datacloud.icgc.cat/datacloud/adreces/gpkg/adreces-v2r2-20260410-gpkg.zip`.
  - **Desde aquí la conexión se corta** (error 35 de curl, el proxy cierra el túnel). No es un captcha. **El usuario puede bajarlo a mano.** El tamaño está sin comprobar.

### 1.7 Catastro (INSPIRE: direcciones, parcelas, edificios)

- **Bloqueado**: `www.catastro.hacienda.gob.es/INSPIRE/...` y `ovc.catastro.meh.es` responden 403 con "Hemos denegado el acceso desde su dirección IP (código -10)". Es un bloqueo por IP, no un captcha.
- **Qué descargar a mano**: el ATOM INSPIRE de la provincia 08: Addresses (`.../INSPIRE/Addresses/08/ES.SDGC.AD.atom_08.xml`), y también CadastralParcels y Buildings, para L'H (08101), Badalona (08015) y Sant Cugat (08205).
- **Para qué sirve**: patios interiores (parcela frente a huella del edificio) y anchura de calle.
- **Atajo en Badalona**: el GeoServer municipal ya sirve una copia de las parcelas catastrales (ver 3.3).

### 1.8 OpenStreetMap (bares y discotecas como sustituto)

- Overpass (`overpass-api.de`) respondió 406 y luego cortó la conexión. **Sin comprobar.**

---

## 2. L'Hospitalet de Llobregat (prioridad 1)

El catálogo municipal está en el CKAN de la AOC: `https://dadesobertes.seu-e.cat/api/3/action/package_search?fq=organization:hospitaletdellobregat`. Responde 200 y tiene 60 conjuntos. La web `dadesobertes.l-h.cat` solo enlaza.

| # | Fuente | URL / acceso | Qué hay de verdad | Licencia | Actualización | Falta frente a BCN |
|---|---|---|---|---|---|---|
| 1 | Mapa de ruido | Generalitat WFS (1.1). Tramos: `MAPA_SOR_2012_VW` con `CODI_INE='08101'`. Isófonas: `SOROLL_MUNI_*_2023` con `AGLO='l''Hospitalet de Llobregat'` | Tramos de **2012** (1.939, Ld/Le/Ln en dB). **Isófonas de 2022** Ld/Le/Ln/Lden en franjas de 5 dB, por foco (también ocio: 9 polígonos) | Avís legal gencat | Fase 4 (2022), publicada en 2023 | No hay tramos recientes ni fachadas |
| 2 | Sensores | — | **No hay** en Sentilo DIBA. En el portal solo está la calidad del aire (`qualitat_aire.csv`: NO2, SO2…; 57.631 filas diarias desde 1991, **sin ruido**) | — | — | Faltan los 176 sensores. Usar los perfiles de BCN |
| 3 | Portales | CKAN `hospitaletdellobregat-carrers-i-adreces` → `territori_adreces.csv` (9,5 MB) | **23.024 portales**, todos con Latitud/Longitud (coma decimal) y `FincaCadastral`, barrio, sección censal. Además, 579 calles como LINESTRING (`territori_noms_carrers.csv`) | CC BY-ND (cuidado: "sin obras derivadas") | Diaria según CKAN (las fechas de modificación de la muestra son de 2019) | Equivalente |
| 4 | Locales / ocio nocturno | — | **No hay censo de actividades.** Solo 30 hoteles, 20 apartamentos turísticos, etc. en el fichero de alojamientos | — | — | Falta el censo y los horarios. Pedir por transparencia |
| 5 | Obras | Geoportal: `https://geoportal.l-h.cat/CartoAPI.ashx?request=getlayer&layer=INV_OBRES&srid=4326&format=GEOJSON` (200) | 181 obras con polígono, estado y fechas, **pero son contratos de 2017–2019**. La web "En aquests moments" (`enaquestsmoments.l-h.cat`) da 503 | CC BY-ND (geoportal) | Parada | No sirve para obras en curso |
| 6 | Quejas | CKAN `hospitaletdellobregat-incidencies-de-neteja-finalitzades` → `incidencies_neteja_any_actual.csv` | 13.679 incidencias del 1 de enero al 5 de octubre de 2026, con fecha, **hora**, coordenadas y motivo. Por ruido: **"Soroll" 8**, "Festa popular" 163. Hay años desde 2016 | CC BY-ND | Diaria | Son solo de limpieza; no hay quejas de ruido de vecinos (IRIS) |
| 7 | Pisos turísticos | CKAN `hospitaletdellobregat-establiments-d-allotjament-turistic` → `gencat_allotjaments_turistics.csv` | 710 (520 pisos turísticos, 140 llars compartides…), **707 con Latitud/Longitud** | ODC-BY | Diaria | Equivalente |
| 8 | Patios | Catastro bloqueado (1.7). AMB `topografia_1000` (1.5) | Sin hacer | — | — | Falta |
| 9 | Anchura de calle | Se puede estimar con portales + ejes de calle | Sin hacer | — | — | Igual que en BCN |
| 10 | Extras | Contenedores (`geoinventari_contenidors.csv`: 4.047 con coordenadas, CC BY), para el aviso de recogida de basuras. Mapa de capacidad acústica en el WFS de la Generalitat (`MCA_ZONES_ACUSTICA`, 6 zonas). Límites de distritos y barrios en SHP | | | | |

---

## 3. Badalona (prioridad 2)

**Bloqueo**: `www.badalona.cat` (y `/dadesobertes`) devuelve **403 "The request could not be satisfied" de CloudFront** desde esta red. No es un captcha, es un bloqueo de red. No se ha intentado saltar.
- Qué puede hacer el usuario: abrir `https://www.badalona.cat/dadesobertes` en su navegador y mirar si hay censo de actividades, obras o quejas.
- Badalona no está en el CKAN de la AOC.

**El geoportal sí responde**: `https://geoportal.badalona.cat/geoserver/ows` (GeoServer, WFS 200, 78 capas). La licencia no se indica: **sin comprobar**.

| # | Fuente | URL / acceso | Qué hay de verdad | Falta frente a BCN |
|---|---|---|---|---|
| 1 | Mapa de ruido | WFS de la Generalitat | **Tramos 2018**: 2.967 en dB (Ld, Le, Ln y Lden; tren en 53 tramos). Tramos 2012: 2.799. Isófonas 2022 del Barcelonès | Fachadas. En tramos, mejor que BCN (año 2018 y dB exactos) |
| 2 | Sensores | Sentilo DIBA (1.3) | 5 CESVA con dirección, **sin dato reciente** | No hay histórico. Pedirlo a la Diputació o al Ayuntamiento |
| 3 | Portales | WFS `badalona:portals` (también `smart_city:Adreces`) | **28.242 portales** con lat/lon, `refcat` (catastro) y calificación urbanística | Equivalente |
| 4 | Locales | WFS `badasud:establiments` | Solo 358 establecimientos del polígono Badalona Sud (venta al por mayor, etc.). **No hay censo de bares** | Falta |
| 5 | Obras | WFS `badalona:inversions_new` | 32 inversiones (obras de 2015 con fase y presupuesto). Desfasado | Falta lo diario |
| 6 | Quejas | — | Nada encontrado (la web principal está bloqueada) | Falta |
| 7 | Pisos turísticos | Registro de la Generalitat (1.2) | 223, solo con dirección. En el geoportal, `badalona_gp:huts` son 2 ámbitos de planeamiento (MPGM de pisos turísticos), no pisos | Geocodificar con los portales |
| 8 | Patios | WFS `badalona_gp:parcela` (16.268 parcelas catastrales con `refcat`), `badalonagu:topo_edificis` (80.803 polígonos de edificios del topográfico 2019) y `badalonagu:illes_25831` (manzanas) | Material suficiente para calcular el interior de manzana | Aún sin calcular |
| 9 | Anchura de calle | WFS `badalona:voreres_3momes`: 2.889 tramos de acera con `amplada` (cm) y tipo. `badalona:calcada`: 2.682 polígonos de calzada con superficie | Mejor que BCN (hay anchura real de acera) | — |
| 10 | Extras | Mapa de capacidad acústica (Generalitat, 6 zonas). En el WFS, `badalona:papereres_2016/2017` | | Recogida de basuras: nada |

---

## 4. Sant Cugat del Vallès (prioridad 3)

- **CKAN de la AOC**: solo 2 conjuntos ("Guia de carrers": `https://dadesobertes.seu-e.cat/csv/santcugatdelvalles/carrers.csv`, CC BY; y solicitudes de acceso a la información).
- **No resuelven** (DNS): `opendata.santcugat.cat` ni `dadesobertes.santcugat.cat`. La página "dades obertes" del Ayuntamiento no lleva a ningún catálogo.
- **El geoportal municipal sí funciona**: `https://geociutat.santcugat.cat/apps/giscube-admin/geoportal/category/catalog/` (JSON con 312 capas).

| # | Fuente | URL / acceso | Qué hay de verdad | Falta frente a BCN |
|---|---|---|---|---|
| 1 | Mapa de ruido | **No existe** mapa estratégico (no es aglomeración). Solo el mapa de capacidad acústica: Generalitat `MCA_ZONES_ACUSTICA` (8 zonas A/B/C) o el municipal en teselas `.../qgisserver/services/ma_capacitat_acu/tilecache/{z}/{x}/{y}.png` | El WMS municipal (`ma_capacitat_acustica`) responde a GetFeatureInfo, pero oculta los atributos (`properties: null`). La capacidad acústica es un objetivo legal, **no un nivel medido** | Grave: no hay niveles por calle. Opciones: sensores + carreteras (`SOROLL_CAR_*`: C-58, C-1413a, BP-1413, BP-1503, solo población expuesta) o un modelo propio. Por la web: informe de ruido de la Festa Major 2025 en PDF (`/files/651-24109-fitxer/Informe_control_soroll_FM_2025_anonimitzat.pdf`, sin abrir) |
| 2 | Sensores | Sentilo DIBA (1.3), 6 CESVA TA120 (alrededor de Rambla del Celler, Plaça Octavià y Valldoreix) | 5 con dato el 6 de octubre de 2026 (p. ej. 44,0 y 48,0 dB). Solo el último valor | El histórico pide token. **Pedirlo** |
| 3 | Portales | GeoJSON `https://geociutat.santcugat.cat/apps/giscube-admin/layerserver/geojsonlayers/bru_portals_locals` (5,5 MB) | **13.968 puntos** (`nom_vial`, `numero`, `nombre_domicilis` = 40.725 domicilios; `tipus_local`: 13.917 habitatge, 51 col·lectiu; barrio) | Sin referencia catastral. Licencia sin comprobar |
| 4 | Locales | — | Solo "activitats SQM" (medio ambiente), sin revisar. **No hay censo de bares** | Falta |
| 5 | Obras | API de ocupación de vía pública `https://aupacaux.apps.santcugat.cat/api/GetOvpGeomByDates` | **401 "not authorized"** (necesita sesión; no es anti-robots) | Falta. Se podría pedir acceso |
| 6 | Quejas | — | Nada | Falta |
| 7 | Pisos turísticos | Registro de la Generalitat | 97, solo con dirección | Geocodificar |
| 8–9 | Patios y anchura | WMS "Any construcció parcel·les cadastrals"; Catastro (bloqueado) | Sin hacer | — |
| 10 | Extras | Capas de residuos (voluminosos, puntos de reciclaje) en GeoJSON; "Músics de carrer" (`ovp_musics_carrer`) | | |

---

## 5. De paso: otros municipios

- **Terrassa**:
  - Mapa: tramos 2018 (4.674) e isófonas 2022 (Vallès Occidental II).
  - **Sentilo municipal público**: `https://sentilo.terrassa.cat/sentilo-catalog-web/component/map/json` devuelve 1.447 componentes, **48 de ruido** (CESVA, dBelectronics y otros). **36 tenían dato el 6 de octubre de 2026** (LAeq, L10, L90…; algunos guardan audio FLAC).
  - El último valor se ve con `/component/map/{id}/lastOb`. El histórico está sin comprobar (la API pide token).
  - Es la mejor candidata para validar los perfiles horarios de BCN.
- **Sabadell**:
  - Mapa: tramos 2018 (4.727); isófonas del Vallès Occidental I; zonas de ruido del mapa de capacidad (9).
  - Visor municipal: `https://planol.sabadell.cat/Planol/inici?code=ma`, sin probar.
  - `opendata.sabadell.cat` no resuelve.
- **Santa Coloma de Gramenet**:
  - Mapa: tramos 2018 (822) e isófonas del Barcelonès.
  - CKAN de la AOC con 34 conjuntos, casi todos estadísticos. Lo más útil: "Qualificació del sòl" y "Tipus d'activitat econòmica" (agregado).
- **Sant Adrià de Besòs**: tramos 2018 (482), isófonas del Barcelonès, 267 pisos turísticos. No hay nada en el CKAN.
- **Cornellà**: tramos 2018 (1.138) e isófonas del Baix Llobregat I.

---

## 6. ¿Se pueden reutilizar los perfiles horarios de Barcelona?

- **L'Hospitalet, Badalona (centro y Gorg), Santa Coloma y Sant Adrià**: es razonable. El tejido urbano es continuo con Barcelona, con calles densas, tráfico parecido y el mismo horario de actividad. Las isófonas de la Generalitat dan Ld, Le y Ln por separado, así que el desfase entre día y noche ya viene del mapa. El perfil de BCN solo repartiría el nivel dentro de cada franja, igual que hacemos ahora.
- **Sant Cugat**: con más cuidado. Es un tejido más residencial y de baja densidad, con más diferencia entre noche y día, y sin mapa de niveles. Habría que calibrar con sus 6 sensores (si se consigue el histórico) antes de dar notas.
- **Cómo validarlo sin sensores propios**: los tramos 2018 de la Generalitat incluyen Barcelona (17.947). Primero se mide cuánto se desvían de los sensores de BCN y del mapa de BCN 2017. Después se aplica la misma corrección en Badalona y los demás.

---

## 7. Qué tendría que descargar o pedir el usuario a mano

1. **Catastro INSPIRE**, provincia 08: Addresses, CadastralParcels y Buildings. Bloqueado por IP desde aquí. ATOM: `https://www.catastro.hacienda.gob.es/INSPIRE/Addresses/08/ES.SDGC.AD.atom_08.xml` (y los equivalentes `/CadastralParcels/08/` y `/Buildings/08/`).
2. **ICGC Adreces v2.2**: `https://datacloud.icgc.cat/datacloud/adreces/gpkg/adreces-v2r2-20260410-gpkg.zip`. La conexión se corta desde aquí; no se sabe si es por la red o por el servidor.
3. **Web de Badalona**, `https://www.badalona.cat/dadesobertes`: 403 de CloudFront desde aquí. Revisar en el navegador si hay censo de actividades, obras o quejas.
4. **Solicitudes de transparencia** (como las de BCN):
   - Histórico horario de los sensores de la Diputació en Sant Cugat y Badalona, y de Terrassa.
   - Censo de actividades con licencia de bar o música en L'H, Badalona y Sant Cugat.
   - Obras en la vía pública en curso.
   - Quejas por ruido con ubicación.

## 8. Sin comprobar

- La licencia exacta de los WFS de la Generalitat ("Avís legal", pendiente de confirmar como CC BY).
- Las licencias del GeoServer de Badalona y del geoportal de Sant Cugat.
- El contenido de las memorias en PDF del mapa estratégico y del informe de la Festa Major de Sant Cugat.
- Si existe un histórico de sensores en dadesobertes.diba.cat.
- Los recuentos de OSM (Overpass falló).
- El tamaño del GPKG del ICGC.
- La capa "activitats SQM" de Sant Cugat.
- La anchura de calle y los patios: los datos existen, pero no se ha calculado nada.
