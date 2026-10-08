import { chromium } from "playwright";
import fs from "fs";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage();
await p.goto("file:///home/user/Ideas/piloto/visor.html");
await p.waitForTimeout(800);
const out = await p.evaluate(() => {
  const pick = n => PILOTO.find(x => x.direccion === n);
  const r = n => { const x = pick(n); const media = calcular(x.r, null); const dias = DIAS.map((_, k) => calcular(x.r, k));
    return { direccion: n, global: Math.round(media.exterior.global), franjas: Object.fromEntries(Object.entries(media.exterior.franjas).map(([k,v])=>[k,Math.round(v)])),
      interior: media.interior ? Math.round(media.interior.global) : null,
      percentil: percentilCiudad(media.exterior.global), sensor: media.sensor ? media.sensor.calle : null, obra: media.obra,
      mapa: media.exterior.mapa,
      dias: dias.map(d => ({ nota: d.exterior.nota.map(v => Math.round(v)), db: d.exterior.db.map(v => Math.round(v*10)/10), noche: Math.round(d.exterior.franjas.N), global: Math.round(d.exterior.global),
         interior: d.interior ? d.interior.nota.map(v=>Math.round(v)) : null })) }; };
  return ["Carrer de Tuset 20", "Carrer de Pomaret 20", "Gran Via de les Corts Catalanes 600"].map(r);
});
fs.writeFileSync("/home/user/Ideas/web/datos/extraccion.json", JSON.stringify(out));
console.log(JSON.stringify(out.map(o => ({d:o.direccion,g:o.global,f:o.franjas,i:o.interior,pc:o.percentil,s:o.sensor,obra:o.obra,mapa:o.mapa,noches:o.dias.map(x=>x.noche), lun:o.dias[0].nota, vie:o.dias[4].nota, dbvie:o.dias[4].db}))));
await b.close();
