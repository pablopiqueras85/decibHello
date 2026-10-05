# DecibHello — Pendientes y lo que falta

Estado a octubre de 2026. Visor: piloto/visor.html (publicado como artifact privado).

## Pendientes tuyos

- [ ] **Datos de los sensores**: descargar `2023_1S_XarxaSoroll_EqMonitor_Dades_1Hora.zip` y `2023_2S_XarxaSoroll_EqMonitor_Dades_1Hora.zip` de [Open Data BCN](https://opendata-ajuntament.barcelona.cat/data/es/dataset/xarxasoroll-equipsmonitor-dades) y pasármelos (adjuntos o en `piloto/sensores/`).
- [ ] **Nota a ciegas** (0–100, de día y de noche) de las calles de control: Tuset 20, Travessera de Gràcia 81, 150 y 300, Martínez de la Rosa 20.
- [ ] **Tramo silencioso de Travessera de Gràcia**: número o cruce.
- [ ] **Anchura de Travessera de Gràcia 150**: confirmar si ≈ 8 m es razonable.
- [ ] **Solicitud de información pública** al Ajuntament (contenedores, rutas y horarios de recogida, calendario de muebles, limpieza nocturna). Borrador en `decibhello-fuentes-datos-barcelona.md`, apartado 2.13.
- [ ] **Decidir cómo tratar los anuncios** (Idealista, Fotocasa…): pedir la calle (ahora), extensión de navegador o acuerdos con portales.
- [ ] **Decisiones abiertas**: idiomas (castellano, catalán, inglés), nombre y dominio.

## Lo que falta para que sea funcional y tenga valor

### 1. Que la nota sea fiable (lo más importante)
- [ ] **Calibrar con mediciones reales**: perfiles por hora y día de la semana con los sensores (sustituye los supuestos v0).
- [ ] **Validación sobre el terreno**: medir con sonómetro o móvil en 20–30 portales, de día y de noche, entre semana y en fin de semana, y comparar con la nota. Sin esto no podemos decir cuánto acierta.
- [ ] **Mapa de ruido 2022**: pasar del de 2017 (por tramo) al ráster de 2022, para recoger cambios como los ejes verdes (Consell de Cent).
- [ ] **Explicar la incertidumbre**: mostrar un margen ("entre 70 y 80") además de la cifra.

### 2. Lo que más le importa a quien alquila o compra
- [ ] **Planta del piso**: un primero y un ático en la misma fachada no suenan igual. Pedir la planta y corregir.
- [ ] **Orientación del piso**: exterior, interior o esquina (que da a dos calles).
- [ ] **Ruido del propio edificio**: bar o local en los bajos, ascensor, aire acondicionado de vecinos. Hoy no lo cubrimos y es de lo que más molesta.
- [ ] **Estacionalidad**: verano (ventanas abiertas, terrazas) frente a invierno.
- [ ] **Avisos temporales**: obras en curso o previstas, fiestas mayores, conciertos (los datos de obras ya están en Open Data BCN).
- [ ] **Comparar**: dos o tres pisos lado a lado, y la calle frente a la media del barrio y de la ciudad.

### 3. Producto usable por cualquiera
- [ ] **Portal independiente propio**: DecibHello como web con marca, dominio y alojamiento propios, que funcione por sí sola (buscador, informe, mapa) sin depender de los portales inmobiliarios. La extensión de Chrome y los acuerdos con portales son vías de entrada a este portal, no lo sustituyen. Hoy es un prototipo privado: falta dominio, alojamiento, que cargue rápido en el móvil y que los datos se actualicen solos.
- [ ] **Mapa** con la calle y los focos (bares, sensores, quejas) alrededor.
- [ ] **Informe para guardar o enviar** (PDF o enlace) por dirección.
- [ ] **Extensión de Chrome**: al abrir un anuncio (Idealista, Fotocasa, Habitaclia…), lee la zona o calle que la página ya muestra al usuario y enseña la nota de DecibHello en el propio anuncio, con enlace al informe completo. Revisar antes las condiciones de uso de cada portal y las normas de la Chrome Web Store (permisos mínimos, privacidad).
- [ ] **Acuerdos con portales inmobiliarios** para mostrar la nota en sus anuncios.
- [ ] **Textos claros y aviso legal**: dejar claro que es una estimación, no una medición del piso.

### 4. Datos de la comunidad
- [ ] **Opiniones de vecinos** por calle: "aquí pasa el camión a las 2:00", "bar con música hasta tarde".
- [ ] **Mediciones con el móvil**, con control de calidad.
- [ ] **Moderación y privacidad** de lo que aporta la gente.

### 5. Negocio
- [ ] **Validar que la gente lo quiere**: 10–15 entrevistas y una página con lista de espera.
- [ ] **Modelo de ingresos**: informe gratuito básico y completo de pago; licencia para inmobiliarias y portales.
- [ ] **Mantenimiento de datos**: actualizar quejas, locales, pisos turísticos y sensores cada mes o trimestre de forma automática.
- [ ] **Siguiente ciudad**: área metropolitana de Barcelona; después Madrid o Valencia.

### 6. Venta a portales y empresas (cuando haya portal público y validación)
- [ ] **Estrategia extensión vs. portales**: la extensión sirve para medir interés, no para presionar. En la web de un portal que integre la nota, la extensión deja de mostrarse. El portal propio sigue siendo el centro.
- [ ] **Material**: demo pública, resultados de la validación, cifras de uso y una hoja de presentación (qué es, datos, integración por recuadro o conexión directa, propuesta de piloto).
- [ ] **Orden de contacto**: primero Fotocasa y Habitaclia (mismo grupo, competidores de Idealista, Habitaclia fuerte en Cataluña); en paralelo agencias, gestoras de alquiler, tasadoras y aseguradoras; Idealista cuando haya un piloto que enseñar.
- [ ] **Canales**: LinkedIn (producto, alianzas, desarrollo de negocio, innovación), contactos que te presenten, eventos (SIMA, Barcelona Meeting Point, PropTech Spain), programas para startups de los propios grupos.
- [ ] **Oferta**: piloto gratuito de 3 meses en los anuncios de Barcelona, midiendo visitas al recuadro, tiempo en el anuncio y peticiones de visita; después licencia mensual o por volumen. Sin exclusividad al principio salvo que se pague.
- [ ] **Mensaje inicial**: borrador en la conversación; adaptarlo a cada portal cuando toque.

## Orden recomendado

1. Sensores + validación sobre el terreno (sin fiabilidad, no hay producto).
2. Planta, orientación y avisos temporales en el visor.
3. Entrevistas y lista de espera en paralelo.
4. Portal independiente propio con buscador, mapa e informe.
5. Opiniones de vecinos.
6. Extensión de Chrome y acuerdos con portales.
