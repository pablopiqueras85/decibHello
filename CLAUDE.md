# DecibHello

Plataforma para consultar el ruido de una calle o portal antes de alquilar o comprar. Empieza por Barcelona. El usuario (Pablo) escribe en castellano: responde y documenta en castellano, con frases cortas y sin jerga.

## Qué hay

Repositorio `pablopiqueras85/decibHello` (Pablo lo renombró con H mayúscula; el nombre antiguo redirige), rama principal `main`. La portada (`README.md`) tiene el mapa completo. El repositorio `pablopiqueras85/Ideas` es el archivo antiguo: no se trabaja ahí.

- `docs/concepto.md`: idea, escala, competencia y modelo de negocio.
- `docs/fuentes-datos-barcelona.md`: fuentes de datos, cómo se accede y borradores de solicitudes de transparencia (2.13 recogida de basuras, 2.15 obras privadas).
- `docs/pendientes.md`: pendientes y hoja de ruta. **Léelo antes de empezar** y márcalo al terminar algo. Arriba está "Ahora mismo", la lista corta de lo abierto: es lo primero que se lee tras un resumen de la conversación, y se actualiza cada vez que algo se abre o se cierra.
- `docs/agentes.md`: equipo de agentes (sesiones, ramas, carpetas) y cómo se les despierta.
- `docs/actualizaciones.md`: registro de cambios para el usuario, por fechas. Añade una sección cuando cambies algo que él note.
- `docs/direcciones-piloto.md`: las direcciones del piloto y lo que se esperaba de cada una.
- `piloto/`: el prototipo de Barcelona (ver `piloto/README.md`).
- `docs/organigrama.html`: fuente del organigrama, publicado en https://claude.ai/artifact/HwD9FCVjj4BNHn5BHUGc2h. Si cambia el equipo, se actualizan el organigrama y `docs/agentes.md`.
- `web/`: la web con lista de espera (agente 1), publicada en https://claude.ai/artifact/KrBrXRxafoU2cScYv55FjD. Guiones de los vídeos de plastilina en `web/GUIONES-VIDEOS.md`. `investigacion/`: el estudio de la siguiente ciudad (agente 5).

## El producto hoy

- Un buscador: se escribe una dirección o se pega un enlace de Google Maps y sale la nota. Los anuncios de portales inmobiliarios (Idealista…) no se pueden leer: se pide la calle.
- Visor: `piloto/visor.html`, publicado como artifact privado en https://claude.ai/artifact/AoLUjYUaWy6arbZLiL9vje. Se genera desde `piloto/visor_plantilla.html` con `python3 piloto/calcular_nota.py`. No edites `visor.html` a mano.
- Una tarea programada ("DecibHello: actualizar obras del visor", `trig_01HxeEp3F1ajZCVVNCd9CrsU`, lunes a viernes a las 6:47) clona este repositorio, regenera el índice y el visor (así se renuevan cada día obras, censo, quejas, pisos turísticos y terrazas) y republica el visor.
- La web lleva su propia copia del motor (`decibhello.js`). Cuando cambia `piloto/paquete/decibhello.js`, hay que republicar la web con el fichero nuevo: los ficheros que se publican deben estar en el directorio de trabajo o en el scratchpad (cópialos allí antes).

## Reglas del modelo (decididas con el usuario; no las cambies sin preguntar)

- **Nota 0–100, 100 = muy ruidoso.** Todo se mide igual: cada hora tiene un nivel en dB (medido por sensor o estimado) y la nota sale de la misma fórmula, lineal entre los extremos reales de Barcelona: día y tarde 45 dB = 0 y 75 dB = 100; noche 35 dB = 0 y 70 dB = 100. Etiquetas cada 20 puntos.
- Franjas: día 7–19, tarde 19–23, noche 23–7. Nota global = 30 % día + 20 % tarde + 50 % noche. El "día" va de 7:00 a 7:00.
- Nada suma "puntos" sueltos: todo entra como dB validados con los sensores municipales, dejando fuera cada distrito (validación cruzada). Si una pista no mejora frente a los sensores, se muestra como explicación o aviso, pero no suma.
- Ya incluido: mapa estratégico de ruido 2017 por tramo, perfiles horarios y por día medidos con sensores, sensores de la misma calle (≤ 120 m), suma proporcional por bares y bares musicales/discotecas (censo de 2024 y Overture Maps, cada uno vale la mitad), horarios de los locales de noche, obras públicas en curso a menos de 25 m (+2 dB de día laborable), exterior frente a interior (patio), aviso de picos nocturnos (calle estrecha, quejas de recogida, pisos turísticos).
- Excepción acordada: la **planta del piso** es una estimación a partir de estudios de calles (calle estrecha y alta: casi igual en todas las plantas; calle ancha: baja con la altura; ático −3 dB; bajo +1 dB), con la altura del edificio del Catastro y la anchura de la calle. Se muestra como estimación hasta medirla con el sonómetro en varias plantas.
- Margen de error: sin sensor, el error que no se supera en 2 de cada 3 sensores (`piloto/incertidumbre.json`, validado por distritos); con sensor, la diferencia entre dos sensores de la misma calle. Se muestra como "entre X y Y".
- Escala dada por buena por Pablo (8 oct 2026), con estas referencias: 20 = calle residencial tranquila (Pomaret), 50 = moderado, 75 = Tuset 20 de media, 100 = Tuset un viernes de madrugada. El 0 casi no se alcanza (solo 5 de cada 100 portales bajan de 10). Las notas a ciegas de las calles de control quedan para cuando se pula la escala.
- Validador humano: el usuario vive cerca de Tuset / Travessera de Gràcia. Tuset de jueves a sábado de madrugada = 100; un domingo a las 15:00 no es ruidoso; Tuset, Travessera y Balmes son ruidosas en hora punta.

