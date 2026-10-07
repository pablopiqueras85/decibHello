// Comprueba que el visor (JavaScript) da las mismas notas que calcular_nota.py (Python) en las direcciones del piloto:
// nota global, nota de cada una de las 7 noches y aviso de picos nocturnos. Termina con código 1 si hay diferencias.
// Uso (después de `python3 piloto/calcular_nota.py`): cd piloto/pruebas && npm install && node paridad.mjs
import { chromium } from "playwright";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const piloto = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const navegador = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }).catch(() => chromium.launch());
const p = await navegador.newPage();
const errores = [];
p.on("pageerror", e => errores.push(e.message));
await p.goto("file://" + path.join(piloto, "visor.html"));
await p.waitForTimeout(600);

const lineas = fs.readFileSync(path.join(piloto, "resultados.csv"), "utf8").trim().split(/\r?\n/);
const cab = lineas[0].split(",");
const filas = lineas.slice(1).map(l => { const v = l.split(","); return Object.fromEntries(cab.map((c, i) => [c, v[i]])); });
const dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"];

const js = await p.evaluate(() => PILOTO.map(x => ({
  d: x.direccion,
  g: Math.round(calcular(x.r, null).exterior.global),
  n: DIAS.map((_, k) => Math.round(calcular(x.r, k).exterior.franjas.N)),
  picos: avisoPicos(x.r.ancho_m, x.r.quejas_recogida, x.r.turisticos),
})));
let dif = 0;
for (const x of js) {
  const r = filas.find(f => f.direccion === x.d);
  if (+r.nota_global !== x.g) { dif++; console.log("global", x.d, r.nota_global, x.g); }
  dias.forEach((d, k) => { if (+r["noche_" + d] !== x.n[k]) { dif++; console.log("noche", x.d, d, r["noche_" + d], x.n[k]); } });
  if (r.picos_nocturnos !== x.picos) { dif++; console.log("picos", x.d, r.picos_nocturnos, x.picos); }
}
console.log(`paridad Python/JS: ${dif} diferencias en ${js.length * 9} valores`);

// El paquete para otras páginas (piloto/paquete/decibhello.js) debe dar lo mismo que el visor.
const q = await navegador.newPage();
q.on("pageerror", e => errores.push("paquete: " + e.message));
await q.addScriptTag({ path: path.join(piloto, "paquete", "decibhello.js") });
await q.waitForFunction(() => window.DecibHello);
const paquete = await q.evaluate(dirs => dirs.map(d => {
  const r = DecibHello.buscar(d);
  return r.tipo === "ok" ? [d, Math.round(r.informe.nota), r.informe.noches.map(Math.round)] : [d, r.tipo];
}), js.map(x => x.d));
let difPaquete = 0;
for (const [d, nota, noches] of paquete) {
  const x = js.find(y => y.d === d);
  if (nota !== x.g || JSON.stringify(noches) !== JSON.stringify(x.n)) { difPaquete++; console.log("paquete", d, nota, x.g); }
}
const extra = await q.evaluate(() => [DecibHello.buscar("https://www.google.com/maps/@41.3953,2.1500,17z").tipo, DecibHello.buscar("https://www.idealista.com/inmueble/123/").tipo, DecibHello.buscar("Carrer Xqzwkt 5").tipo, DecibHello.buscar("40.4168,-3.7038").tipo]);
if (extra.join() !== "ok,aviso,sin_resultado,fuera") { difPaquete++; console.log("paquete, casos especiales:", extra); }
// Corrección por planta: la misma en JavaScript que en Python (tabla escrita por calcular_nota.py).
const tabla = JSON.parse(fs.readFileSync(path.join(piloto, "pruebas", "planta_python.json"), "utf8"));
const js_planta = await q.evaluate(t => t.map(([p, pe, an]) => DecibHello.correccionPlanta(p, pe, an)), tabla.casos);
tabla.casos.forEach((c, i) => { if (Math.abs(js_planta[i] - tabla.db[i]) > 1e-9) { difPaquete++; console.log("planta", c, tabla.db[i], js_planta[i]); } });
const js_margen = await q.evaluate(t => t.map(([m, f]) => DecibHello.margenPuntos(m, f)), tabla.casos_margen);
tabla.casos_margen.forEach((c, i) => { if (Math.abs(js_margen[i] - tabla.margen[i]) > 1e-9) { difPaquete++; console.log("margen", c, tabla.margen[i], js_margen[i]); } });
const js_esq = await q.evaluate(([a, b]) => DecibHello.combinarEsquina(a, b), tabla.esquina);
if (JSON.stringify(js_esq) !== JSON.stringify(tabla.esquina[2])) { difPaquete++; console.log("esquina", js_esq, tabla.esquina[2]); }
console.log(`paquete decibhello.js: ${difPaquete} diferencias (incluye ${tabla.casos.length} casos de planta, ${tabla.casos_margen.length} de margen y la esquina)`);
dif += difPaquete;
if (errores.length) console.log("errores de la página:", errores);
await navegador.close();
process.exit(dif || errores.length ? 1 : 0);
