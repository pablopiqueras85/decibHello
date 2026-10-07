# DecibHello — Actualización (noche del 5 al 6 de octubre de 2026)

## Resumen

Con los datos de los sensores que pasaste, la nota ya no depende de supuestos míos para las horas y los días de la semana: usa lo que midieron 135 sensores municipales en 2023. Además, en 352 tramos de la ciudad la nota sale directamente de la medición de un sensor. Todo está en la rama `claude/keen-bohr-5oenpq` y en el visor (mismo enlace).

## Qué he hecho

1. **Encontrado y corregido un error en los datos del Ajuntament.** De 7:00 a 23:59 la fecha registrada es la del día siguiente (de 0:00 a 6:59 es correcta). Lo detecté porque el tráfico salía mínimo los lunes y la verbena de Sant Joan aparecía el día 24. Comprobado también con Navidad y Semana Santa. Sin esta corrección, los días de la semana habrían salido cambiados.
2. **Patrones medidos en lugar de supuestos** (sin festivos ni vísperas):
   - tráfico de día: sábado −1,2 dB, domingo −2,2 dB;
   - ocio de noche: viernes +2,7 dB y sábado +2,4 dB; lunes −2,6, martes −2,5 y domingo −3,0. El jueves queda en la media (yo lo había sobrestimado);
   - la forma hora a hora del tráfico y del ocio, también medida.
3. **Donde hay sensor, manda la medición.** Los portales del mismo tramo que un sensor (a menos de 60 m) usan el nivel medido día a día y hora a hora. Salen con "confianza medida" y el visor dice qué sensor es.
4. **Comparación sensores frente al mapa oficial** (`piloto/validacion_sensores.md`, 140 sensores):
   - en calles de tráfico el mapa acierta: +0,9 dB de diferencia mediana de noche;
   - en zonas de ocio se queda corto: +2,6 dB de mediana y **hasta +18 a +27 dB** en plazas y calles pequeñas de Gràcia, el Born y Sant Antoni (Raspall, Puigmartí, Fonollar, Comte Borrell);
   - Consell de Cent confirma el eje verde: el sensor mide 6,6 dB menos que el mapa de 2017, y su nota baja de 82 a 72.
   - Probé si bares, quejas o anchura de la calle explican esa diferencia: apenas (mejora de 0,2–0,3 dB). No he inventado una corrección.
5. ~~Aviso nuevo en el visor sobre la noche en calles de ocio~~: retirado el 6 de octubre, porque los datos no lo respaldan (ver abajo).
6. **Documentación**: informe del piloto actualizado (`piloto/resultados.md`), `piloto/README.md` con cómo regenerarlo todo, fuentes de datos y pendientes al día.
7. **Comprobado**: el visor y el cálculo en Python dan exactamente las mismas notas en las 26 direcciones (nota global, 7 noches y aviso de picos).

## Cambios que notarás en el visor

- Las notas han cambiado algunos puntos, sobre todo por día de la semana. Ejemplo: Verdi 20 sube de 75 (lunes) a 85 (viernes) de noche.
- Calles con sensor (Consell de Cent, Aragó 300, Blai 20, Rambla del Poblenou 60, Enric Granados 50…) muestran "confianza medida".

## Lo que necesito de ti

1. Tu **nota a ciegas** (0–100, día y noche) de Tuset 20, Travessera de Gràcia 81, 150 y 300 y Martínez de la Rosa 20. Ya se ven en el visor, así que si quieres que sea a ciegas, puntúalas antes de abrirlo.
2. El **tramo silencioso de Travessera de Gràcia**.
3. Si te parece razonable que Travessera de Gràcia 150 mida unos 8 m de ancho.
4. Cuando quieras: la **solicitud al Ajuntament** sobre contenedores y horarios de recogida (borrador en `decibhello-fuentes-datos-barcelona.md`, apartado 2.13).

## Pendiente que queda

