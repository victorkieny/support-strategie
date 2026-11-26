# Support « Stratégie patrimoniale » — générateur

Dépôt **privé** : code uniquement, jamais de données client (dossier `clients/` ignoré par git).

## Utilisation
    python3 gen.py chemin/client.json --out dossier_sortie [--version AAAA-MM-JJ]

- Entrées : un JSON par client (modèle : `spec/client_exemple.json`).
- Calculs : exécutés par le JavaScript des simulateurs de Victor, tel quel, depuis le dépôt `victorkieny/site-internet`
  (`une-pierre-deux-coups.html`, `projection.html`) — cloné automatiquement si absent. Le modèle n'assemble que les résultats.
- Contrôles : entrées avant génération, PDF après (pages, mots interdits, autofinancement).
- Test de référence : `python3 tests/test_exemple.py`.

## Dépendances
Python 3, Node 22, Playwright (Chromium via `/usr/bin/google-chrome`), poppler (`pdfinfo`, `pdftotext`), git.

## Limites connues
Registres « vous » et « couple » : refusés par `gen.py` (non encore réalisés).
Variante sans financement (`financement.retenu = false`) : réalisée, 7 pages (page 6 supprimée, pieds « x/7 »), aucun levier ni mot de financement ; 2 leviers (versement initial, mensuel) + l'impôt si PER ; 2 ou 3 enveloppes ; page « mise en place » avec une seule flèche vers la SCPI en direct. `gen.py` échoue si un mot de financement subsiste dans le PDF (objectif du client à reformuler). Exemples : `spec/client_sans_financement_exemple.json` (avec PER) et `spec/client_sans_financement_sans_per_exemple.json`, test : `tests/test_sans_financement.py`.
Variante sans PER (PER initial et mensuel à 0) : réalisée, 3 enveloppes, `leviers.tmi` et `leviers.impot_annee` facultatifs, `financement.logement = "heberge"` pour un client hébergé (attestation d'hébergement à la place du bail). Exemple : `spec/client_sans_per_exemple.json`, test : `tests/test_sans_per.py`. Page 4 (« effort réel ») : sans PER et avec peu de SCPI en direct au départ, elle perd son message (écart de quelques euros) : à arbitrer par Victor.
Page 4 (effort réel) : avec au moins une SCPI (en direct ou financée), graphique dans le temps (1er mois, 5, 10, 15 ans) ; PER seul, cascade du 1er mois sans « de plus en plus » (`spec/client_per_seul_exemple.json`) ; ni PER ni SCPI, la page n'existe pas (6 pages de base + financement + effort réel, pieds « x/N » recalculés ; `spec/client_av_seule_exemple.json`). Limite connue : un client sans SCPI voit encore « SCPI en direct » à 0 € sur les pages 2 et 3, la frise et les hypothèses, à traiter.

## Polices
Bodoni Moda et Inter, embarquées dans `fonts/` (licence SIL Open Font License) pour que le rendu ne dépende pas des polices installées.

## Page 1 : situation initiale
`situation.composition` (obligatoire) : patrimoine actuel du client tel que relevé, un poste par ligne `{libelle, montant}` (1 à 8, dans l'ordre d'affichage, par exemple Livret A, LDD, PEA). `situation.origine` (obligatoire) : d'où vient l'épargne à investir, poste par poste (libellés identiques à la composition ; total = `situation.investir`). La page affiche la barre de composition avec, sous chaque poste, son nom et son montant (ni pourcentage ni précision de disponibilité), puis dans le levier « Versement initial » la provenance des fonds. `gen.py` refuse un dossier sans ces deux blocs : ils se demandent, ils ne se déduisent pas.
