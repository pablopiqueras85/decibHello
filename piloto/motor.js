// DecibHello — motor común: modelo (copia de piloto/modelo.py), índice de Barcelona y buscador.
// Lo usan el visor (piloto/visor_plantilla.html, dentro de la página) y la web (piloto/paquete/decibhello.js).
// Espera una constante global DATOS (la escribe calcular_nota.py). No edites piloto/paquete/ a mano.
// MODELO:inicio — copia de piloto/modelo.py; si cambias uno, cambia el otro.
const FRANJA = Array.from({ length: 24 }, (_, h) => (h >= 7 && h < 19 ? "D" : h >= 19 && h < 23 ? "E" : "N"));
const HORAS = { D: [], E: [], N: [] };
FRANJA.forEach((f, h) => HORAS[f].push(h));
const PESOS = { D: 0.3, E: 0.2, N: 0.5 };
// Escala de cada franja: dB que dan 0 y 100 puntos (extremos reales de Barcelona). Lineal entre ambos.
const ESCALA = { D: [45, 75], E: [45, 75], N: [35, 70] };
const DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"];
const normalizarPesos = p => { const m = p.reduce((a, b) => a + b, 0) / p.length; return p.map(x => x / m); };
// Formas horarias y pesos por día medidos con los sensores municipales (sensores.py -> perfiles_sensores.json).
const PS = DATOS.perfiles;
const PERFIL_TRAFICO = PS.trafico.forma_horaria_db;
const PERFIL_OCIO = (() => { const f = PS.ocio.forma_horaria_db, hs = [23, 0, 1, 2, 3, 4, 5, 6], m = Math.max(...hs.map(h => f[h])), o = {}; hs.forEach(h => (o[h] = Math.round((f[h] - m) * 10) / 10)); return o; })();
const PESO_DIA_TRAFICO = { D: normalizarPesos(PS.trafico.pesos_dia.D), E: normalizarPesos(PS.trafico.pesos_dia.E), N: normalizarPesos(PS.trafico.pesos_dia.N) };
const PESO_DIA_OCIO_NOCHE = normalizarPesos(PS.ocio.pesos_dia.N);
const PESO_DIA_OCIO_TARDE = normalizarPesos(PS.ocio.pesos_dia.E);
const PESO_DIA_HORA_TRAFICO = PS.trafico.pesos_dia_hora || null;
const PESO_DIA_HORA_OCIO = PS.ocio.pesos_dia_hora || null;
const energia = db => Math.pow(10, db / 10);
const suma = a => a.reduce((x, y) => x + y, 0);