- Datos de sensores minuto a minuto, para los picos cortos (camiones de basura).
- Cómo detectar el ocio que el mapa no ve en calles sin sensor (opiniones de vecinos, mediciones con móvil).
- Pasar del mapa de 2017 al de 2022.
- El resto, en `decibhello-pendientes.md`.

## Actualización del 6 de octubre: el ruido de ocio que el mapa no ve

Detalle completo en `piloto/ocio_oculto.md` (script `piloto/ocio_oculto.py`).

- **Pistas nuevas**: bares (sin restaurantes), bares musicales y discotecas, locales abiertos 24 h, terrazas con su número de mesas, quejas por motivo (gente en la calle, salida de locales, músicos, fiestas, terrazas), pisos turísticos, plazas, anchura de la calle y los componentes del propio mapa.
- **Entrenamiento con 140 sensores**, validando por distritos (el modelo nunca ve el distrito que se evalúa).
- **La trampa**: un modelo con todo parecía mejorar mucho, pero la mejora venía del nivel del propio mapa. Los sensores en zonas "tranquilas" del mapa se pusieron por quejas, así que esa regla subiría el ruido de calles de verdad tranquilas. **No se aplica.**
- **De noche, ninguna pista pública predice dónde se equivoca el mapa.** Retirado el aviso nocturno que puse anoche.
- **De día y por la tarde, sí**: con 10 o más bares a menos de 100 m, el mapa se queda corto (mediana +7 dB de día y +12 dB por la tarde). El mapa no modela el ocio fuera de la noche. Se corrige con una estimación prudente: **+6 dB de día y +8,8 dB por la tarde**, en ~1.000 tramos (2,6 % de la ciudad). En esos sensores, el error de tarde baja de 11 a 4 dB.
- **Para la noche hace falta medir**: mediciones con el móvil, opiniones de vecinos o más sensores.

## Actualización del 6 de octubre (tarde): bares y discotecas suman en proporción

- La regla de "zona de bares" (todo o nada a partir de 10 bares) se sustituye por una **suma proporcional**: cuantos más bares y bares musicales o discotecas haya a menos de 100 m, más dB se suman, en las tres franjas. Sin locales no se suma nada.
- Coeficientes (dB por log(1 + número)), ajustados con los sensores y validados dejando fuera cada distrito: día 1,32 (bares) y 1,68 (musicales); tarde 2,90 y 0,72; noche 1,93 y 0. Ejemplo: 10 bares ≈ +3,2 / +7,0 / +4,6 dB; con 5 musicales más ≈ +6,2 / +8,2 / +4,6 dB.
- Error medio con validación por distritos: día 4,47 → 4,43 dB, tarde 5,91 → 4,99 dB, noche 4,33 → 4,16 dB.
- **Pisos turísticos**: los sensores no muestran que suban el nivel medio de la hora (coeficiente 0). Cuentan en el **aviso de picos nocturnos**: 20 o más a menos de 100 m suben el aviso (llegadas y salidas a deshoras).
- En el visor, "Por qué suena así" muestra los bares musicales y discotecas y cuántos dB suma cada franja.

## Actualización del 6 de octubre (noche): escala nueva

- **Problema**: con la escala anclada en la OMS (45 dB de noche = 50), el 84 % de los portales de Barcelona salía "ruidoso" o "muy ruidoso" y ninguno bajaba de 33.
- **Cambio**: la nota va ahora de los extremos reales de Barcelona. Día y tarde: 45 dB = 0, 75 dB = 100. Noche: 35 dB = 0, 70 dB = 100. Lineal, sin compresión. Etiquetas cada 20 puntos.
- **Resultado en toda la ciudad**: 35 % tranquilo o muy tranquilo, 23 % moderado, 42 % ruidoso o muy ruidoso.
- **Ejemplos**: Tuset viernes 1:00 = 100 (antes 86); Tuset lunes noche = 58; Pomaret = 19 (antes 45); Campoamor = 50 (antes 62).
- **Nuevo en el visor**: "más ruidosa (o más tranquila) que el X % de los portales de Barcelona", con la nota media del día de la fachada.
- **Pendiente**: las grandes avenidas quedan todas cerca de 100; afinar con tus notas a ciegas.

