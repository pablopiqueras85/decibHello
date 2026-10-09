# Correo a Open Data BCN

No es una solicitud de transparencia: es una consulta. No hay plazo legal ni reclamación.

## Dónde se envía

- Formulario de contacto / canal de consultas de Open Data BCN: https://w10.bcn.cat/APPS/irsconsultesWeb/continuar.executant.do?i=e&origen=DADES_OBERTES&detall=4675 (enlace que aparece en la ficha de Open Data BCN en datos.gob.es; sin comprobar que siga activo).
- Portal: https://opendata-ajuntament.barcelona.cat (la sección "Contacte" lleva al mismo canal; sin comprobar).
- No se ha encontrado un correo directo comprobado. No uses `opendata@bcn.cat` sin verificarlo (sin comprobar).

## Qué necesitas

- Tu nombre y un correo: `[NOMBRE Y APELLIDOS]`, `[CORREO]`. No hace falta DNI.
- Estar registrado en el portal solo hace falta para obtener el token de acceso (ver abajo).

## Pista sobre el token

Open Data BCN tiene una página "Token d'accés" (https://opendata-ajuntament.barcelona.cat/en/tokens). No se pudo abrir: pide verificación anti-robots y no se ha saltado. Según un resumen de búsqueda (sin comprobar):

- Algunos recursos que se actualizan a menudo se descargan con un token personal.
- El token va en la cabecera `Authorization` de la petición.
- Hace falta cuenta en el portal.
- La API del catálogo (CKAN) es pública y no necesita token.

**Pablo, antes de enviar**: abre esa página con tu navegador y mira si los sensores de ruido y los ráster aparecen allí. Si es así, quita del correo la pregunta 3 sobre el token.

## Asunto

Consulta sobre el mapa de ruido 2022 por tramo y el acceso automático a datos de sensores y ráster

## Texto para copiar

```
Buenos días:

Soy [NOMBRE Y APELLIDOS] y estoy desarrollando DecibHello, un servicio informativo que da a cada portal de Barcelona una nota de ruido de 0 a 100 antes de alquilar o comprar. Uso los datos abiertos del Ajuntament y quería hacerles tres preguntas.

1. Mapa estratégico de ruido 2022. Hoy uso el mapa de 2017 por tramo de calle. ¿Existe una versión de 2022 por tramo de calle (Lden, Ld, Le, Ln), como la de 2017? Si existe, ¿dónde está y en qué formato? Si solo está en ráster o en mapa, ¿está previsto publicar la versión por tramo?

2. Sensores de ruido (Sentilo). Los datos minuto a minuto de la red de sensores solo he podido bajarlos a mano desde la web, que pide verificación anti-robots. ¿Hay una forma de acceso automático (API, descarga programada o fichero periódico) a los datos minuto a minuto de los sensores y a los ráster de 2022? Si es necesario un acuerdo o una solicitud, ¿a quién debo dirigirme?

3. Token de acceso. He visto la página "Token d'accés". ¿Sirve para descargar de forma automática estos recursos (sensores y ráster)? Si es así, ¿qué recursos lo admiten y qué límites de uso tiene?

Respeto la verificación anti-robots y no la salto: por eso pregunto cuál es el camino previsto.

Si hay documentación sobre cómo el Ajuntament calcula la fecha de los datos de noche y de 7:00 a 23:59 en los ficheros de sensores, también me sería de gran ayuda.

Gracias por su tiempo. Si les sirve, puedo explicarles el uso que hago de los datos y compartir los resultados de la validación.

Un saludo,
[NOMBRE Y APELLIDOS]
[CORREO]
```

## Formato que pedimos

Respuesta por correo, con enlaces a los conjuntos de datos y a la documentación.

## Plazo

No hay plazo legal. Suelen contestar en unos días o semanas (sin comprobar).

## Si no contestan

- Esperar 3 semanas y enviar de nuevo.
- Usar la sugerencia de datos del propio portal.
- Como último recurso, una solicitud de transparencia al Ajuntament (Llei 19/2014) pidiendo esos ficheros. Se reclamaría a la GAIP en un mes.
