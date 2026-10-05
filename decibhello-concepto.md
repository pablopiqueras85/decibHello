# DecibHello — Documento de concepto

Estado: borrador inicial. Ciudad de partida: **Barcelona**. Puntuación: **0–100**. Los campos `[...]` están por decidir. Las cifras de mercado y de competencia son hipótesis a validar, no datos contrastados.

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

1. **Puntuación de ruido DecibHello** de 0 a 100 (ver sección 4), separada en día, tarde y noche.
2. **Origen del ruido**: tráfico, ocio nocturno, obras, aeropuerto/ferrocarril, colegios, comercios.
3. **Patrón temporal**: laborable frente a fin de semana, verano frente a invierno.
4. **Comparativa**: frente a la media de la ciudad y a barrios alternativos.
5. **Nivel de confianza**: de qué datos sale cada cifra y cuán recientes son.

Diferencial buscado: traducir datos técnicos (dB) a un lenguaje cotidiano ("equivale a una conversación normal", "como un restaurante concurrido").

## 4. Escala de puntuación (0–100)

Convención: **0 = muy tranquilo, 100 = muy ruidoso**. La nota funciona como un medidor de ruido: cuanto más alta, más ruido.

| Rango | Etiqueta | Lectura para el usuario |
|---|---|---|
| 0–15 | Muy tranquilo | Se duerme con la ventana abierta |
| 16–30 | Tranquilo | Ruido puntual, poco molesto |
| 31–50 | Moderado | Tráfico o actividad notable en algunas franjas |
| 51–70 | Ruidoso | Molesto a menudo; conviene buen aislamiento |
| 71–100 | Muy ruidoso | Ruido intenso y frecuente, también de noche |

Cómo se calcula (propuesta a validar):
- Se calcula una nota por franja (día 7–19 h, tarde 19–23 h, noche 23–7 h) y una nota global ponderada.
- La noche pesa más que el día, porque es la franja que más afecta al descanso.
- Referencia para calibrar: las guías de ruido ambiental de la OMS (2018) recomiendan para tráfico rodado menos de 53 dB Lden y menos de 45 dB Lnight. Por encima de esos niveles la nota debería superar 50.
- Además de los dB, la nota sube por los focos intermitentes (bares, terrazas, obras), que molestan más de lo que indica una media anual.
- Cada informe muestra el nivel de confianza de la nota (alto, medio o bajo) según los datos disponibles en esa calle.

## 5. Público objetivo

| Segmento | Necesidad | Disposición a pagar |
|---|---|---|
| Inquilinos jóvenes y teletrabajadores | Dormir y trabajar en casa sin ruido | Media, uso puntual |
| Compradores de vivienda | Evitar un error de mucho dinero | Alta |
| Familias con niños pequeños | Descanso y entorno tranquilo | Media-alta |
| Personas que buscan animación (ocio, bares) | Lo contrario: barrio vivo | Baja-media |
| Inmobiliarias y portales | Diferenciar anuncios, reducir devoluciones | Alta (B2B) |
| Personas que se mudan a otra ciudad | No conocen la zona | Media |

Foco inicial: inquilinos y compradores en Barcelona. Merecen atención especial quienes llegan de fuera (otras ciudades o países) y no conocen la ciudad, porque es donde más se nota no saber cómo suena una calle.

## 6. Funcionalidades

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

## 7. Fuentes de datos

- Mapas estratégicos de ruido oficiales (directiva europea END) y mapas municipales.
- Datos abiertos de tráfico, aeropuertos y ferrocarril.
- OpenStreetMap: tipo de vía, locales de ocio, colegios, hospitales, obras.
- Licencias de terrazas y locales de ocio de los ayuntamientos.
- Quejas y denuncias por ruido, si hay datos abiertos.
- Mediciones propias o colaborativas.

Riesgos: cobertura desigual entre ciudades, datos desactualizados, mapas oficiales con media anual (no reflejan picos nocturnos).

### Barcelona

Investigación detallada en [decibhello-fuentes-datos-barcelona.md](decibhello-fuentes-datos-barcelona.md). Resumen:

- **Base de la nota**: mapa estratégico de ruido municipal (el último publicado por tramo de calle es de 2017; el de 2022 solo está como rejilla ráster), con día, tarde y noche y fuentes separadas (tráfico, ferrocarril, industria, ocio). Open Data BCN, licencia CC BY 4.0.
- **Ruido real**: red municipal de 176 sensores activos (Sentilo), con datos minuto a minuto desde 2024 en Open Data BCN.
- **Focos intermitentes**: censo de locales en planta baja, pisos turísticos, obras, quejas IRIS y OpenStreetMap.
- **Secundarias en la ciudad**: aeropuerto de El Prat y ferrocarril (SICA).

Factores propios de Barcelona que la nota debe recoger:
- Ocio nocturno y terrazas, muy concentrados en algunos barrios.
- Fiestas mayores de barrio (Gràcia, Sants...), La Mercè y Sant Joan: picos de pocos días al año. Mejor mostrarlos como aviso que meterlos en la nota.
- Turismo y pisos turísticos (maletas, entradas y salidas a deshoras).
- Supermanzanas (superilles) y calles pacificadas, que reducen el tráfico en su interior.
- Estacionalidad: el verano, con ventanas abiertas y más terrazas, cambia mucho la experiencia.

Zonas para el piloto (hipótesis, sin datos aún): contrastar barrios presumiblemente ruidosos (Ciutat Vella, Gràcia, Poble-sec, ejes del Eixample) con otros presumiblemente tranquilos (zonas altas de Sarrià-Sant Gervasi, Horta-Guinardó) para comprobar que la nota distingue bien.

## 8. Modelo de negocio (hipótesis)

- **Freemium para el usuario**: puntuación básica gratis; informe completo por unidad o suscripción corta.
- **B2B**: licencia a portales e inmobiliarias para incluir la puntuación en sus anuncios.
- **Afiliación**: servicios de aislamiento acústico, ventanas, mudanzas.
- A explorar: acuerdos con ayuntamientos y asociaciones vecinales.

## 9. Competencia y alternativas

- Mapas de ruido oficiales de ayuntamientos: gratis pero poco accesibles.
- Plataformas internacionales de ruido por dirección: `[investigar]`.
- Portales inmobiliarios con filtros de "zona tranquila": normalmente subjetivos.
- Visitar el piso a distintas horas: es la alternativa real y es gratis, pero cuesta tiempo.

Ventaja a construir: cobertura local buena, lenguaje claro, integración con el momento de decisión (el anuncio).

## 10. Riesgos y preguntas abiertas

- ¿Se puede estimar el ruido de una calle concreta con la precisión que espera el usuario?
- Responsabilidad legal si la puntuación se percibe como una garantía. Hay que dejar claro que es una estimación.
- Presión de propietarios e inmobiliarias contra puntuaciones bajas.
- Privacidad en las mediciones colaborativas.
- Disposición real a pagar: validar antes de construir.

## 11. Validación inicial

1. 10–15 entrevistas con personas que se han mudado en el último año.
2. Landing con lista de espera y una promesa concreta.
3. Prototipo manual para 20 direcciones de Barcelona, repartidas entre barrios ruidosos y tranquilos, y comprobar si el informe sirve.
4. Contrastar la nota calculada con mediciones propias (sonómetro o app) en 5–10 de esas direcciones, de día y de noche.
5. Medir si pagarían por el informe completo.

## 12. Hoja de ruta tentativa

| Fase | Objetivo | Resultado |
|---|---|---|
| 0 | Validar problema | Entrevistas + landing |
| 1 | Datos de Barcelona | Informe manual de 20 direcciones con nota 0–100 |
| 2 | MVP web | Búsqueda por dirección en Barcelona con puntuación |
| 3 | Primeros ingresos y área metropolitana | Pago por informe; L'Hospitalet, Badalona... |
| 3b | Segunda ciudad | `[Madrid / Valencia / ...]` |
| 4 | B2B | Piloto con portal o inmobiliaria |

## 13. Decisiones pendientes

- ~~Ciudad de partida~~: Barcelona (decidido).
- ~~Escala de puntuación~~: 0–100, 100 = muy ruidoso (decidido). Pendiente: pesos exactos por franja.
- Idiomas del producto: `[castellano / catalán / inglés]`.
- Nombre y marca: confirmar que DecibHello está libre (dominio y marca).
- Quién construye qué: `[...]`