function perfilHorario(total, trafico, ocioNoche, dia) {
  const db = new Array(24).fill(0);
  for (const f of "DEN") {
    const horas = HORAS[f], n = horas.length;
    const eTotal = energia(total[f]);
    let traf = horas.map(() => 0), ocio = horas.map(() => 0);
    if (trafico) {
      const forma = horas.map(h => energia(PERFIL_TRAFICO[h]));
      const k = energia(trafico[f]) / (suma(forma) / n);
      traf = forma.map(x => x * k);
    }
    if (ocioNoche != null && f === "N") {
      const forma = horas.map(h => energia(PERFIL_OCIO[h]));
      const k = energia(ocioNoche) / (suma(forma) / n);
      ocio = forma.map(x => x * k);
    }
    let resto = Math.max(0, eTotal - (suma(traf) + suma(ocio)) / n);
    if (!trafico) {
      const forma = horas.map(h => energia(PERFIL_TRAFICO[h]));
      const k = eTotal / (suma(forma) / n);
      traf = forma.map(x => x * k);
      resto = 0;
    }
    const ajuste = eTotal / (horas.reduce((a, _, i) => a + traf[i] + ocio[i] + resto, 0) / n);
    const fTraf = dia != null ? PESO_DIA_TRAFICO[f][dia] : 1;
    const fOcio = dia != null ? PESO_DIA_OCIO_NOCHE[dia] : 1;
    const eT = suma(traf), eO = suma(ocio);
    const fResto = eT + eO ? (eT * fTraf + eO * fOcio) / (eT + eO) : fTraf;
    // El resto (sin fuente asignada) sigue la forma horaria de tráfico + ocio de la franja.
    const mediaBase = (eT + eO) / n;
    horas.forEach((h, i) => {
      const forma = mediaBase ? (traf[i] + ocio[i]) / mediaBase : 1;
      let ft = fTraf, fo = fOcio, fr = fResto;
      if (dia != null && PESO_DIA_HORA_TRAFICO) {
        ft = PESO_DIA_HORA_TRAFICO[dia][h]; fo = PESO_DIA_HORA_OCIO[dia][h];
        fr = traf[i] + ocio[i] ? (traf[i] * ft + ocio[i] * fo) / (traf[i] + ocio[i]) : ft;
      }
      db[h] = 10 * Math.log10((traf[i] * ft + ocio[i] * fo + resto * forma * fr) * ajuste);
    });
  }
  for (const [h1, h2] of [[18, 19], [22, 23]]) {
    const e1 = energia(db[h1]), e2 = energia(db[h2]);
    db[h1] = 10 * Math.log10((2 * e1 + e2) / 3);
    db[h2] = 10 * Math.log10((e1 + 2 * e2) / 3);
  }
  return db;
}
function notaDb(db, f) {
  const [cero, cien] = ESCALA[f];
  return Math.min(100, Math.max(0, (db - cero) / (cien - cero) * 100));
}
// Misma fórmula para todo: la nota de cada hora sale solo de su nivel en dB (medido o estimado).
function notasHorarias(db) {
  return db.map((v, h) => notaDb(v, FRANJA[h]));
}
function resumen(notas) {
  const franjas = {};
  for (const f of "DEN") franjas[f] = HORAS[f].reduce((a, h) => a + notas[h], 0) / HORAS[f].length;
  return { franjas, global: PESOS.D * franjas.D + PESOS.E * franjas.E + PESOS.N * franjas.N };
}
function perfilMedido(dbDias, dia) {
  if (dia != null) return dbDias[dia].slice();
  return Array.from({ length: 24 }, (_, h) => 10 * Math.log10(dbDias.reduce((a, d) => a + energia(d[h]), 0) / 7));
}
// Obra pública activa a menos de 25 m: +2 dB de 8 a 18 h, de lunes a viernes (validado con sensores, obras_validacion.md).
const OBRA_DB = 2.0;
function sumaObra(db, dia) {
  const extra = dia != null ? OBRA_DB : 10 * Math.log10((5 * Math.pow(10, OBRA_DB / 10) + 2) / 7);
  if (dia == null || dia < 5) for (let h = 8; h < 18; h++) db[h] += extra;
}
// Planta del piso. ESTIMACIÓN a partir de estudios de ruido en calles; aún sin medir en Barcelona (copia de modelo.py).
function correccionPlanta(planta, plantasEdificio = -1, anchoM = -1) {
  if (planta == null || planta === 1) return 0;
  if (planta === 0) return 1.0;
  const alto = plantasEdificio > 0 ? 3.0 * plantasEdificio + 1 : 20.0;
  const ancho = anchoM >= 3 ? anchoM : 20.0;
  const pendiente = 0.4 * (1 - Math.min(alto / ancho, 1));
  let extra = 0;
  if (planta === "atico") { planta = plantasEdificio > 1 ? plantasEdificio : 7; extra = -3.0; }
  const altura = 4 + 3.0 * (planta - 1);
  return -Math.min(8.0, pendiente * Math.max(0, altura - 4)) + extra;
}
function avisoPicos(anchoM, quejas, turisticos = 0) {
  const estrecha = anchoM >= 0 && anchoM < 12;
  // Pisos turísticos: llegadas y salidas a deshoras; 20 o más a menos de 100 m cuentan como foco.
  const turistico = turisticos >= 20;
  if ((estrecha && (quejas >= 1 || turistico)) || quejas >= 5 || (turistico && quejas >= 1)) return "alto";
  if (estrecha || quejas >= 1 || turistico) return "medio";
  return "bajo";
}
// MODELO:fin

