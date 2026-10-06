# Guion de la web de DecibHello

La página es un viernes en el Carrer de Tuset 20, de 7:00 a 7:00. Al bajar se hace de noche y el marcador enseña la hora, los dB y la nota reales de cada hora (media de los viernes de 2023, sensor de Tuset 30).

Este fichero sirve para retocar el guion sin leer el código. Cada bloque dice a qué hora del viernes cae, qué cuenta y qué texto lleva. Si cambias algo aquí, pide que se lleve a `index.html`.

## Bloques, en orden

| # | Hora aprox. | Fondo | Bloque | Para qué sirve |
|---|---|---|---|---|
| 0 | — | vídeo | **Portada**: "Escucha la calle antes de firmar." | La promesa en una frase |
| 1 | 7:00–9:00 | mañana | **Presentación**: esta página es un viernes en Tuset 20 | Explicar el juego del scroll y el marcador |
| 2 | 10:00 | mañana | **"Visitas el piso un martes a las once. Hay luz. Firmas."** + pegatinas (terraza, camión, bar musical, hora punta, obras) | El problema: el ruido se descubre tarde |
| 3 | 12:00 | mediodía | **"Las fotos no tienen sonido."** + escala 0–100 | Los datos existen pero no se ven; qué es la nota |
| 4 | 15:00 | tarde | **"El mismo portal suena distinto cada día."** + gráfico con deslizador (día elegido frente al lunes) | Momento interactivo |
| 5 | 17:00 | tarde | **"Tres calles, tres maneras de vivir."** Pomaret 19, Tuset 75, Gran Via 98 | Comparar calles |
| 6 | 19:00 | atardecer | **"Barcelona es ruidosa de noche."** 35 % tranquilo, 23 % moderado, 42 % ruidoso | El problema es de toda la ciudad |
| 7 | 20:00–22:00 | crepúsculo | **"Cómo lo medimos."** Mapa, sensores, ocio, obras, picos | Confianza: de dónde salen los datos |
| 8 | 22:00 | noche | **"La noche del lunes, Tuset saca un 60. La del viernes, un 93."** + barras de la semana | El día de la semana importa |
| 9 | 0:00 | noche | **"Mismo portal. Otro piso."** Exterior 75, interior 25 | Exterior frente a interior |
| 10 | 2:00 | noche | **"Así es un informe."** Hoja de Tuset 20 + enlace al visor | Qué recibe el usuario |
| 11 | 4:00 | madrugada | **"Apúntate antes de firmar."** + formulario | La acción |
| 12 | 6:30 | amanecer | **Pie**: fuentes y créditos | |

Todas las cifras salen del piloto (`piloto/resultados.csv`, `piloto/resultados.md` y el visor). No hay testimonios ni cifras inventadas.

## Ideas abiertas para retocar

- **Extensión de Chrome**: el sitio natural es justo después del bloque 3 ("Las fotos no tienen sonido"). Ahí se habla de los anuncios, así que encaja enseñar un anuncio de ejemplo con la nota de DecibHello encima, con una pegatina "Extensión de Chrome · próximamente". El anuncio debe ser inventado y marcado como ejemplo: sin logotipos ni capturas de portales reales. Otra opción es mostrarla como segunda vía en el formulario ("Avísame cuando salga la extensión").
- **Buscador dentro de la página**: en el bloque 10, en lugar del enlace al visor, un buscador real de calle (hoy el visor es privado).
- **El marcador**: que avise con una pegatina cuando cruza un umbral ("Ahora es muy ruidoso"), o que suene un clic suave al pasar de franja (solo si el usuario lo activa).
- **Ritmo**: decidir si cada bloque debe caer en su hora exacta (hoy la hora la marca la posición en la página y es aproximada).
- **Otras calles**: repetir el viaje con Pomaret 20 como contraste ("el mismo viernes en una calle tranquila").
- **Idiomas**: castellano, catalán e inglés (decisión pendiente).
- **Público abierto**: la lista de espera solo funciona para personas invitadas a la página. Para abrirla hace falta dominio propio y un formulario.

## Cómo pedir retoques

- Comenta directamente sobre la página (modo comentario del artifact): el comentario llega a Claude con el trozo exacto señalado.
- O escribe aquí o al director: "en el bloque 6 cambia…".
