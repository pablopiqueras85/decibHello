# DecibHello — Equipo de agentes

Organigrama visual (privado): https://claude.ai/artifact/HwD9FCVjj4BNHn5BHUGc2h. Su fuente es [`organigrama.html`](organigrama.html): edítala y republícala en el mismo enlace. Si cambia el equipo, actualiza las dos cosas.

El director del proyecto es la sesión principal de Claude (la que habla con Pablo). Cada agente es una sesión aparte en claude.ai/code, con su propia rama y su encargo escrito en sus instrucciones. Están **dormidos**: solo empiezan cuando Pablo lo pide y el director les envía el mensaje. Ninguno toca `piloto/` (el modelo y el visor los mantiene el director).

## Repositorio y ramas

- Desde el 8 de octubre de 2026 el proyecto tiene repositorio propio: `pablopiqueras85/decibhello`, rama principal `main`.
- Cada agente trabaja en este repositorio, en su rama `agente/<nombre>`, sacada de `main`.
- Sus sesiones se crearon con el repositorio Ideas. Al despertarlos, el director les dice que añadan `pablopiqueras85/decibhello` y que trabajen ahí.
- La web (agente 1) y el estudio de ciudades (agente 5) ya están integrados en `main` (8 oct 2026).
- Las ramas antiguas quedan en Ideas como archivo: no se trabaja en ellas.

## Agentes

| # | Agente | Sesión | Rama | Carpeta | Estado |
|---|---|---|---|---|---|
| 1 | Web y lista de espera | `session_01AKVCMzunJ9suXjcJRcHFEd` | `agente/web-lista-espera` | `web/` | hecho (6 oct): landing en https://claude.ai/artifact/KrBrXRxafoU2cScYv55FjD con vídeo, buscador de calles (usa `piloto/paquete/decibhello.js`), voto de ciudades y lista de espera. Pendiente de Pablo: guiones de los vídeos de plastilina, su vídeo con sonido y una foto del área metropolitana. Integrado en `main` (8 oct) |
| 2 | Extensión de Chrome | `session_01VAn9UEcGXw6tfhhJ4Vu2Eg` | `agente/extension-chrome` | `extension/` | dormido |
| 3 | Sonómetro web | `session_01TP2VCShQMuQCnyVzeHegj7` | `agente/sonometro` | `sonometro/` | dormido |
| 4 | Entrevistas de validación | `session_015Fobjtmy4viNvwbz6ecU7i` | `agente/entrevistas` | `negocio/` | dormido |
| 5 | Siguiente ciudad | `session_01FjeojmRJDgrrT1p1TLiUH7` | `agente/siguiente-ciudad` | `investigacion/` | hecho (6 oct): recomienda Madrid (datos: Barcelona 9,5 · Madrid 8 · Valencia 5 · L'Hospitalet + Badalona 3,5 · Sant Cugat 1). Informes en [`investigacion/`](../investigacion/). Madrid confirmado por Pablo; el piloto de Madrid, en espera (primero Barcelona). Borrador de las dos solicitudes de transparencia a Madrid en [`investigacion/solicitud-transparencia-madrid.md`](../investigacion/solicitud-transparencia-madrid.md). Integrado en `main` (8 oct) |
| 6 | Textos legales | `session_0145ccAQynYUi5LEEFvuqGkW` | `agente/legal` | `legal/` | dormido |

## Cómo funciona

- **Despertar**: el director envía el encargo a la sesión (`send_message`) y le recuerda que añada `pablopiqueras85/decibhello`. El agente saca su rama de `main`, trabaja, hace push a su rama y termina con un resumen.
- **Memoria**: cada agente guarda su estado en `<su carpeta>/ESTADO.md` de su rama. Lo lee al despertar y lo actualiza y sube al terminar. El director se lo recuerda en cada encargo. Los agentes 1 y 5 tienen un borrador escrito por el director ([`web/ESTADO.md`](../web/ESTADO.md) e [`investigacion/ESTADO.md`](../investigacion/ESTADO.md)): lo revisan y completan al despertar.
- **Seguimiento**: los agentes no pueden escribir al director; el director lee su resultado en la sesión (`list_events`) y se lo resume a Pablo.
- **Integrar**: cuando Pablo da por bueno un trabajo, el director hace merge de la rama del agente a `main`. Sin pull requests, salvo que Pablo lo pida.
- Cada agente gasta uso del plan solo mientras trabaja. Dormido no gasta nada.
