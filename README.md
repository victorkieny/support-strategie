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
Variante sans PER (PER initial et mensuel à 0) : réalisée, 3 enveloppes, `leviers.tmi` et `leviers.impot_annee` facultatifs, `financement.logement = "heberge"` pour un client hébergé (attestation d'hébergement à la place du bail). Exemple : `spec/client_sans_per_exemple.json`, test : `tests/test_sans_per.py`. Page 4 (« effort réel ») : sans PER et avec peu de SCPI en direct au départ, elle perd son message (écart de quelques euros) : à arbitrer par Victor.

## Polices
Bodoni Moda et Inter, embarquées dans `fonts/` (licence SIL Open Font License) pour que le rendu ne dépende pas des polices installées.
