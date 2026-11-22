// Moteur « financement » : exécute telles quelles les fonctions du simulateur de Victor
// (simulateurs/une-pierre-deux-coups.html). Aucune réécriture : le fichier HTML fait foi.
// Usage : node engine_fin.js <chemin_html>   (paramètres en JSON sur l'entrée standard)
const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const a = html.indexOf("function calculerMensualiteCreditMois");
const b = html.indexOf("// Données et hypothèses");
const c = html.indexOf("function calculerEffetLevierCreditSeul");
const e = html.indexOf("// Lignes affichées quand");
if ([a, b, c, e].some(i => i < 0)) { console.error("EXTRACTION_IMPOSSIBLE: structure du simulateur modifiée"); process.exit(2); }
const code = html.slice(a, html.lastIndexOf("// ----", b)) + "\n" + html.slice(c, e);
eval(code + "\nglobalThis.__f={simulerUnePierreDeuxCoups,calculerEffetLevier,calculerMensualiteCreditMois};");
const p = Object.assign({ versementInitial: 0, versementMensuelProgramme: 0, arreterVersementsAutofinancement: false,
                          isolerLevierCredit: true, horizonAnnees: 30 }, JSON.parse(fs.readFileSync(0, "utf8")));
const res = __f.simulerUnePierreDeuxCoups(p);
const l = __f.calculerEffetLevier(res, p);
const r1 = res.annees[0], rl = res.annees[l.anneeLimite - 1];
const delta = l.patrimoineAvecFinancement - l.patrimoineSansFinancement;
console.log(JSON.stringify({
  mensualite: r1.mensualite,
  mensualite_pret: __f.calculerMensualiteCreditMois(p.montantEmprunte, p.tauxInteretPct, p.dureeCredit * 12),
  loyer_mois1: r1.revenuBrutCreditMensuel, effort_m1: r1.effortSansComptant, effort_fin: rl.effortSansComptant,
  annee_autofinancement: res.anneeAutofinancement, annee_limite: l.anneeLimite,
  effort_total: l.partReelle, avec: l.patrimoineAvecFinancement, capital_sans: l.capitalContrefactuel,
  loyers_sans: l.loyersCumulesNets, sans: l.patrimoineSansFinancement, levier: delta,
  annees: res.annees.map(r => ({annee: r.annee, valeur: r.valeurPartsCredit, crd: r.capitalRestantDu, loyer: r.revenuBrutCredit, loyer_mois: r.revenuBrutCreditMensuel, en_cours: r.creditEnCours})),
  levier_pct: l.patrimoineSansFinancement > 0 ? (l.patrimoineAvecFinancement / l.patrimoineSansFinancement - 1) * 100 : 0
}));
