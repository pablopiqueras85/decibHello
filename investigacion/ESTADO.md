Borrador del director (8 oct 2026); el agente lo revisa y completa al despertar.

# Agente 5: siguiente ciudad — estado

## Encargo

- Comparar qué ciudad tiene mejores datos abiertos para repetir el piloto de Barcelona: Madrid, Valencia y el área metropolitana (L'Hospitalet, Badalona, Sant Cugat).
- Carpeta `investigacion/`. Rama `agente/siguiente-ciudad`, sacada de `main`. Sesión `session_01FjeojmRJDgrrT1p1TLiUH7`.
- No toca `piloto/`. Las reglas del modelo son las de Barcelona.

## Hecho

- **Estudio completo** (6 oct) en [siguiente-ciudad.md](siguiente-ciudad.md): tabla fuente a fuente, bloqueos y cómo encajaría Madrid en el sistema de Barcelona.
- **Madrid frente a Valencia** con nota de datos de 0 a 10 y estimación de trabajo en [siguiente-ciudad-madrid-valencia.md](siguiente-ciudad-madrid-valencia.md). Notas: Barcelona 9,5 · Madrid 8 · Valencia 5 · L'Hospitalet + Badalona 3,5 · Sant Cugat 1.
- **Recomendación**: Madrid primero. Mapa de 2021 en dB exactos cada 5 m (con patios), censo de locales con horario y descargas sin captcha. Su hueco: no publica datos de sensores por hora.
- **Borrador de dos solicitudes de transparencia** a Madrid (datos por hora de las 31 estaciones; horarios de recogida y limpieza) en [solicitud-transparencia-madrid.md](solicitud-transparencia-madrid.md).
- **Notas de trabajo** con columnas, cifras y consultas: [Madrid](notas/madrid.md), [Valencia](notas/valencia.md) y [área metropolitana](notas/amb.md).
- **Integrado en `main`** el 8 oct 2026.

## Falta

- Piloto de Madrid (unas 3–4 semanas), cuando Pablo lo pida. Pasos: índice de portales leyendo el ráster, locales y horarios, pesos por día con los datos diarios, recalcular la suma por bares con las 31 estaciones, obras de Informo, quejas y pisos turísticos con el callejero.
- Aclarar a qué día se apunta la noche en los datos diarios de Madrid (va en la solicitud; si no, deducirlo con Nochevieja).
- Área metropolitana como ampliación de Barcelona, más adelante. Necesita descargas a mano (Catastro, ICGC; ver la sección 6 del estudio).
- Valencia, solo si contesta a una solicitud sobre locales y sensores.
- Revisar y completar este borrador.

## Decisiones de Pablo

- **Madrid es la siguiente ciudad** (6 oct 2026).
- **El piloto de Madrid espera**: primero se termina Barcelona (6 oct).
- Las solicitudes de transparencia a Madrid las envía Pablo (pendiente).

## Enlaces

- Estudio: [siguiente-ciudad.md](siguiente-ciudad.md) · Madrid frente a Valencia: [siguiente-ciudad-madrid-valencia.md](siguiente-ciudad-madrid-valencia.md)
- Solicitudes a Madrid: [solicitud-transparencia-madrid.md](solicitud-transparencia-madrid.md)
- Pendientes del proyecto: [docs/pendientes.md](../docs/pendientes.md) · Equipo y ramas: [docs/agentes.md](../docs/agentes.md)
- Votación de ciudades en la web: https://claude.ai/artifact/KrBrXRxafoU2cScYv55FjD (privado)