// ---------- Vocabulario de calles (antes del índice, que lo usa) ----------
const TIPOS = { carrer: "carrer", calle: "carrer", c: "carrer", cl: "carrer", cr: "carrer", avinguda: "avinguda", avenida: "avinguda", av: "avinguda", avda: "avinguda", avgda: "avinguda",
  passeig: "passeig", paseo: "passeig", pg: "passeig", pso: "passeig", placa: "placa", plaza: "placa", pl: "placa", pza: "placa", ronda: "ronda", rda: "ronda",
  rambla: "rambla", rbla: "rambla", passatge: "passatge", pasaje: "passatge", ptge: "passatge", pje: "passatge", travessera: "travessera", travesera: "travessera", trav: "travessera",
  cami: "cami", camino: "cami", carretera: "carretera", ctra: "carretera", baixada: "baixada", bajada: "baixada", pujada: "pujada", subida: "pujada", via: "via", moll: "moll", muelle: "moll" };
const PARTICULAS = new Set(["de", "del", "d", "la", "les", "el", "els", "dels", "l", "i", "y", "las", "los", "en", "na"]);
const RUIDO_TEXTO = new Set(["barcelona", "bcn", "espana", "spain", "catalunya", "cataluna", "n", "no", "num", "numero", "nro", "s", "sn", "piso", "planta", "puerta", "pta", "bajo", "baixos", "atico", "principal", "pral", "esc", "escalera"]);

// ---------- Índice ----------
const IX = DATOS.indice;
const NC = IX.campos_rango.length;
const bandaDb = i => 37.5 + 5 * i;
const CALLES = IX.calles.map(([nombre, planos]) => {
  const rangos = [];
  for (let i = 0; i < planos.length; i += NC) {
    const r = {};
    IX.campos_rango.forEach((c, k) => (r[c] = planos[i + k]));
    r.lat = IX.origen.lat + r.lat_e5 / 1e5;
    r.lon = IX.origen.lon + r.lon_e5 / 1e5;
    rangos.push(r);
  }
  rangos.sort((a, b) => a.ini - b.ini);
  return { nombre, rangos, ...tokensCalle(nombre) };
});
const cacheCalc = new Map();
// Corrección proporcional por bares y bares musicales/discotecas (dB por log(1+n)), validada con sensores por distritos.
const CL = DATOS.coef_locales;
function correccionLocales(r) {
  const c = {};
  for (const f of ["D", "E", "N"]) c[f] = r.sensor >= 0 ? 0 : CL[f].bares * Math.log1p(r.solo_bares) + CL[f].musicales * Math.log1p(r.musicales);
  return c;
}
const fmtDb = x => x.toFixed(1).replace(".", ",");
const HOY = new Date().toLocaleDateString("sv-SE");  // AAAA-MM-DD en la hora local de quien mira
const obrasCerca = r => (r.obras >= 0 ? IX.grupos_obras[r.obras] : []).map(([o, d]) => ({ ...IX.obras[o], d }));
const obraEnCurso = o => o.estado !== "Aturada" && o.inicio <= HOY && HOY <= o.fin;
const obraSuma = r => obrasCerca(r).some(o => o.d <= IX.obras_radio_efecto && o.suma && obraEnCurso(o));
function calcular(r, dia = null, planta = null) {
  const clave = planta + "|" + r.tramo + "|" + r.patio + "|" + r.ocio + "|" + r.bares + "|" + r.quejas + "|" + r.turisticos + "|" + r.sensor + "|" + r.solo_bares + "|" + r.musicales + "|" + r.obras + "|" + r.noches + "|" + dia;
  if (cacheCalc.has(clave)) return cacheCalc.get(clave);
  const t = IX.tramos[r.tramo];
  const b = k => bandaDb(+t[IX.campos_tramo.indexOf(k)]);
  const sensor = r.sensor >= 0 ? DATOS.sensores[r.sensor] : null;
  const zb = correccionLocales(r);
  const dbExt = sensor ? perfilMedido(sensor.db, dia) : perfilHorario({ D: b("TOTAL_D") + zb.D, E: b("TOTAL_E") + zb.E, N: b("TOTAL_N") + zb.N }, { D: b("TRANSIT_D"), E: b("TRANSIT_E"), N: b("TRANSIT_N") }, b("OCI_N"), dia);
  // Planta del piso (estimación): mismo desplazamiento en todas las horas de la fachada a la calle.
  const dPlanta = correccionPlanta(planta, r.plantas, r.ancho_m);
  if (dPlanta) for (let h = 0; h < 24; h++) dbExt[h] += dPlanta;
  // Horarios de los locales de noche cercanos: más ruido las noches en que abren de madrugada (no si hay sensor).
  if (!sensor && r.noches >= 0 && dia != null) HORAS.N.forEach(h => (dbExt[h] += IX.ajustes_noche[r.noches][dia]));
  // Obra pública en curso a menos de 25 m: ruido extra temporal de día laborable (también si hay sensor: la medición es de 2023).
  const obra = obraSuma(r);
  const globalSinObra = obra ? resumen(notasHorarias(dbExt)).global : null;
  if (obra) sumaObra(dbExt, dia);
  const notasExt = notasHorarias(dbExt);
  const ext = { db: dbExt, nota: notasExt, ...resumen(notasExt), mapa: { D: IX.bandas[+t[0]], E: IX.bandas[+t[1]], N: IX.bandas[+t[2]] } };
  let int = null;
  if (r.patio >= 0) {
    const p = IX.tramos[r.patio];
    const dbInt = perfilHorario({ D: bandaDb(+p[0]), E: bandaDb(+p[1]), N: bandaDb(+p[2]) }, null, null, dia);
    const notasInt = notasHorarias(dbInt);
    int = { db: dbInt, nota: notasInt, ...resumen(notasInt), mapa: { D: IX.bandas[+p[0]], E: IX.bandas[+p[1]], N: IX.bandas[+p[2]] } };
  }
  const res = { exterior: ext, interior: int, trafico: IX.bandas[+t[5]], ocioMapa: IX.bandas[+t[6]], sensor, locales: zb, obra, globalSinObra, dPlanta,
    ajusteNoches: !sensor && r.noches >= 0 ? IX.ajustes_noche[r.noches] : null };
  cacheCalc.set(clave, res);
  return res;
}

