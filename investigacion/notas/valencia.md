# València: datos abiertos para DecibHello

Revisado el 6 de octubre de 2026. Todo lo que lleva cifras se ha comprobado consultando la API o descargando el fichero. Lo que no se pudo comprobar dice "sin comprobar".

Las descargas están en `scratchpad/descargas-valencia/` (ckan/, geo/, sens/, gva/, osm/, web/).

## Resumen en 10 líneas

- **Portal municipal**: https://opendata.vlci.valencia.es (CKAN, 279 conjuntos). La API funciona (200). `datastore_search` sí; `datastore_search_sql` **no existe** ("Action name not known").
- **Casi todo lo geográfico está en el geoportal** (ArcGIS Server): `https://geoportal.valencia.es/server/rest/services/OPENDATA/...`. Consultas por punto, por atributos y conteos funcionan sin clave. Máximo 2.000 registros por petición (hay que paginar).
- **Licencia**: CC BY 4.0 en todo lo del portal municipal y en lo de la GVA. Igual que Barcelona.
- **Mapa de ruido**: hay 2012, 2017 y 2022 (fase 4), pero solo como **isófonas** (manchas de 5 dB), no por tramo de calle ni por fachada. **Ojo: el "Mapa Ruido" del portal de datos abiertos es el de 2012**, no el actual.
- **Sensores**: solo **16 sonómetros en Russafa** con datos abiertos, **diarios** (Ld, Le, Ln, Lden), desde 2020. No hay datos por hora ni por minuto abiertos. Los 22 sonómetros de ocio (Cánovas, Cedro, Honduras, Benimaclet, Polo y Peyrolón) y los 12 de las ZAS no publican mediciones.
- **Portales**: 56.647 números de policía con coordenadas.
- **Obras en la calle**: sí, con fechas y ubicación, actualizadas a diario (653 ocupaciones activas, 385 de obras).
- **Quejas**: 176.051 quejas y sugerencias desde 2020, 10.853 de ruido, **solo por barrio** (sin coordenadas).
- **Pisos turísticos**: registro de la GVA con 5.765 viviendas en València, con dirección y referencia catastral (en el 90 %).
- **No hay** censo de locales ni de bares/discotecas, ni horarios, ni licencias de actividad por local.

## Comparación rápida con Barcelona

| Pieza | Barcelona | València | Estado |
|---|---|---|---|
| Mapa de ruido | Tramo de calle 2017, ráster 2022, fachadas | Isófonas 2012, 2017 y 2022 (polígonos por franjas de 5 dB) | Peor: sin tramo ni fachada |
| Sensores | 176, por hora 2015–2023 y por minuto | 16 en Russafa, por día, 2020–hoy | Mucho peor: sin perfil horario |
| Portales | 172.000 | 56.647 | Igual de útil |
| Locales en planta baja | 44.000 con ocio nocturno | No existe | Falta |
| Horarios de ocio | Sí | No | Falta |
| Obras en curso | Sí, diario | Sí, diario (puntos y líneas) | Igual |
| Quejas con motivo ruido | Con coordenadas | Solo barrio | Peor |
| Pisos turísticos | Con coordenadas | Dirección + ref. catastral (GVA) | Se puede |
| Patios de manzana | Sí | No directo; se puede calcular | Calcular |
| Anchura de calle | Estimada con portales | Bordillos + fachadas + alineaciones | Mejor |

---

## 1. Mapa estratégico de ruido

### Lo que ofrece el portal de datos abiertos (es el de 2012)

- Conjuntos: `mapa-soroll-dia-7h-19h`, `mapa-soroll-vesprada-19-23h`, `mapa-soroll-nit-23-7h`, `mapa-soroll-lden-24-h`.
  - Ejemplo: https://opendata.vlci.valencia.es/dataset/mapa-soroll-nit-23-7h
