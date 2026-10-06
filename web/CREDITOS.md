# Créditos y fuentes de la web

## Datos
- Ajuntament de Barcelona, Open Data BCN (https://opendata-ajuntament.barcelona.cat/): mapa estratégico de ruido 2017, red de sensores de ruido (datos por hora de 2023), locales de ocio, obras públicas y quejas IRIS.
- Las notas de la página salen del piloto (`piloto/resultados.csv` y `piloto/visor.html`). Se extraen con `web/datos/extraer.mjs` a `web/datos/extraccion.json`.

## Portada
- Fondo actual: ilustración animada propia (trama del Eixample dibujada en canvas). Sin derechos de terceros.
- Vídeo: **pendiente**. Desde este entorno no se ha permitido la descarga, y Pexels y Pixabay piden verificación anti-robots.

### Vídeo propuesto (lo descarga Pablo)
- "People walking in Spain", Coverr: https://coverr.co/videos/people-walking-in-spain-bv25chbp7d
  - Fichero: botón "Download", 1080p.
  - Licencia: Coverr License (https://coverr.co/license/): uso comercial gratuito, sin atribución obligatoria.
  - Autor: el que indique la página del vídeo (anotarlo aquí al descargarlo).
  - Ojo: Coverr no dice que sea Barcelona. Si encuentras uno del Eixample o de Gràcia con gente y coches (por ejemplo en Pexels, buscando "Barcelona street"), mejor.
- Alternativa: "Cars driving down a road in Spain", Coverr: https://coverr.co/videos/cars-driving-down-a-road-in-spain-vowgyigbrd

Cuando lo tengas, súbelo como `web/media/original.mp4`. El agente lo comprime (`portada.mp4` H.264 y `portada.webm`, 720p, ≤ 8 MB, más `portada.jpg` como imagen fija) y republica. La página ya busca esos tres ficheros en `media/`.

## Tipografías
- Schibsted Grotesk, Source Serif 4 e IBM Plex Mono (Google Fonts, licencia SIL Open Font License).