// ---------- Búsqueda ----------
function normalizar(s) {
  return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/l·l/g, "ll").replace(/[º°ª]/g, " ").replace(/[^a-z0-9]+/g, " ").trim();
}
function tokensCalle(nombre) {
  const toks = normalizar(nombre).split(" ").filter(Boolean);
  let tipo = null;
  const nucleo = [];
  toks.forEach((t, i) => {
    if (i === 0 && TIPOS[t]) tipo = TIPOS[t];
    else if (!PARTICULAS.has(t)) nucleo.push(t);
  });
  return { tipo, nucleo, norm: toks.join(" ") };
}
function levenshtein(a, b, max) {
  if (Math.abs(a.length - b.length) > max) return max + 1;
  let prev = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    const cur = [i];
    let minFila = i;
    for (let j = 1; j <= b.length; j++) {
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      minFila = Math.min(minFila, cur[j]);
    }
    if (minFila > max) return max + 1;
    prev = cur;
  }
  return prev[b.length];
}
function parecido(q, t) {
  if (q === t) return 1;
  if (q.length >= 2 && t.startsWith(q)) return 0.8;
  if (q.length >= 4 && levenshtein(q, t, 1) <= 1) return 0.75;
  if (q.length >= 7 && levenshtein(q, t, 2) <= 2) return 0.6;
  return 0;
}
function analizarTexto(texto) {
  const toks = normalizar(texto).split(" ").filter(Boolean);
  let tipo = null, numero = null;
  const nucleo = [];
  let vistoTexto = false;
  for (const t of toks) {
    if (/^\d+$/.test(t)) {
      if (t.length === 5) continue; // código postal
      if (vistoTexto && numero === null && t.length <= 4) numero = +t;
      continue;
    }
    if (numero !== null) continue; // piso, puerta, ciudad después del número
    if (RUIDO_TEXTO.has(t)) continue;
    if (!vistoTexto && TIPOS[t] && tipo === null) { tipo = TIPOS[t]; continue; }
    vistoTexto = true;
    if (!PARTICULAS.has(t)) nucleo.push(t);
  }
  return { tipo, nucleo, numero };
}
function buscarCalles(consulta, max = 8) {
  if (!consulta.nucleo.length) return [];
  const res = [];
  for (let i = 0; i < CALLES.length; i++) {
    const c = CALLES[i];
    if (!c.nucleo.length) continue;
    let suma = 0, ok = true;
    const usados = new Set();
    for (const q of consulta.nucleo) {
      let mejor = 0, mejorJ = -1;
      c.nucleo.forEach((t, j) => { if (usados.has(j)) return; const p = parecido(q, t); if (p > mejor) { mejor = p; mejorJ = j; } });
      if (!mejor) { ok = false; break; }
      usados.add(mejorJ); suma += mejor;
    }
    if (!ok) continue;
    const cobertura = consulta.nucleo.length / Math.max(consulta.nucleo.length, c.nucleo.length);
    let puntos = (suma / consulta.nucleo.length) * (0.6 + 0.4 * cobertura);
    if (consulta.tipo && consulta.tipo === c.tipo) puntos += 0.15;
    puntos += 0.01 * Math.log10(1 + c.rangos.length); // a igualdad, primero las calles largas (las más buscadas)
    res.push({ i, puntos });
  }
  res.sort((a, b) => b.puntos - a.puntos || CALLES[a.i].nombre.length - CALLES[b.i].nombre.length);
  return res.slice(0, max);
}
function rangoDeNumero(calle, numero) {
  const rs = calle.rangos;
  if (numero == null) return { r: rs[Math.floor(rs.length / 2)], exacto: false, sinNumero: true };
  const mismos = rs.filter(r => r.ini % 2 === numero % 2);
  const base = mismos.length ? mismos : rs;
  const exacto = base.find(r => r.ini <= numero && numero <= r.fin);
  if (exacto) return { r: exacto, exacto: true };
  const cerca = base.reduce((m, r) => { const d = Math.min(Math.abs(numero - r.ini), Math.abs(numero - r.fin)); return !m || d < m.d ? { r, d } : m; }, null);
  return { r: cerca.r, exacto: cerca.d <= 4 }; // a 4 números o menos de un portal del mismo lado: se da por encontrado
}
function distanciaM(lat1, lon1, lat2, lon2) {
  const x = (lon2 - lon1) * Math.cos(((lat1 + lat2) / 2) * Math.PI / 180) * 111320;
  const y = (lat2 - lat1) * 110540;
  return Math.hypot(x, y);
}
function rangoMasCercano(lat, lon) {
  let mejor = null;
  CALLES.forEach((c, ci) => c.rangos.forEach(r => {
    const d = distanciaM(lat, lon, r.lat, r.lon);
    if (!mejor || d < mejor.d) mejor = { ci, r, d };
  }));
  return mejor;
}
const PORTALES = ["idealista", "fotocasa", "habitaclia", "pisos.com", "milanuncios", "yaencontre", "badi.com", "spotahome", "housinganywhere", "uniplaces", "enalquiler", "tucasa"];
function interpretar(texto) {
  const t = texto.trim();
  if (!t) return { tipo: "vacio" };
  const tl = t.toLowerCase();
  if (/maps\.app\.goo\.gl|goo\.gl\/maps/.test(tl)) return { tipo: "aviso", html: "<strong>Ese es un enlace corto de Google Maps.</strong> Ábrelo, espera a que cargue el mapa y copia la dirección completa de la barra del navegador (empieza por google.com/maps/…). También puedes escribir la calle y el número." };
  const portal = PORTALES.find(p => tl.includes(p + ".") || tl.includes(p + "/") || tl.includes(p));
  if (/^https?:\/\//.test(tl) && portal) return { tipo: "aviso", html: `<strong>Los anuncios no traen la dirección en el enlace.</strong> El enlace de ${portal} solo identifica el anuncio, y muchos portales ocultan el número exacto. Escribe la calle que aparece en el anuncio (y el número si lo pone), o abre su mapa en Google Maps y pega ese enlace aquí.` };
  let m = t.match(/!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)/) || t.match(/[?&](?:q|query|ll|destination|center)=(-?\d+\.\d+)(?:,|%2C)\s*(-?\d+\.\d+)/i);
  let precision = "punto";
  if (!m) { m = t.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/); precision = "centro"; }
  if (!m) { m = t.match(/^\s*(-?\d{1,2}\.\d{3,})\s*[,;\s]\s*(-?\d{1,3}\.\d{3,})\s*$/); precision = "punto"; }
  if (m) return { tipo: "coordenadas", lat: +m[1], lon: +m[2], precision };
  const lugar = t.match(/google\.[a-z.]+\/maps\/(?:place|search)\/([^/@?]+)/i);
  if (lugar) return { tipo: "texto", texto: decodeURIComponent(lugar[1].replace(/\+/g, " ")) };
  if (/^https?:\/\//.test(tl)) return { tipo: "aviso", html: "<strong>No reconozco ese enlace.</strong> Pega un enlace de Google Maps o escribe la calle y el número." };
  return { tipo: "texto", texto: t };
}