- Capas: `OPENDATA/Salud/MapServer/158` (día), `142` (tarde), `143` (noche), `144` (Lden).
- Formato: polígonos (isófonas). Campos: `gridcode` (1 a 6) y `gid`. Nada más: ni año, ni fuente.
- Registros (comprobado): día 53, tarde 53, noche 54, Lden 52 polígonos multiparte. Cada capa pesa unos 22 MB en GeoJSON (≈540.000 vértices).
- Descarga: GeoJSON/JSON por API (200), CSV con WKT (`https://geoportal.valencia.es/apps/OpenData/Salud/Salud__143.csv`, 200, 20 MB), SHP, KML, WMS y WFS.
- **Es el mapa de 2012**: la geometría es idéntica, vértice a vértice, a la del servicio `Laboratorio/MapaRuido2012` (mismos `gid`, mismo número de vértices y mismas coordenadas en las pruebas). Además, el número de polígonos coincide en las cuatro franjas.
- **La leyenda de la noche está mal** en el portal: pone "<55 … >75 dBA" como el día. En el servicio de 2012, la noche va de "<50" a ">70 dBA".

### Los mapas de 2017 y 2022 (no están en el catálogo, pero sí en el geoportal)

Los encontré buscando en ArcGIS Online (cuenta `appSigval` del Ayuntamiento, web "Capital Verde"):

- **2022 (fase 4)**: `https://geoportal.valencia.es/server/rest/services/Laboratorio/MapaRuido/MapServer`
- **2017 (fase 3)**: `https://geoportal.valencia.es/server/rest/services/Laboratorio/MapaRuido2022/MapServer` (sí, el nombre está cruzado)
- **2012**: `https://geoportal.valencia.es/server/rest/services/Laboratorio/MapaRuido2012/MapServer`

Cómo sé cuál es cada uno: el elemento de ArcGIS Online "SERVICIO CONTAMINACION ACUSTICA 2022" apunta a `MapaRuido`, y "…2017" apunta a `MapaRuido2022`. La "Escena Ruido 2022" usa `MapaRuido`. No lo he podido contrastar con la memoria oficial (ver bloqueos).

Cada servicio tiene 16 capas: Lden, día, tarde y noche × (total, tráfico rodado, ferrocarril, industria). **El ocio no aparece como fuente.**

- 2022: campos `from_`, `to_` (en dB). Día: 5 polígonos (55–60, 60–65, 65–70, 70–75, 75–99). Noche: 6 polígonos (50–55 … 75–99). Por debajo de 55 dB (día) o 50 dB (noche) no hay polígono. Cada polígono tiene cientos o miles de anillos (por ejemplo, la noche 50–55 tiene 4.434 anillos y 58.415 vértices).
- 2017: campos `category` (por ejemplo `Lnight5054`, `LnightLowerThan40`), `source`, `umecod` = `Ag_VAL_15`. Noche: 8 polígonos, con franjas hasta por debajo de 40 dB.
- Consulta por punto: funciona (`/query?geometry=lon,lat&inSR=4326&spatialRel=esriSpatialRelIntersects`). Prueba en el sensor T248679 (Matías Perelló / Doctor Sumsi), mapa 2022: día 65–70, tarde 65–70, noche 60–65, Lden 65–70. El sensor da una mediana de **Ln 55,2** y **Ld 61,6** (2020–2026). El mapa sobrestima unos 5 dB en este punto.
- **Licencia de los servicios "Laboratorio": no declarada** (el campo `licenseInfo` está vacío). Lo publicado en el catálogo es CC BY 4.0. Antes de usar 2017 o 2022 en producción habría que preguntar al Ayuntamiento.
- Visores: https://aytovalencia.maps.arcgis.com/apps/webappviewer/index.html?id=f76ea8deaf524ce8afd4940874e47d04 (2022) y comparadores 2017–2022 en experience.arcgis.com.
- Fachadas: **no hay** niveles por fachada publicados (sin comprobar si están en la memoria de la fase 4).

**Frente a Barcelona, falta**: un dato por tramo de calle y por fachada. Habría que asignar a cada portal la franja de la isófona en la que cae, con errores de ±2,5 dB solo por el redondeo a franjas.

### Mapas de la Generalitat (carreteras y ferrocarril autonómicos)

- 12 conjuntos en https://dadesobertes.gva.es (búsqueda "ruido"): Ld, Le, Ln, Lden de grandes ejes viarios y ferroviarios (4.ª fase), pantallas acústicas y "Instrumentos de planificación" (PAM y ZAS por municipio).
- Servicio WFS/WMS: `https://terramapas.icv.gva.es/0503_ContaminacionAcustica` (GetCapabilities 200). Capas: `MER.Viaria.Ldia/Ltarde/Lnoche/Lden`, `MER.Ferroviaria.*`, `InstrumentosMunicipales.ZAS`, `InstrumentosMunicipales.PAM`, pantallas.
- `InstrumentosMunicipales.ZAS` en CSV: 542 municipios; para València, `zas = SÍ` y `apam = SÍ`, con el **polígono del término municipal entero**, no de cada ZAS. Solo sirve como dato administrativo.
- Solo cubren las vías de la GVA (no las calles de la ciudad). Sin comprobar cuánto entra dentro del término de València.

