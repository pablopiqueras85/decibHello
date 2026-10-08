Borrador del director (8 oct 2026); el agente lo revisa y completa al despertar.

# Agente 1: web y lista de espera — estado

## Encargo

- Web de presentación de DecibHello con lista de espera, en `web/`.
- Rama `agente/web-lista-espera`, sacada de `main`. Sesión `session_01AKVCMzunJ9suXjcJRcHFEd`.
- No toca `piloto/`. El buscador usa el motor común `piloto/paquete/decibhello.js`, que genera el director.

## Hecho

- **Web publicada** (6 oct) como artifact privado, con vídeo de portada (plaça de Catalunya, Coverr) comprimido a 720p en mp4 y webm, más una imagen fija.
- **Guion**: un viernes en Tuset 20, de 7:00 a 7:00. Al bajar se hace de noche y un marcador enseña la hora, los dB y la nota reales (sensor de Tuset 30). Bloques y textos en [GUION.md](GUION.md).
- **Maqueta de la extensión de Chrome** (bloque 3b), con un anuncio inventado y la casilla "Avísame también cuando salga la extensión".
- **Buscador real** con el motor común: dirección o enlace de Google Maps → nota, franjas, noches, exterior o interior, picos, obras, planta, esquina, margen y medias del barrio y de Barcelona (7 oct).
- **Votación de la próxima ciudad** con fotos (colección `votos`, sin correo) y **lista de espera** guardada en la base de datos del artifact.
- **Cifras** sacadas del piloto con [datos/extraer.mjs](datos/extraer.mjs) → `datos/extraccion.json`. Créditos y licencias en [CREDITOS.md](CREDITOS.md).
- **Integrada en `main`** el 8 oct 2026.

## Falta

- Foto del área metropolitana: puesta (8 oct; L'Hospitalet, Jorge Franganillo, CC BY 2.0).
- Guiones de los vídeos de plastilina: borrador en [GUIONES-VIDEOS.md](GUIONES-VIDEOS.md) (8 oct), pendiente de que Pablo los apruebe.
- De Pablo: su vídeo con sonido.
- Ideas abiertas del guion: páginas por ciudad, dónde va el recuadro de la extensión, avisos del marcador, ritmo de los bloques, el mismo viaje en Pomaret 20 e idiomas.
- Abrir la lista de espera al público: hoy solo funciona para personas invitadas. Hace falta dominio propio y un formulario.
- Revisar y completar este borrador.

## Decisiones de Pablo

- El vídeo de portada lo descargó Pablo (Coverr, uso comercial libre). Si aparece uno con más gente y coches, se cambia con los mismos nombres de fichero.
- Siguiente ciudad: Madrid (6 oct). El piloto de Madrid espera a terminar Barcelona.
- Por decidir: nombre, dominio, idiomas (castellano, catalán, inglés) y cómo tratar los anuncios de portales (hoy se pide la calle).

## Enlaces

- Web: https://claude.ai/artifact/KrBrXRxafoU2cScYv55FjD (privado)
- Visor: https://claude.ai/artifact/AoLUjYUaWy6arbZLiL9vje (privado)
- Guion: [GUION.md](GUION.md) · Créditos: [CREDITOS.md](CREDITOS.md)
- Motor común: [piloto/paquete/decibhello.js](../piloto/paquete/decibhello.js)
- Equipo y ramas: [docs/agentes.md](../docs/agentes.md)
