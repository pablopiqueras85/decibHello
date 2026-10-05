# DecibHello — Documento de concepto

Estado: borrador inicial. Los campos `[...]` están por decidir. Las cifras de mercado y de competencia son hipótesis a validar, no datos contrastados.

## 1. Resumen

DecibHello es una plataforma que permite comprobar el nivel de ruido y de bullicio de un piso antes de alquilarlo o comprarlo: el barrio, la calle y los alrededores inmediatos, a distintas horas del día y de la semana.

Frase corta: "Visita el piso, pero también escucha el barrio antes de firmar."

## 2. Problema

- Los anuncios muestran metros, precio y fotos, pero casi nunca el ruido.
- Una visita dura 20 minutos, normalmente de día y entre semana. No refleja el viernes a las 2:00, el camión de la basura, la terraza de abajo o el colegio de al lado.
- El ruido se descubre después de mudarse, cuando ya hay contrato o hipoteca. Salir cuesta dinero (penalización, fianza, gastos de compraventa).
- Los mapas oficiales de ruido existen, pero son difíciles de encontrar, están fragmentados por municipio y son poco legibles para un usuario normal.
- Impacto: sueño, estrés, teletrabajo, convivencia con niños, valor de reventa.

## 3. Propuesta de valor

Para cada dirección, un informe claro con:

1. **Puntuación de ruido** (por ejemplo 0–100 o A–E) separada en día, tarde y noche.
2. **Origen del ruido**: tráfico, ocio nocturno, obras, aeropuerto/ferrocarril, colegios, comercios.
3. **Patrón temporal**: laborable frente a fin de semana, verano frente a invierno.
4. **Comparativa**: frente a la media de la ciudad y a barrios alternativos.
5. **Nivel de confianza**: de qué datos sale cada cifra y cuán recientes son.

Diferencial buscado: traducir datos técnicos (dB) a un lenguaje cotidiano ("equivale a una conversación normal", "como un restaurante concurrido").

## 4. Público objetivo

| Segmento | Necesidad | Disposición a pagar |
|---|---|---|
| Inquilinos jóvenes y teletrabajadores | Dormir y trabajar en casa sin ruido | Media, uso puntual |
| Compradores de vivienda | Evitar un error de mucho dinero | Alta |
| Familias con niños pequeños | Descanso y entorno tranquilo | Media-alta |
| Personas que buscan animación (ocio, bares) | Lo contrario: barrio vivo | Baja-media |
| Inmobiliarias y portales | Diferenciar anuncios, reducir devoluciones | Alta (B2B) |
| Personas que se mudan a otra ciudad | No conocen la zona | Media |

Foco inicial propuesto: inquilinos y compradores en `[ciudad]`.

## 5. Funcionalidades

**MVP**
- Búsqueda por dirección o por enlace de un anuncio.
- Informe con puntuación y desglose por franja horaria.
- Mapa de calor del ruido alrededor del punto.
- Lista de focos cercanos (bares, colegios, vías principales).

**Siguientes fases**
- Mediciones colaborativas con el móvil (micrófono) y validación.
- Valoraciones y comentarios de vecinos.
- Comparador de varios pisos o barrios.
- Alertas de nuevos anuncios que cumplan un umbral de ruido.
- Extensión de navegador que muestre la puntuación en los portales.
- API para inmobiliarias y portales.

## 6. Fuentes de datos (a investigar)

- Mapas estratégicos de ruido oficiales (directiva europea END) y mapas municipales.
- Datos abiertos de tráfico, aeropuertos y ferrocarril.
- OpenStreetMap: tipo de vía, locales de ocio, colegios, hospitales, obras.
- Licencias de terrazas y locales de ocio de los ayuntamientos.
- Quejas y denuncias por ruido, si hay datos abiertos.
- Mediciones propias o colaborativas.

Riesgos: cobertura desigual entre ciudades, datos desactualizados, mapas oficiales con media anual (no reflejan picos nocturnos).

## 7. Modelo de negocio (hipótesis)

- **Freemium para el usuario**: puntuación básica gratis; informe completo por unidad o suscripción corta.
- **B2B**: licencia a portales e inmobiliarias para incluir la puntuación en sus anuncios.
- **Afiliación**: servicios de aislamiento acústico, ventanas, mudanzas.
- A explorar: acuerdos con ayuntamientos y asociaciones vecinales.

## 8. Competencia y alternativas

- Mapas de ruido oficiales de ayuntamientos: gratis pero poco accesibles.
- Plataformas internacionales de ruido por dirección: `[investigar]`.
- Portales inmobiliarios con filtros de "zona tranquila": normalmente subjetivos.
- Visitar el piso a distintas horas: es la alternativa real y es gratis, pero cuesta tiempo.

Ventaja a construir: cobertura local buena, lenguaje claro, integración con el momento de decisión (el anuncio).

## 9. Riesgos y preguntas abiertas

- ¿Se puede estimar el ruido de una calle concreta con la precisión que espera el usuario?
- Responsabilidad legal si la puntuación se percibe como una garantía. Hay que dejar claro que es una estimación.
- Presión de propietarios e inmobiliarias contra puntuaciones bajas.
- Privacidad en las mediciones colaborativas.
- Disposición real a pagar: validar antes de construir.

## 10. Validación inicial

1. 10–15 entrevistas con personas que se han mudado en el último año.
2. Landing con lista de espera y una promesa concreta.
3. Prototipo manual para 20 direcciones en una ciudad y comprobar si el informe sirve.
4. Medir si pagarían por el informe completo.

## 11. Hoja de ruta tentativa

| Fase | Objetivo | Resultado |
|---|---|---|
| 0 | Validar problema | Entrevistas + landing |
| 1 | Datos de una ciudad | Informe manual de 20 direcciones |
| 2 | MVP web | Búsqueda por dirección con puntuación |
| 3 | Segunda ciudad y primeros ingresos | Pago por informe |
| 4 | B2B | Piloto con portal o inmobiliaria |

## 12. Decisiones pendientes

- Ciudad o país de partida: `[...]`
- Escala de puntuación: `[0–100 / A–E]`
- Nombre y marca: confirmar que DecibHello está libre (dominio y marca).
- Quién construye qué: `[...]`
