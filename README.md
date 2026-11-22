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
Registres « vous » et « couple » et variante sans financement : refusés par `gen.py` (non encore réalisés).

## Polices
Bodoni Moda et Inter, embarquées dans `fonts/` (licence SIL Open Font License) pour que le rendu ne dépende pas des polices installées.
