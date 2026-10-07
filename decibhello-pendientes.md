# DecibHello — Pendientes y lo que falta

Estado a octubre de 2026. Visor: piloto/visor.html (publicado como artifact privado).

## Pendientes tuyos

- [x] **Datos de los sensores por hora (2023)**: recibidos y analizados (octubre de 2026).
- [ ] **Datos de los sensores minuto a minuto** (desde 2024, 250–350 MB por mes) para medir los picos cortos (camiones de basura, gritos). Hay que buscar cómo pasarlos: recortarlos antes o enlazarlos desde una nube.
- [ ] **Nota a ciegas** (0–100, de día y de noche) de las calles de control: Tuset 20, Travessera de Gràcia 81, 150 y 300, Martínez de la Rosa 20.
- [ ] **Tramo silencioso de Travessera de Gràcia**: número o cruce.
- [ ] **Anchura de Travessera de Gràcia 150**: confirmar si ≈ 8 m es razonable.
- [ ] **Solicitud de información pública** al Ajuntament (contenedores, rutas y horarios de recogida, calendario de muebles, limpieza nocturna). Borrador en `decibhello-fuentes-datos-barcelona.md`, apartado 2.13.
- [ ] **Solicitudes de transparencia al Ayuntamiento de Madrid** (dos: datos por hora de las 31 estaciones de ruido, y horarios de recogida y limpieza). Borrador del agente 5 en `investigacion/solicitud-transparencia-madrid.md` (rama `agente/siguiente-ciudad`).
- [ ] **Solicitud de información pública sobre obras privadas** (licencias de obras mayores y permisos de andamios, grúas y contenedores desde 2024). Borrador en el apartado 2.15.
- [ ] **Decidir cómo tratar los anuncios** (Idealista, Fotocasa…): pedir la calle (ahora), extensión de navegador o acuerdos con portales.
- [ ] **Decisiones abiertas**: idiomas (castellano, catalán, inglés), nombre y dominio.

## Lo que falta para que sea funcional y tenga valor

### 1. Que la nota sea fiable (lo más importante)
- [x] **Calibrar con mediciones reales**: perfiles por hora y día de la semana medidos con los sensores, y nivel medido en 352 tramos con sensor.
- [x] **Ocio infravalorado de día y de tarde**: los bares y discotecas suman dB en proporción a cuántos hay a menos de 100 m (también de noche), validado con sensores por distritos (`piloto/ocio_oculto.md`). Los pisos turísticos cuentan en el aviso de picos nocturnos.
- [x] **Reparto semanal del ocio nocturno**: horarios de discotecas y bares musicales cercanos (Open Data BCN) y sensores de la misma calle. Tuset ya usa su sensor.
- [ ] **Medir los picos, no solo la media**: un domingo a las 15:00 se percibe tranquilo y la hora punta muy ruidosa, pero los sensores solo marcan 2–4 dB de diferencia en la media horaria. Lo que cambia son los picos (motos, bocinas, camiones, autobuses). Con los datos minuto a minuto se puede calcular un indicador de picos (por ejemplo, el nivel superado el 10 % del tiempo) y sumarlo a la nota.
- [x] **Escala repartida**: 0 = calle muy tranquila, 100 = Tuset un viernes de madrugada (Tuset ya da 100), y posición en la ciudad ("más ruidosa que el X %"). Antes el 84 % de los portales salía ruidoso.
- [ ] **Afinar la escala** con tus notas a ciegas de las calles de control, y separar las grandes avenidas, que quedan todas cerca de 100 (quizá subir el tope de día).
- [ ] **Limitadores de sonido de los locales**: las discotecas y bares musicales deben tener un limitador-registrador que envía datos al Ajuntament, pero no son públicos. Pedirlos por transparencia (miden dentro del local, no el ruido de la gente en la calle).
- [ ] **Ocio infravalorado de noche**: ninguna pista pública lo predice (probado con bares, terrazas, quejas por motivo, pisos turísticos, plazas). Solo se resuelve midiendo: mediciones con el móvil, opiniones de vecinos, más sensores.
- [ ] **Validación sobre el terreno**: medir con sonómetro o móvil en 20–30 portales, de día y de noche, entre semana y en fin de semana, y comparar con la nota. Sin esto no podemos decir cuánto acierta.
- [ ] **Mapa de ruido 2022**: pasar del de 2017 (por tramo) al ráster de 2022, para recoger cambios como los ejes verdes (Consell de Cent).
- [x] **Margen de error** (7 oct): el visor dice "entre X y Y". Sin sensor: ±4,9 dB de día, ±6,1 de tarde y ±4,6 de noche (el error que no se supera en 2 de cada 3 sensores, validado por distritos; ≈ ±15 puntos en la nota del día). Con sensor en la calle: ±2–3 dB (≈ ±7 puntos).

