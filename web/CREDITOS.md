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
- Si el vídeo no carga, o con "reducir movimiento", la portada muestra la imagen fija `media/portada.jpg`.

## Maqueta de la extensión
- El anuncio, la dirección web (ejemplo.com) y la fachada son inventados y dibujados a mano. No se usan logotipos ni capturas de portales reales.

## Fotos de ciudades (Wikimedia Commons)
- Barcelona: "Barcelona Skyline as seen from Parc Güell", Chris Koerner, CC BY 2.0. https://commons.wikimedia.org/wiki/File:Barcelona_Skyline_as_seen_from_Parc_G%C3%BCell.jpg → `media/ciudad-barcelona.jpg`
- Madrid: "Madrid - Madrid skyline - 140314 195825", Barcex, CC BY-SA 3.0. https://commons.wikimedia.org/wiki/File:Madrid_-_Madrid_skyline_-_140314_195825.jpg → `media/ciudad-madrid.jpg`
- Valencia: "Skyline València", Francesc Fort, CC BY-SA 4.0. https://commons.wikimedia.org/wiki/File:Skyline_Val%C3%A8ncia.jpg → `media/ciudad-valencia.jpg`
- Reducidas a 900 px de ancho, sin otros cambios. El crédito va en el pie de la página.
- Área metropolitana: sin foto todavía (Commons limitó las descargas). Fondo propio de puntos. Pendiente: una foto de L'Hospitalet o Badalona con licencia CC, o una de Pablo.

## Buscador
- `decibhello.js` es `piloto/paquete/decibhello.js` (motor común que genera `piloto/calcular_nota.py`). La web lo publica junto a la página y lo carga solo al acercarse al buscador.

## Tipografías
- Gloock, Hanken Grotesk e IBM Plex Mono (Google Fonts, licencia SIL Open Font License).