// Posición en la ciudad: % de portales de Barcelona con una nota global exterior menor.
function percentilCiudad(g) {
  const pc = DATOS.percentiles_ciudad;
  let k = 0;
  while (k < 100 && pc[k + 1] <= g) k++;
  return Math.max(1, Math.min(99, k));
}
function nivelTexto(s) {
  if (s < 20) return "Muy tranquilo";
  if (s < 40) return "Tranquilo";
  if (s < 60) return "Moderado";
  if (s < 80) return "Ruidoso";
  return "Muy ruidoso";
}

// ---------- API pública (la usan el visor y la web) ----------
// Resultado listo para pintar, sin depender de la página que lo use.
function informe(ci, r, dia = null, planta = null) {
  const res = calcular(r, dia, planta);
  const ext = res.exterior;
  const noches = DIAS.map((_, d) => calcular(r, d, planta).exterior.franjas.N);
  return {
    calle: CALLES[ci].nombre, portales: [r.ini, r.fin], barrio: IX.barrios[r.barrio] || "",
    nota: ext.global, etiqueta: nivelTexto(ext.global), percentil: percentilCiudad(calcular(r, null).exterior.global),
    franjas: ext.franjas, horas: ext.nota, db: ext.db, noches,
    interior: res.interior ? { nota: res.interior.global, franjas: res.interior.franjas, horas: res.interior.nota, db: res.interior.db } : null,
    sensor: res.sensor ? res.sensor.calle : null, obraSuma: res.obra, obras: obrasCerca(r),
    picos: avisoPicos(r.ancho_m, r.quejas_recogida, r.turisticos), mapa: ext.mapa,
    plantasEdificio: r.plantas, planta, correccionPlantaDb: res.dPlanta,
  };
}
// Texto, dirección o enlace de Google Maps -> { tipo: "ok" | "varias" | "aviso" | "sin_resultado" | "fuera" | "vacio", ... }
function buscar(texto) {
  const intento = interpretar(texto);
  if (intento.tipo === "vacio" || intento.tipo === "aviso") return intento;
  if (intento.tipo === "coordenadas") {
    const { lat, lon } = intento;
    if (lat < 41.31 || lat > 41.47 || lon < 2.05 || lon > 2.24) return { tipo: "fuera" };
    const m = rangoMasCercano(lat, lon);
    return { tipo: "ok", ci: m.ci, r: m.r, numero: m.r.ini, exacto: true, distancia: Math.round(m.d), precision: intento.precision, informe: informe(m.ci, m.r) };
  }
  const a = analizarTexto(intento.texto);
  const res = buscarCalles(a);
  if (!res.length) return { tipo: "sin_resultado" };
  const claro = res.length === 1 || res[0].puntos - res[1].puntos >= 0.1;
  if (!claro) return { tipo: "varias", opciones: res.map(x => ({ ci: x.i, calle: CALLES[x.i].nombre, numero: a.numero })) };
  return elegirCalle(res[0].i, a.numero);
}
// Una calle concreta (por ejemplo, tras elegir entre "varias") y su número.
function elegirCalle(ci, numero) {
  const { r, exacto, sinNumero } = rangoDeNumero(CALLES[ci], numero);
  return { tipo: "ok", ci, r, numero: sinNumero ? null : numero, exacto: exacto && !sinNumero, sinNumero: !!sinNumero, informe: informe(ci, r) };
}
const DecibHello = { buscar, elegirCalle, informe, calcular, correccionPlanta, sugerencias: (texto, max = 8) => buscarCalles(analizarTexto(texto), max).map(x => ({ ci: x.i, calle: CALLES[x.i].nombre })),
  CALLES, DIAS, HORAS, FRANJA, nivelTexto, percentilCiudad, fechaDatos: { obras: IX.obras_fecha } };