### 2. Lo que más le importa a quien alquila o compra
- [x] **Planta del piso** (estimación, 7 oct): selector en el visor, de bajo a ático. Usa las plantas del edificio (Catastro) y la anchura de la calle: en calles estrechas y altas casi no cambia; en calles anchas baja con la altura (Diagonal 500, 6.º: −3,9 dB); ático −3 dB; bajo +1 dB.
- [ ] **Medir la planta**: con el sonómetro, medir a la vez en varias plantas del mismo edificio, en una calle estrecha y en una ancha, y ajustar las cifras.
- [x] **Orientación del piso** (7 oct): exterior, interior (patio) y esquina. La esquina se marca a mano ("también da a Carrer X") y cada hora cuenta la fachada más ruidosa.
- [ ] **Ruido del propio edificio**: bar o local en los bajos, ascensor, aire acondicionado de vecinos. Hoy no lo cubrimos y es de lo que más molesta.
- [ ] **Estacionalidad**: verano (ventanas abiertas, terrazas) frente a invierno.
- [x] **Obras públicas**: las obras en curso a menos de 25 m suman +2 dB de día laborable mientras duran (validado con sensores); el visor lista las obras a menos de 100 m con sus fechas (`piloto/obras_validacion.md`).
- [ ] **Obras privadas** (rehabilitación de edificios, derribos, obra nueva): no hay datos públicos de licencias. Las grandes con andamio o grúa en la calle ya están en las obras públicas. Pedir licencias y permisos de andamios y grúas por transparencia (borrador en `decibhello-fuentes-datos-barcelona.md`, apartado 2.15).
- [x] **Obras al día**: una tarea programada regenera y republica el visor de lunes a viernes (6:47) con las obras del día.
- [ ] **Otros avisos temporales**: fiestas mayores, conciertos.
- [x] **Comparar** (7 oct): hasta 3 pisos lado a lado (con su planta, lado y esquina), y la calle frente a la media de su barrio y de Barcelona.

### 3. Producto usable por cualquiera
- [ ] **Portal independiente propio**: DecibHello como web con marca, dominio y alojamiento propios, que funcione por sí sola (buscador, informe, mapa) sin depender de los portales inmobiliarios. La extensión de Chrome y los acuerdos con portales son vías de entrada a este portal, no lo sustituyen. Hoy es un prototipo privado: falta dominio, alojamiento, que cargue rápido en el móvil y que los datos se actualicen solos.
- [x] **Mapa de la zona** (7 oct): 200 m alrededor, con la nota de cada tramo, bares, bares musicales y discotecas, quejas por ruido, sensores y obras. Dibujado por nosotros (sin mapa base de calles).
- [x] **Informe para guardar o enviar** (7 oct): botón "Descargar informe" (un fichero que se abre en cualquier navegador) e "Imprimir o guardar en PDF".
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
- [x] **Siguiente ciudad: Madrid** (confirmado el 6 de octubre de 2026). Datos de 0 a 10: Barcelona 9,5 · Madrid 8 · Valencia 5 · L'Hospitalet + Badalona 3,5 · Sant Cugat 1. Informes en `investigacion/` (rama `agente/siguiente-ciudad`). El área metropolitana, como ampliación de Barcelona más adelante.
- [ ] **Piloto de Madrid** (en espera: Pablo prefiere terminar antes Barcelona, 6 oct): unas 3–4 semanas. Mapa 2021 en dB exactos cada 5 m, censo de locales con horarios, portales con coordenadas. Falta: sensores por hora (transparencia), ocio en el mapa (recalibrar con pocas estaciones) y situar en el mapa las quejas y los pisos turísticos.

### 6. Venta a portales y empresas (cuando haya portal público y validación)
- [ ] **Estrategia extensión vs. portales**: la extensión sirve para medir interés, no para presionar. En la web de un portal que integre la nota, la extensión deja de mostrarse. El portal propio sigue siendo el centro.
- [ ] **Material**: demo pública, resultados de la validación, cifras de uso y una hoja de presentación (qué es, datos, integración por recuadro o conexión directa, propuesta de piloto).
- [ ] **Orden de contacto**: primero Fotocasa y Habitaclia (mismo grupo, competidores de Idealista, Habitaclia fuerte en Cataluña); en paralelo agencias, gestoras de alquiler, tasadoras y aseguradoras; Idealista cuando haya un piloto que enseñar.
- [ ] **Canales**: LinkedIn (producto, alianzas, desarrollo de negocio, innovación), contactos que te presenten, eventos (SIMA, Barcelona Meeting Point, PropTech Spain), programas para startups de los propios grupos.
- [ ] **Oferta**: piloto gratuito de 3 meses en los anuncios de Barcelona, midiendo visitas al recuadro, tiempo en el anuncio y peticiones de visita; después licencia mensual o por volumen. Sin exclusividad al principio salvo que se pague.
- [ ] **Mensaje inicial** (adaptarlo a cada portal cuando toque):

  > Hola, [nombre]. Soy [tu nombre], fundador de DecibHello: una nota de ruido de 0 a 100 para cada portal de Barcelona, que cambia según la hora y el día de la semana y explica de dónde viene el ruido (tráfico, ocio nocturno, camiones de recogida, piso exterior o interior). Es lo que los compradores e inquilinos no pueden ver en las fotos y descubren después de mudarse.
  >
  > Me gustaría proponeros un piloto de 3 meses en vuestros anuncios de Barcelona, sin coste, para medir el efecto en el interés por los anuncios. ¿Tienes 20 minutos para enseñártelo? Demo: [enlace]

## Orden recomendado

1. Sensores + validación sobre el terreno (sin fiabilidad, no hay producto).
2. Planta, orientación y avisos temporales en el visor.
3. Entrevistas y lista de espera en paralelo.
4. Portal independiente propio con buscador, mapa e informe.
5. Opiniones de vecinos.
6. Extensión de Chrome y acuerdos con portales.
