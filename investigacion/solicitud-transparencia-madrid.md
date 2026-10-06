# Solicitud de acceso a la información pública — Ayuntamiento de Madrid

Borrador para DecibHello, 6 de octubre de 2026. Lo envía Pablo.

## Cómo enviarla

- **Dónde**: sede electrónica del Ayuntamiento de Madrid ([sede.madrid.es](https://sede.madrid.es)), trámite "Acceso a la información pública". Pide identificarse con certificado digital, Cl@ve o DNI electrónico.
- **Norma**: Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno (estatal), y la Ordenanza de Transparencia de la Ciudad de Madrid.
- **Plazo de respuesta**: un mes, ampliable a otro mes más si la información es voluminosa o compleja (artículo 20 de la Ley 19/2013).
- **Si no responden o lo deniegan**: reclamación ante el Consejo de Transparencia y Buen Gobierno. El plazo para reclamar es de un mes.
- **Consejo**: mejor enviar **dos solicitudes separadas**, una por cada punto. Así, si una tarda o se deniega, la otra sigue adelante. Cada punto va a un área distinta (Medio Ambiente y Limpieza).

## Solicitud 1: datos por hora de la red de ruido

> Al amparo de la Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno, y de la Ordenanza de Transparencia de la Ciudad de Madrid, solicito la siguiente información, referida al Sistema de Vigilancia de la Contaminación Acústica (red fija de estaciones de medida de ruido), en formato reutilizable (CSV o similar):
>
> 1. El nivel sonoro continuo equivalente (LAeq) **de cada hora**, en dB(A), de cada una de las estaciones de la red fija, desde el 1 de enero de 2023 hasta la fecha de la respuesta. Si se dispone de ellos, también los percentiles horarios (L10, L50 y L90).
> 2. Si existen, los mismos datos con resolución de un minuto, para el mismo periodo.
> 3. Una breve descripción de los campos y de la convención de fecha y hora, en concreto a qué fecha se asigna el periodo de noche (de 23:00 a 7:00) en los datos diarios publicados en datos.madrid.es (conjunto "Contaminación acústica. Datos diarios", fichero Ruido_diario_acumulado.csv).
>
> Estos datos ya se publican en el portal de datos abiertos agregados por día y por periodo (día, tarde y noche). Solicito la versión horaria, que según la información municipal registra la red desde su renovación.
>
> La finalidad es elaborar un servicio informativo sobre el ruido urbano para la ciudadanía. Solicito además, si es posible, que esta información se publique de forma periódica en el portal de datos abiertos del Ayuntamiento.

## Solicitud 2: horarios de recogida de residuos y limpieza

> Al amparo de la Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno, y de la Ordenanza de Transparencia de la Ciudad de Madrid, solicito la siguiente información, referida a los servicios municipales de recogida de residuos y de limpieza viaria, en formato reutilizable (CSV, JSON o SHP):
>
> 1. Rutas o sectores de recogida de residuos y, para cada calle o tramo, la franja horaria y los días de la semana en que se realiza la recogida de cada fracción (resto, orgánica, envases, papel y cartón, vidrio).
> 2. Franjas horarias de los servicios nocturnos de limpieza viaria (barrido mecánico, baldeo y soplado) por calle o sector.
> 3. Si existe, el calendario de recogida de muebles y enseres por zona.
>
> La finalidad es elaborar un servicio informativo sobre el ruido urbano para la ciudadanía. Solicito además, si es posible, que esta información se publique en el portal de datos abiertos del Ayuntamiento.

## Por qué se piden

- **Datos por hora**: Madrid solo publica un dato por día y por franja. Con los datos horarios, la forma de cada hora saldría de mediciones de Madrid, igual que en Barcelona, y no de los perfiles de Barcelona. Mientras no lleguen, el piloto puede funcionar con los perfiles de Barcelona.
- **Convención de la noche**: hace falta saberla para calcular bien los pesos por día de la semana. Si no la aclaran, se puede deducir de los datos (por ejemplo, con Nochevieja), con menos seguridad.
- **Recogida y limpieza**: en Madrid hay 4.272 quejas sobre la maquinaria de limpieza y 667 sobre el camión de basura desde 2023. Es el mismo aviso de picos nocturnos que en Barcelona.
