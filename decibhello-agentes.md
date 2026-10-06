# DecibHello — Equipo de agentes

El director del proyecto es la sesión principal de Claude (la que habla con Pablo). Cada agente es una sesión aparte en claude.ai/code, con este repositorio, su propia rama y su encargo escrito en sus instrucciones. Están **dormidos**: solo empiezan cuando Pablo lo pide y el director les envía el mensaje. Ninguno toca `piloto/` (el modelo y el visor los mantiene el director).

| # | Agente | Sesión | Rama | Carpeta | Estado |
|---|---|---|---|---|---|
| 1 | Web y lista de espera | `session_01AKVCMzunJ9suXjcJRcHFEd` | `agente/web-lista-espera` | `web/` | hecho (6 oct): landing en https://claude.ai/artifact/KrBrXRxafoU2cScYv55FjD con vídeo, buscador de calles (usa `piloto/paquete/decibhello.js`), voto de ciudades y lista de espera. Pendiente de Pablo: guiones de los vídeos de plastilina, su vídeo con sonido y una foto del área metropolitana |
| 2 | Extensión de Chrome | `session_01VAn9UEcGXw6tfhhJ4Vu2Eg` | `agente/extension-chrome` | `extension/` | dormido |
| 3 | Sonómetro web | `session_01TP2VCShQMuQCnyVzeHegj7` | `agente/sonometro` | `sonometro/` | dormido |
| 4 | Entrevistas de validación | `session_015Fobjtmy4viNvwbz6ecU7i` | `agente/entrevistas` | `negocio/` | dormido |
| 5 | Siguiente ciudad | `session_01FjeojmRJDgrrT1p1TLiUH7` | `agente/siguiente-ciudad` | `investigacion/` | hecho (6 oct): recomienda Madrid (datos: Barcelona 9,5 · Madrid 8 · Valencia 5 · L'Hospitalet + Badalona 3,5 · Sant Cugat 1). Informes en `investigacion/` de su rama. Pendiente de Pablo: confirmar Madrid y la solicitud de transparencia de los datos por hora de los sensores de Madrid |
| 6 | Textos legales | `session_0145ccAQynYUi5LEEFvuqGkW` | `agente/legal` | `legal/` | dormido |

Cómo funciona:
- **Despertar**: el director envía el encargo a la sesión (`send_message`). El agente trabaja, hace push a su rama y termina con un resumen.
- **Seguimiento**: los agentes no pueden escribir al director; el director lee su resultado en la sesión (`list_events`) y se lo resume a Pablo.
- **Integrar**: cuando Pablo da por bueno un trabajo, el director lo trae a la rama principal del proyecto.
- Cada agente gasta uso del plan solo mientras trabaja. Dormido no gasta nada.