## 2. Sensores municipales de ruido

### 16 sonómetros de Russafa (lo único útil)

- Conjuntos `t248652-daily` … `t251234-daily` (16). Ejemplo: https://opendata.vlci.valencia.es/dataset/t248679-daily
- Descarga: CSV desde Pentaho: `https://datosbi.vlci.valencia.es/pentaho/plugin/cda/api/doQuery?path=/public/vlci/datosabiertos/calidadambiental_sonometros_ruzafa_diarios.cda&dataAccessId=sqlSonometrosRuzafaDaily&paramid=T248679-daily&outputType=CSV&_TRUST_USER_=publicoda` (200, entre 214 y 374 KB por sensor). Separador `;`.
- Columnas: `recvtime; entitytype (NoiseLevelObservedAggregated); entityid; laeq; laeq_d; laeq_den; laeq_e; laeq_n; dateobserved`.
- **Un registro por día.** No hay datos por hora. La ficha dice que el sensor mide LAeq cada minuto, pero solo se publica el resumen diario.
- Registros y fechas (comprobado): 32.291 filas en total; entre 1.767 y 2.254 días por sensor. Los primeros empiezan el 2 de marzo de 2020 (4 sensores) y el resto en septiembre–noviembre de 2020. Todos llegan hasta el **5 de octubre de 2026** (ayer), salvo T248669, que se para el 5 de marzo de 2026. Se actualiza a diario (la fila de ayer se insertó hoy a las 5:32).
- La ubicación exacta viene en la descripción del conjunto (por ejemplo, T248679: 39.4614718, -0.3681443), no en el CSV.
- Medianas de Ln por sensor: 49,3 a 60,1 dB. Ld: 57,0 a 65,8 dB.
- **Perfil por día de la semana: sí se puede** (día a día). Ejemplo: Cura Femenía 14 (T251234), mediana de Ln de lunes a domingo: 50,5 / 51,0 / 51,6 / 54,4 / **62,6 / 65,6** / 52,8 (la fecha es la del inicio de la noche: viernes y sábado son las noches de fin de semana).
- **Perfil por hora: no se puede.** Solo hay tres franjas (día, tarde, noche).

### Otras estaciones

- `estacions-de-soroll-estaciones-de-ruido`: 4 estaciones fijas (Ayuntamiento, Don Juan de Austria, Avda. Aragón, Pista de Silla), en `OPENDATA/MedioAmbiente/MapServer/160`.
  - Sus datos (`https://mapas.valencia.es/WebsMunicipales/uploads/atmosferica/ruido.csv`, 200) son **una media diaria de un solo mes y de solo 2 estaciones** (Aragón y Ayuntamiento). Hoy (6 de octubre) el fichero tiene **junio de 2026** (30 filas). Está desfasado y sin histórico.
- `estacions-de-soroll-monitoritzacio-zas-…`: 12 puntos de las ZAS (Xúquer X01/X04, Juan Llorens J02/J04/J05, Carmen C01/C02, Woody W01–W04, y Buen Orden A02) en `OPENDATA/MedioAmbiente/MapServer/161`. **Solo la ubicación, sin mediciones.**
- Los 22 sonómetros de las zonas de ocio (Cánovas 3, Polo y Peyrolón 6, Cedro 5, Honduras 4, Benimaclet 4), según la prensa y smartcity.valencia.es: **no hay datos abiertos** en el catálogo. Sin comprobar si el visor municipal los muestra.
- Pentaho: no se pueden listar otras consultas (`listQueries` y `getCdaList` dan 401). No he probado nombres de consulta inventados.

**Frente a Barcelona, falta**: datos por hora o por minuto, y sensores fuera de Russafa. Sin perfil horario propio, habría que reutilizar los perfiles horarios de Barcelona y calibrarlos con las tres franjas diarias de Russafa. Merece la pena pedir por transparencia los datos por minuto u hora (los sensores ya los miden).

## 3. Portales (números de policía)

