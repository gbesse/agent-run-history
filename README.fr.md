# Agent Run History

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
