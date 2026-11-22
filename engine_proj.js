// Moteur « projection » : exécute telles quelles les fonctions computeAssuranceVie et computeScpi
// de simulateurs/projection.html (source de vérité). Paramètres en JSON sur l'entrée standard.
const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const a = html.indexOf("const PS_RATE");
const b = html.indexOf("// Même effort d'épargne (versement initial + mensuel) que l'assurance vie");
if (a < 0 || b < 0) { console.error("EXTRACTION_IMPOSSIBLE: structure de projection.html modifiée"); process.exit(2); }
eval(html.slice(a, b) + "\nglobalThis.__p={computeScpi,computeAssuranceVie};");
const q = JSON.parse(fs.readFileSync(0, "utf8"));
const av = v => __p.computeAssuranceVie(Object.assign({frais:0,fraisActifs:false,fraisEntree:0,fraisEntreeActifs:false}, v));
console.log(JSON.stringify({ av: av(q.av), per: av(q.per), scpi: __p.computeScpi(q.scpi) }));