- `portals-dels-carrers-portales-de-las-calles`, capa `OPENDATA/UrbanismoEInfraestructuras/MapServer/217`.
- **56.647 puntos**. Campos: `codvia, numportal, dupli_trip, accesorio, angulo, catfis, descripcion`. El nombre de la calle no viene: hay que cruzar `codvia` con `llistat-dels-carrers` (CSV) o con los ejes de calle.
- SHP en ZIP: `https://geoportal.valencia.es/apps/OpenData/UrbanismoEInfraestructuras/UrbanismoEInfraestructuras__217.zip` (200, 2,1 MB). Proyección EPSG:25830; la API devuelve WGS84 con `outSR=4326`.
- Extra útil: `Parcelas catastrales urbana` (capa 216), **38.356 parcelas** con `refcat`, `codvia`, `npol`, año de construcción y **población por parcela** (total y por edades).

## 4. Locales, bares, discotecas, terrazas y horarios

- **No hay censo de locales ni de actividades** en el portal municipal. Búsquedas de "licencias", "actividades", "bares" y "ocio": nada a nivel de local.
- `recibos-mesas-y-sillas-2020-2025`: 383 filas, **número de recibos de terraza por barrio y año** (sin dirección).
- `recibos_iae_2020-2025`: 453 filas, recibos del IAE por barrio y tipo (empresarial, profesional…), sin epígrafe de hostelería.
- `Ordenanzas Mesas y Sillas` (`SociedadBienestar/MapServer/6`): 57 polígonos con campo `zona`. Sin comprobar qué horario corresponde a cada zona (hay que leer la ordenanza).
- `Ordenanza Espacios Públicos` (`SociedadBienestar/MapServer/7`): 68 polígonos con `zona`.
- **Alternativa: OpenStreetMap** (Overpass, comprobado hoy): 2.203 locales en el término de València: 1.268 restaurantes, 425 cafés, 262 bares, 208 pubs y **40 discotecas**. Solo 75 bares, pubs o discotecas tienen `opening_hours`. Licencia ODbL (no CC BY: obliga a compartir igual la base derivada).
- Catastro (uso "ocio y hostelería" por inmueble): **bloqueado** desde aquí (ver bloqueos).

**Frente a Barcelona, falta**: todo el censo de locales con indicador de ocio nocturno y los horarios. Habría que pedirlo por transparencia (licencias de actividad de hostelería y de espectáculos, con dirección) o tirar de OSM.

## 5. Obras en la vía pública

- `ocupacio-via-publica-ocupacion-via-publica` → `OPENDATA/Trafico/MapServer/209` (puntos). **653 registros**, todos activos hoy. Tipos: OBRAS 385, INCIDENCIAS 267, FESTEJOS 1.
  - Campos: `id_incidencia, desc_incidencia` (empresa o servicio, por ejemplo "UTE CANAL DE ACCESO"), `tipo_incidencia, desc_calle, tipo_afectacion` (acera, calzada, estacionamiento…), `fecha_inicio, fecha_fin, numero_policia_origen`.
  - Fechas de inicio: del 2 de enero de 2025 al 6 de octubre de 2026 (hoy). Se actualiza a diario. Parece que solo publica las vigentes.
  - Incluye obras privadas y municipales (por el nombre de la empresa), pero no lo distingue en un campo.
- `OPENDATA/Trafico/MapServer/235` "Obras": **266 líneas** con `fecha_inicio_periodo, fecha_fin_periodo, estado (Valido_p), ocupacion`. Todas activas hoy. CSV: `https://geoportal.valencia.es/apps/OpenData/Trafico/Trafico__235.csv` (200).
- Capas hermanas: `234 Mudanzas` (0 ahora), `233 Festejos` (1).
- `obres-executades` (obras terminadas): el GeoJSON da **404** y el CSV enlazado es en realidad el de obras en curso (capa 235). Roto.

**Frente a Barcelona**: equivalente. Hay punto y tramo en vez de polígono, y la fecha de fin viene. Sirve para la regla de "+2 dB a menos de 25 m".

## 6. Quejas ciudadanas

