# Créditos y fuentes de la web

## Datos
- Ajuntament de Barcelona, Open Data BCN (https://opendata-ajuntament.barcelona.cat/): mapa estratégico de ruido 2017, red de sensores de ruido (datos por hora de 2023), locales de ocio, obras públicas y quejas IRIS.
- Las notas de la página salen del piloto (`piloto/resultados.csv` y `piloto/visor.html`). Se extraen con `web/datos/extraer.mjs` a `web/datos/extraccion.json`.

## Portada
- Vídeo: "Empty Plaça de Catalunya in Barcelona", Coverr: https://coverr.co/videos/empty-placa-de-catalunya-in-barcelona-f01pou1l9s
  - Licencia: Coverr License (https://coverr.co/license/): uso comercial gratuito, sin atribución obligatoria.
  - Autor: Coverr no lo indica en la ficha.
  - Lo descargó Pablo (1080p, 12,9 s). Comprimido sin sonido a 1280×720 y 25 fps: `media/portada.mp4` (H.264, 0,8 MB) y `media/portada.webm` (VP9, 0,5 MB). Imagen fija: `media/portada.jpg` (segundo 5).
  - Ojo: la plaza sale casi vacía. Si aparece un vídeo del Eixample o de Gràcia con gente y coches, se puede cambiar dejando los mismos nombres de fichero.
- Si el vídeo no carga, o con "reducir movimiento", la portada muestra una ilustración animada propia (trama del Eixample dibujada en canvas, sin derechos de terceros).

## Tipografías
- Schibsted Grotesk, Source Serif 4 e IBM Plex Mono (Google Fonts, licencia SIL Open Font License).
