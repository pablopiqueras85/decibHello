# Madrid: datos por hora de la red de estaciones de ruido

## Dónde se envía

Formulario "Solicitud de acceso a la información pública" de la sede electrónica del Ayuntamiento de Madrid:

https://sede.madrid.es/portal/site/tramites/menuitem.62876cb64654a55e2dbd7003a8a409a0/?vgnextoid=48422ee1f6851510VgnVCM2000000c205a0aRCRD&vgnextchannel=d6e537c190180210VgnVCM100000c90da8c0RCRD&vgnextfmt=default

Portal de transparencia (información general): https://transparencia.madrid.es

Enlaces vistos en resultados de búsqueda; no se abrió el formulario (sin comprobar).

## Qué necesitas

- Un sistema de identificación electrónica admitido por la sede de Madrid (certificado digital, Cl@ve...) (sin comprobar la lista).
- **Identifícate con todos tus datos**, no solo con el correo. Según el Ayuntamiento, con solo el correo la solicitud se tramita de forma más limitada. Con datos completos se tramita por la Ley 10/2019 de Madrid.
- Tus datos: `[NOMBRE Y APELLIDOS]`, `[DNI]`, `[CORREO]`.
- **Una solicitud por materia.** Esta es la 4. La de recogida y limpieza (5) va aparte.
- El formulario admite hasta 10 ficheros adjuntos (12 MB en total). No hace falta adjuntar nada.

## Asunto

Solicitud de acceso a información pública: niveles de ruido por hora de la red fija de estaciones de medida

## Texto para copiar

```
Nombre y apellidos: [NOMBRE Y APELLIDOS]
DNI: [DNI]
Correo electrónico: [CORREO]

Al amparo de la Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno, y de la Ordenanza de Transparencia de la Ciudad de Madrid, solicito la siguiente información, referida al Sistema de Vigilancia de la Contaminación Acústica (red fija de estaciones de medida de ruido), en formato reutilizable (CSV o similar):

1. El nivel sonoro continuo equivalente (LAeq) de cada hora, en dB(A), de cada una de las estaciones de la red fija, desde el 1 de enero de 2023 hasta la fecha de la respuesta. Si se dispone de ellos, también los percentiles horarios (L10, L50 y L90).

2. Si existen, los mismos datos con resolución de un minuto, para el mismo periodo.

3. Una breve descripción de los campos y de la convención de fecha y hora; en concreto, a qué fecha se asigna el periodo de noche (de 23:00 a 7:00) en los datos diarios publicados en datos.madrid.es (conjunto "Contaminación acústica. Datos diarios", fichero Ruido_diario_acumulado.csv).

Estos datos ya se publican en el portal de datos abiertos agregados por día y por periodo (día, tarde y noche). Solicito la versión horaria, que según la información municipal registra la red desde su renovación.

La finalidad es elaborar un servicio informativo sobre el ruido urbano para la ciudadanía. Solicito además, si es posible, que esta información se publique de forma periódica en el portal de datos abiertos del Ayuntamiento.

Pido recibir la respuesta por vía electrónica.
```

## Formato que pedimos

CSV (una fila por estación y hora: estación, fecha, hora, LAeq, L10, L50, L90). Más un documento corto con el significado de los campos y la lista de estaciones con sus coordenadas.

## Plazo

- **Ley 19/2013** (la que pide el encargo): un mes desde que la solicitud entra en el órgano que tiene la información, ampliable otro mes si es voluminosa o compleja (artículo 20; de memoria, sin comprobar en el texto oficial).
- **Ojo**: la web del Ayuntamiento de Madrid cita la **Ley 10/2019** de Transparencia de la Comunidad de Madrid y dice **20 días hábiles**, ampliables (según el resumen de una búsqueda; sin comprobar en la página original). Cuenta con el más corto, pero espera hasta el más largo antes de reclamar.
- Si piden aclarar la solicitud, tienen que dar 10 días y el plazo se para (sin comprobar).
- Si no contestan en plazo, se entiende denegada (silencio negativo).

## Si no contestan

Reclamación ante el **Consejo de Transparencia y Protección de Datos de la Comunidad de Madrid** (no ante el Consejo de Transparencia y Buen Gobierno estatal, como decía el borrador antiguo). Según los resultados de búsqueda y el propio Ayuntamiento, es la vía para sus denegaciones. No se ha leído la norma de competencia (sin comprobar).

- Plazo: **un mes** desde la notificación de la denegación. Si hay silencio, desde que vence el plazo para resolver.
- Es voluntaria y gratuita. Es alternativa al recurso contencioso-administrativo (2 meses): no se pueden usar las dos.
- Formulario en línea: https://sede.comunidad.madrid/denuncias-reclamaciones-recursos/consejo-transparencia-proteccion-datos
- Correo: consejotransparenciaypd@madrid.org
- Hay resoluciones que inadmiten por pasarse el plazo. Contar bien los días.

## Notas

- Viene de `investigacion/solicitud-transparencia-madrid.md`, solicitud 1.
- Si responden con un enlace a datos.madrid.es, comprobar que sea por hora y no solo el diario que ya existe.