- `total-castellano` ("Queixes i Suggeriments"): https://opendata.vlci.valencia.es/dataset/total-castellano. CSV de 21 MB (200), con datastore.
- **176.051 filas**, del 1 de enero de 2020 al **31 de mayo de 2026**.
- Columnas: `tipo_solicitud; canal_entrada; fecha_entrada_ayuntamiento; tema; subtema; distrito_solicitante; barrio_solicitante; distrito_localización; barrio_localización`.
- Tema "Contaminación acústica": **10.853 quejas**, 10.154 con barrio. Subtemas: actividades (molestias y denuncias) 3.960, tráfico rodado 2.511, botellón 1.062, **servicios de limpieza 809**, vecinos 726, mesas y sillas 301, eventos públicos 297, casales falleros 292, obras municipales 266, aviones 241, obras privadas 209, aire acondicionado 179.
- **Sin coordenadas ni calle.** Solo código de barrio (por ejemplo "123"). Barrio con más quejas: el 123, con 1.567 (sin comprobar el nombre; probablemente Russafa o similar en el distrito 12).
- App "València al dia": sin comprobar. No hay conjunto abierto de sus avisos.

**Frente a Barcelona, falta**: la ubicación exacta. Por barrio solo sirve como aviso de zona. Las quejas por la limpieza (809) son el equivalente a la pista de "recogida de basuras".

## 7. Viviendas turísticas

- GVA, Registro de Turismo: `tur-gestur-vt`, https://dadesobertes.gva.es/dataset/tur-gestur-vt. CSV, JSON y XML, con datastore. **Actualización diaria** (último cambio: hoy, 08:41).
- 90.098 viviendas en la Comunitat. Con el filtro `municipio = "VALÈNCIA"` (exactamente así): **5.765 viviendas**. Altas del 13 de marzo de 2001 al 23 de septiembre de 2026.
- Campos: `cod_municipio, cp, direccion` (por ejemplo "C LIRIO, 32 Bl:A Pl:B Pt:4"), `dormit_totales, fecha_alta, plazas_totales, ref_catastral, signatura, superficie…`. **Sin coordenadas.**
- `ref_catastral` presente en 5.172 (de 20 caracteres). Los 14 primeros caracteres son la parcela: se cruzan con la capa 216 (`refcat`) y dan la ubicación sin geocodificar.
- Ayuntamiento: `Ámbitos Excluidos VUT` (`Turismo/MapServer/219`), 10 polígonos (zonas donde no se permiten, por ejemplo El Perellonet o Carpesa). Sin interés para el ruido.

**Frente a Barcelona**: equivalente, con un cruce más (referencia catastral → parcela).

## 8. Patios de manzana / fachadas interiores

- No hay una capa de patios.
- Se puede calcular:
  - `Manzanas` (`UrbanismoEInfraestructuras/MapServer/262`): 4.929 polígonos.
  - `Ocupación del suelo` (`…/324`): 5.378 polígonos, de los que 4.549 son "AGRUPACION DE EDIFICIOS".
  - `Cartografía Base Edificios` (`…/112`): 553.586 líneas de fachada (EDIFICIO 58.224, MEDIANERA 106.280, CAMBIO DE ALTURA 268.828, VOLADIZOS 120.254), escala 1:500, vuelo de 2018.
  - Patio ≈ manzana menos edificación. Fachada interior = línea de EDIFICIO que no da a la calle (sin comprobar la calidad del resultado).

## 9. Anchura de calle

- Mejor que en Barcelona, porque hay geometría real:
  - `Cartografía Base Bordillos` (`…/307`): 50.630 líneas (ACERA BORDILLO 50.550), 1:500, 2018.
  - Fachadas de edificios (`…/112`, arriba).
  - `PGOU – Alineaciones` (`…/212`): 21.998 polígonos con `altura` (número de plantas permitido). También sirve para "calle en cañón" (relación altura/anchura).
  - `Ejes de calle` (`…/223` o `…/328`): 12.892 tramos con `codvia`, nombre, numeración de portales izquierda y derecha, y `longitud`.
- Anchura = distancia entre las fachadas de ambos lados, medida perpendicular al eje (sin calcular todavía).
- `Velocidad Calles` (`Trafico/MapServer/223`): 12.880 tramos con límite (peatonal, 20, 30, 50).

## 10. Extras

### ZAS (zonas acústicamente saturadas)