## Actualización del 6 de octubre: obras públicas

- **Datos**: Open Data BCN publica las obras en el espacio público (1.919 desde 2022, ~300 en curso) con polígono, tipo, estado y fechas.
- **Validación con sensores (2023)**: una obra a menos de 25 m sube el ruido de día laborable una mediana de +2 dB mientras dura (Enric Granados, reurbanización: +8 dB; Escudellers, pavimentación: +5 a +6 dB). A 25–75 m, +0,4 dB; a 300–600 m (control), nada.
- **En la nota**: obra en curso a menos de 25 m → +2 dB de 8 a 18 h, de lunes a viernes, hasta la fecha de fin. Desaparece sola cuando termina. No suman las previstas, las paradas ni los grandes proyectos (túnel de la L9, Camp Nou…), que se muestran como aviso.
- **En el visor**: bloque "Obras" con las obras a menos de 100 m (distancia, tipo, fechas y ficha) y cuánto cambia la nota.
- **Pendiente**: obras privadas de edificios; actualización diaria en el portal.

## Actualización del 6 de octubre: obras al día

- Las **obras públicas** se actualizan a diario en Open Data BCN. Una tarea programada las descarga de lunes a viernes a las 6:47, regenera el visor y lo republica en el mismo enlace.
- Las **quejas vecinales (IRIS)** se publican cada trimestre (las de 2026 llegan a marzo): no sirven para un aviso del día, así que no se usan para obras.
- Las **obras privadas** siguen pendientes de la solicitud de transparencia (borrador en `decibhello-fuentes-datos-barcelona.md`, apartado 2.15).

## Actualización del 6 de octubre (tarde): equipo de agentes, web y Madrid

- **Equipo de agentes**: seis agentes con su encargo, su rama y su carpeta (`decibhello-agentes.md`). Se despiertan a petición de Pablo.
- **Web** (agente 1): landing con vídeo, historia con datos reales del piloto, buscador de calles, votación de la próxima ciudad y lista de espera. https://claude.ai/artifact/KrBrXRxafoU2cScYv55FjD
- **Motor común**: el modelo y el buscador en JavaScript están en `piloto/motor.js`. El visor y la web usan la misma pieza (`piloto/paquete/decibhello.js`), así que dan la misma nota.
- **Siguiente ciudad: Madrid** (agente 5, confirmado por Pablo). Tiene mejor mapa (2021, dB exactos cada 5 m) y mejor censo de locales que Barcelona. Le faltan sensores por hora: hay que pedirlos por transparencia (borrador listo).

## Actualización del 7 de octubre: planta del piso

- **Nuevo selector "Planta"** en el visor: bajo, 1.º, 2.º… hasta la última planta del edificio, y ático.
- **Cómo se calcula** (estimación a partir de estudios de calles, aún sin medir en Barcelona): el mapa oficial calcula a la altura de un 1.º. En una calle estrecha entre edificios altos el sonido rebota y casi no cambia con la altura. En una calle ancha baja poco a poco. El ático retirado gana unos 3 dB por la pantalla del pretil, y el bajo suma 1 dB.
- **Datos**: las plantas de cada edificio salen del Catastro y la anchura de la calle, del índice.
- **Ejemplos**: Diagonal 500, 6.º: −3,9 dB (nota 71). Tuset 20, 8.º: igual que un 1.º (calle de 23 m con edificios de 10 plantas). Tuset 20, ático: −3 dB. Verdi 20, bajo: +1 dB.
- **También**: arreglado un recuadro de obras vacío que salía en calles sin obras.