## Cómo trabajar

- El modelo existe dos veces: `piloto/modelo.py` (Python) y su copia en JavaScript `piloto/motor.js` (modelo, índice y buscador). **Cualquier cambio en uno va en el otro.** `calcular_nota.py` mete `motor.js` en el visor y genera `piloto/paquete/decibhello.js` (motor + datos en un solo fichero) para otras páginas, como la web: `window.DecibHello.buscar("Tuset 20")`. Nadie copia la fórmula a mano. Después ejecuta:
  ```bash
  python3 piloto/indice.py        # solo si cambian los datos del índice (≈1 min, descarga Open Data BCN)
  python3 piloto/calcular_nota.py # notas del piloto + visor.html
  cd piloto/pruebas && npm install && node paridad.mjs   # visor y paquete: deben dar 0 diferencias
  ```
  Chromium está en `/opt/pw-browsers/chromium`; no ejecutes `playwright install`.
- Mira el visor en el móvil (390 px de ancho) y en escritorio antes de publicar.
- Datos: API del datastore de Open Data BCN (`datastore_search`, `datastore_search_sql`). Las descargas directas de ficheros piden verificación anti-robots: **nunca la saltes**; pide al usuario que los descargue.
- Los CSV de sensores de 2023 (`piloto/sensores/`, ~50 MB) no están en el repositorio. Solo hacen falta para `sensores.py`, `ocio_oculto.py` y `obras.py`; si los necesitas, pídeselos al usuario.
- Sensores: de 7:00 a 23:59 la fecha registrada es la del día siguiente (`sensores.py` lo corrige).
- Bares y locales de noche: censo de 2024 y Overture Maps (`piloto/overture.py` → `piloto/datos/overture_locales.json.gz`). Overture sale cada mes: cambia `VERSION` y regenera. Google Maps no se usa como fuente: sus condiciones no dejan guardar datos ni copiarlos del mapa; solo serviría para consultas en directo en un portal propio.
- Mapa de ruido: por tramo de calle solo existe hasta 2017 (lo que usa el modelo). El de 2022 solo está en ráster (`rasters-mapa-estrategic-soroll`, ficheros `2022_Raster_Total_Dia/Vespre/Nit`), con verificación anti-robots: lo descarga Pablo. Se buscó una copia en la Agencia Europea de Medio Ambiente (`piloto/cache/mes2022/eea_end2022_ES.gpkg`, toda España, sin revisar).
- `ancho_m` se mide de portal a portal: sale unos 2 m más ancho que entre fachadas (comprobado con el Catastro en Travessera de Gràcia). No cambia la nota.
- Ramas: el director trabaja en `main`. Cada agente trabaja en su rama `agente/<nombre>`, sacada de `main`. Integrar es hacer merge a `main` cuando Pablo lo aprueba. No toquéis los mismos ficheros a la vez (sobre todo `modelo.py`, `motor.js`, `visor_plantilla.html` y `calcular_nota.py`).
- No abras pull requests salvo que Pablo lo pida.
- Subagentes: Pablo pide usarlos para tareas pesadas o de búsqueda, con Sonnet para lo ligero y Opus solo cuando haga falta. Que escriban solo sus ficheros y no hagan commit: el director revisa, sube y publica. El uso tiene un límite por sesión: si se agota, los subagentes se cortan a medias.
- Lista de tareas: el director lleva su lista de tareas de la sesión y una copia en "Ahora mismo" de `docs/pendientes.md`.
- Memoria de cada agente: `<su carpeta>/ESTADO.md`, en su rama (encargo, qué está hecho, qué falta, decisiones de Pablo, enlaces). Léelo al empezar y actualízalo y súbelo al terminar: la conversación puede resumirse o perderse, el fichero no. El director hace lo mismo con `docs/pendientes.md` y `docs/agentes.md`.
