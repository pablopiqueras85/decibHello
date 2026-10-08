# DecibHello

Nota de ruido de 0 a 100 para cada portal de Barcelona, por hora y día de la semana (100 = muy ruidoso).

DecibHello sirve para saber cuánto ruido hay en una calle o un portal antes de alquilar o comprar un piso. Se escribe una dirección, o se pega un enlace de Google Maps, y sale la nota hora a hora y de lunes a domingo, con de dónde viene el ruido: tráfico, bares y discotecas, obras o camiones de recogida. Empieza por Barcelona, con datos abiertos del Ajuntament comprobados con sus sensores de ruido.

## Enlaces

Son privados: solo los abre Pablo.

- **Visor** (buscador y nota de cada portal): https://claude.ai/artifact/AoLUjYUaWy6arbZLiL9vje
- **Web** con lista de espera: https://claude.ai/artifact/KrBrXRxafoU2cScYv55FjD
- **Organigrama** del equipo: https://claude.ai/artifact/HwD9FCVjj4BNHn5BHUGc2h

## Qué hay en el repositorio

- [`README.md`](README.md): esta portada.
- [`CLAUDE.md`](CLAUDE.md): instrucciones para los agentes: reglas del modelo y cómo trabajar.
- [`docs/`](docs/): documentación del proyecto.
  - [`concepto.md`](docs/concepto.md): idea, escala, competencia y modelo de negocio.
  - [`fuentes-datos-barcelona.md`](docs/fuentes-datos-barcelona.md): fuentes de datos, cómo se accede y borradores de solicitudes de transparencia.
  - [`pendientes.md`](docs/pendientes.md): lo abierto ahora mismo y la hoja de ruta.
  - [`agentes.md`](docs/agentes.md): el equipo de agentes, sus ramas y cómo se les despierta.
  - [`actualizaciones.md`](docs/actualizaciones.md): registro de cambios para Pablo, por fechas.
  - [`direcciones-piloto.md`](docs/direcciones-piloto.md): las direcciones del piloto y lo que se esperaba de cada una.
- [`piloto/`](piloto/): el prototipo de Barcelona. Detalle en su [README](piloto/README.md).
  - [`modelo.py`](piloto/modelo.py): el modelo de la nota, en Python.
  - [`motor.js`](piloto/motor.js): el mismo modelo en JavaScript, con el índice y el buscador.
  - [`indice.py`](piloto/indice.py): el índice de toda la ciudad (cada portal con su tramo del mapa de ruido y lo que tiene cerca).
  - [`calcular_nota.py`](piloto/calcular_nota.py): calcula las notas del piloto y genera el visor y el paquete.
  - [`visor_plantilla.html`](piloto/visor_plantilla.html): plantilla del visor. De ella sale `visor.html` (generado, no se edita a mano).
  - [`paquete/decibhello.js`](piloto/paquete/decibhello.js): motor y datos en un solo fichero para otras páginas, como la web (generado).
  - [`pruebas/paridad.mjs`](piloto/pruebas/paridad.mjs): comprueba que Python y JavaScript dan las mismas notas.
  - [`resultados.md`](piloto/resultados.md): notas del piloto y conclusiones.
- [`web/`](web/): la web de presentación con lista de espera (agente 1).
  - [`index.html`](web/index.html): la página. [`GUION.md`](web/GUION.md): los bloques y sus textos. [`CREDITOS.md`](web/CREDITOS.md): fuentes y licencias. [`ESTADO.md`](web/ESTADO.md): estado del agente.
- [`investigacion/`](investigacion/): el estudio de la siguiente ciudad (agente 5).
  - [`siguiente-ciudad.md`](investigacion/siguiente-ciudad.md): Madrid, Valencia y el área metropolitana, fuente a fuente.
  - [`siguiente-ciudad-madrid-valencia.md`](investigacion/siguiente-ciudad-madrid-valencia.md): la comparación final y la recomendación (Madrid).
  - [`solicitud-transparencia-madrid.md`](investigacion/solicitud-transparencia-madrid.md): borrador de las solicitudes al Ayuntamiento de Madrid.
  - [`notas/`](investigacion/notas/): notas de trabajo. [`ESTADO.md`](investigacion/ESTADO.md): estado del agente.

## Cómo se actualiza

Una tarea programada ("DecibHello: actualizar obras del visor") regenera el visor con las obras públicas del día y lo republica en el mismo enlace. Se ejecuta de lunes a viernes a las 6:47 (hora de Madrid). Si algo falla, no publica.

## Cómo regenerar a mano

```bash
python3 piloto/indice.py        # solo si cambian los datos del índice (≈1 min, descarga Open Data BCN)
python3 piloto/calcular_nota.py # notas del piloto + visor.html
cd piloto/pruebas && npm install && node paridad.mjs   # visor y paquete: deben dar 0 diferencias
```

- El modelo existe dos veces: [`modelo.py`](piloto/modelo.py) y [`motor.js`](piloto/motor.js). Cualquier cambio en uno va en el otro; la prueba de paridad lo comprueba.
- `piloto/visor.html` y `piloto/paquete/decibhello.js` se generan: no se editan a mano.
- La prueba usa el Chromium de `/opt/pw-browsers/chromium`.
- Dependencias de Python y el resto de scripts, en el [README del piloto](piloto/README.md).

## Cómo trabajamos

- **Pablo** decide y valida. El **director** (la sesión principal de Claude) mantiene el modelo, el visor y la documentación, y trabaja en `main`.
- Cada **agente** tiene un encargo y una carpeta, y trabaja en su rama `agente/<nombre>`, sacada de `main`. Están dormidos hasta que Pablo pide algo.
- **Integrar** es hacer merge a `main` cuando Pablo lo aprueba. No se abren pull requests salvo que Pablo lo pida.
- **Memoria**: cada agente guarda su estado en `ESTADO.md`, dentro de su carpeta. El director lleva [`docs/pendientes.md`](docs/pendientes.md) y [`docs/agentes.md`](docs/agentes.md).
- El equipo completo y cómo se despierta a cada agente, en [`docs/agentes.md`](docs/agentes.md).

---

Proyecto privado. Datos de Open Data BCN (CC BY 4.0) y del Catastro; fuentes y licencias en [`docs/fuentes-datos-barcelona.md`](docs/fuentes-datos-barcelona.md).
