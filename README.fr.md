# Agent Run History

## Nouveau : reçu du successeur de consolidation

**« Une opération reste rouge alors que son successeur a terminé le même travail. »** Lancez `python3 operation_successor.py demo --lang fr` ; pour vos opérations sauvegardées, utilisez `python3 operation_successor.py check --operations operations.json --lang fr`. Une opération échouée est **couverte** seulement si elle nomme `superseded_by`, si le successeur terminé la nomme dans `supersedes`, si leurs `bank_id` sont identiques et si le successeur couvre tous les `source_ids`. La seule chronologie reste indéterminée. C’est un format de reçu hors ligne, pas un analyseur automatique des diagnostics Hindsight.

**Projets voisins :** [Hindsight #5434](https://github.com/vectorize-io/hindsight/issues/5434) rapporte l’indicateur d’échec persistant ; [Hindsight](https://github.com/vectorize-io/hindsight) gère la consolidation. Ce vérificateur lit des preuves explicites et ne modifie pas Hindsight ; aucune affiliation n’est revendiquée.

## Nouveau : reçu de transfert

`python3 handoff_receipt.py handoff-demo --lang fr` montre un tour conservé et un transfert incertain ; la démonstration réussie sort avec le code 0. Avec vos captures : `python3 handoff_receipt.py check --events events.json --snapshot document.json --lang fr`. `events.json` contient des objets `{turn_id, operation_id, marker, phase, mode}` ; `phase` vaut `enqueued`, `accepted` ou `failed`, et `mode` vaut `append`, `replace` ou `unknown`. L’instantané Hindsight doit contenir `original_text`. L’outil ne relance jamais une écriture : un marqueur absent après `accepted` est manquant ; après `failed` ou `enqueued`, il est incertain.

**Rapports voisins :** [Hindsight #5286](https://github.com/vectorize-io/hindsight/issues/5286) et [#5251](https://github.com/vectorize-io/hindsight/issues/5251) motivent la conservation des tours et des preuves de transfert. Vous fournissez les événements ; cette version ne lit pas automatiquement les diagnostics Hindsight.

**Vérifiez qu’un document mémoire garde le résultat de chaque exécution de l’agent.**

[English](README.md) · [Français](README.fr.md) · [Español](README.es.md)

## Projets voisins

- [Hindsight](https://github.com/vectorize-io/hindsight) — Fournit l’API de documents utilisée en mode connecté.
- [Issue #4963](https://github.com/vectorize-io/hindsight/issues/4963) — Décrit un cas Pi où la seconde exécution semble remplacer la première.
- [agent-capsule](https://github.com/gbesse/agent-capsule) — Rejoue des traces d’outils ; ce contrôle porte sur les résultats conservés dans un document.

Ces liens décrivent des projets voisins, sans affiliation.

## Essayer

```sh
python3 run_history.py demo --lang fr
```

## Ce que cet outil vérifie

Lit `original_text` via la route documentée de Hindsight ou dans une réponse JSON enregistrée, puis contrôle des marqueurs explicites. Ne modifie jamais la banque.

## Utiliser avec vos données

```sh
python3 run_history.py check --base-url http://127.0.0.1:8888 --bank demo --document conversation:session-1 --expect OUTCOME:run-1 --expect OUTCOME:run-2 --lang fr
```

Ajoutez un marqueur `OUTCOME:<run-id>` unique à chaque résultat conservé, puis lancez `check` sur l’identifiant du document. Un marqueur absent renvoie 1. La route HTTP est testée avec un serveur local simulé.

## Périmètre et limites

L’outil ne crée pas les marqueurs, ne restaure pas les données écrasées et ne diagnostique pas l’adaptateur Pi. Hindsight réel n’a pas été démarré pour cet alpha ; vérifiez votre version.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

MIT · v0.1.0-alpha.1