- `zones-zas-zonas-zas` → `OPENDATA/SociedadBienestar/MapServer/5`: **5 polígonos**: CARMEN, XUQUER (2), WOODY (Menéndez Pelayo), JUAN LLORENS. También en `Laboratorio/ContaminacionAtmosfericaAcustica/MapServer/3`, con área (Carmen: 361.373 m²).
- **Russafa, Benimaclet, Cánovas y Cedro no aparecen** como polígono ZAS en el geoportal. Sin comprobar si están declaradas o en trámite.

### Contenedores y recogida

- `contenidors-residus-solids-…` (`MedioAmbiente/MapServer/0`): **23.057 contenedores** con tipo (papel, envases, resto…), modelo, tipo de carga (por ejemplo "Lateral Derecha"), empresa, calle y número. La última actualización pone "2026-JUNIO".
- **No hay horarios de recogida.** Habría que pedirlos por transparencia, igual que en Barcelona.

### Tráfico

- `Intensidad de los Puntos de Medida` (`Trafico/MapServer/208`): **1.210 puntos** con `ih` (vehículos por hora). Se actualiza cada hora; la última lectura es de hoy. **Solo el último valor, sin histórico abierto.** El catálogo avisa: "temporalmente con errores de procesamiento".
- `Intensidad tráfico tramos` (`…/188`): 394 tramos con `lectura` (última) e `imv` (intensidad media).
- `Estado tráfico tiempo real` (`…/192`): 462 tramos, cada 3 minutos.
- Para un perfil horario de tráfico habría que guardar las lecturas uno mismo cada hora (como con las obras en Barcelona) o pedir el histórico.

### Planes de acción

- Plan de acción contra el ruido 2023–2027 (4.ª fase): enlazado en https://www.valencia.es/cas/calidadaire/mapa-del-ruido (PDF, sin comprobar el contenido).

---

## Bloqueos y cosas que no pude comprobar

- **Ninguna descarga pidió captcha**, hCaptcha ni reto de Cloudflare.
- **valencia.es** rechaza `curl` con "Request Rejected" (cortafuegos web, código 503). Con un lector web normal sí se ve. No es un captcha, pero los PDF de esa web habría que bajarlos a mano:
  - Página: https://www.valencia.es/cas/calidadaire/mapa-del-ruido
  - Ficheros: "Plan de acción en materia de contaminación acústica de València (4.ª fase 2023-2027)" y "Presentación del Mapa 2017".
- **SICA (Ministerio, sicaweb.cedex.es)**: con `curl` falla el certificado SSL, y con el lector web da 503. La memoria del mapa 2022 debería descargarse a mano desde https://sicaweb.cedex.es/docs/mapas/fase4/aglomeracion/Aglomeraci%C3%B3n%20de%20Valencia/Ag_VAL_Valencia_15_Memoria.pdf. Sirve para confirmar el año de cada servicio y si hay niveles en fachada.
- **Catastro**: "Hemos denegado el acceso desde su dirección IP" (403) en el ATOM INSPIRE. El usuario tendría que bajarlo desde su casa: edificios INSPIRE de València (municipio 46900) desde https://www.catastro.hacienda.gob.es/INSPIRE/buildings/46/ES.SDGC.bu.atom_46.xml, y, si interesa el uso hostelero por inmueble, los datos alfanuméricos de la Sede Electrónica (requiere identificarse).
- **Pentaho (datosbi.vlci.valencia.es)**: no deja listar consultas (401). No sé si hay consultas por hora o por minuto de los sensores.
- **valencia.opendatasoft.com ya no existe** (404, "This domain could not be found").
- Sin comprobar:
  - si los servicios "Laboratorio" (mapas 2017 y 2022) tienen licencia abierta;
  - qué barrio es el código 123;
  - si existen datos de los 22 sonómetros de ocio;
  - los horarios de terrazas por zona de ordenanza;
  - los datos de la app València al dia;
  - la calidad del cálculo de patios y anchuras.

## Qué pedir por transparencia (València)

1. Datos por hora (o por minuto) de los 16 sonómetros de Russafa, de los 22 de las zonas de ocio y de los 12 de las ZAS, desde el inicio.
2. Censo de actividades con licencia (hostelería, ocio, espectáculos) con dirección, tipo y horario autorizado.
3. Quejas de ruido con dirección o coordenadas (aunque sea redondeada a 50 m).
4. Horarios de recogida de residuos y de limpieza por calle.
5. Confirmación de la licencia de los mapas de ruido 2017 y 2022 del geoportal, y si hay niveles en fachada (fase 4).
