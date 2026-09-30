# Agent Run History

**Compruebe que un documento de memoria conserva el resultado de cada ejecución del agente.**

[English](README.md) · [Français](README.fr.md) · [Español](README.es.md)

## Proyectos relacionados

- [Hindsight](https://github.com/vectorize-io/hindsight) — Proporciona la API de documentos usada en modo conectado.
- [Issue #4963](https://github.com/vectorize-io/hindsight/issues/4963) — Describe un caso de Pi donde la segunda ejecución parece reemplazar la primera.
- [agent-capsule](https://github.com/gbesse/agent-capsule) — Reproduce trazas de herramientas; esta comprobación se centra en los resultados conservados en un documento.

Estos enlaces describen proyectos relacionados, sin afiliación.

## Probar

```sh
python3 run_history.py demo --lang es
```

## Qué comprueba esta herramienta

Lee `original_text` mediante la ruta documentada de Hindsight o desde una respuesta JSON guardada y comprueba marcadores explícitos. Nunca modifica el banco.

## Usar con sus datos

```sh
python3 run_history.py check --base-url http://127.0.0.1:8888 --bank demo --document conversation:session-1 --expect OUTCOME:run-1 --expect OUTCOME:run-2 --lang es
```

Añada un marcador único `OUTCOME:<run-id>` a cada resultado guardado y ejecute `check` sobre el identificador del documento. Un marcador ausente devuelve 1. La ruta HTTP se prueba con un servidor local simulado.

## Alcance y límites

No crea marcadores, no recupera datos sobrescritos ni diagnostica el adaptador Pi. Hindsight real no se inició para esta versión alfa; compruebe su versión.

## Pruebas

```sh
python3 -m unittest discover -s tests -v
```

MIT · v0.1.0-alpha.1
