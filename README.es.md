# Agent Run History

## Nuevo: recibo del sucesor de consolidación

**« Una operación sigue en rojo aunque su sucesora terminó el mismo trabajo. »** Ejecute `python3 operation_successor.py demo --lang es`; para operaciones guardadas use `python3 operation_successor.py check --operations operations.json --lang es`. Una operación fallida está **cubierta** solo si indica `superseded_by`, el sucesor completado la indica en `supersedes`, ambos tienen el mismo `bank_id` y el sucesor cubre todos los `source_ids`. La mera cronología es indeterminada. Este es un formato de recibo sin conexión, no un analizador automático de diagnósticos Hindsight.

**Proyectos relacionados:** [Hindsight #5434](https://github.com/vectorize-io/hindsight/issues/5434) informa del indicador de fallo persistente; [Hindsight](https://github.com/vectorize-io/hindsight) realiza la consolidación. El verificador lee pruebas explícitas y no modifica Hindsight ni afirma afiliación.

## Nuevo: recibo de traspaso

`python3 handoff_receipt.py handoff-demo --lang es` muestra un turno conservado y un traspaso incierto; la demostración correcta sale con código 0. Con capturas guardadas: `python3 handoff_receipt.py check --events events.json --snapshot document.json --lang es`. `events.json` contiene objetos `{turn_id, operation_id, marker, phase, mode}`; `phase` es `enqueued`, `accepted` o `failed`, y `mode` es `append`, `replace` o `unknown`. La instantánea del documento Hindsight debe contener `original_text`. El recibo nunca reintenta una escritura: un marcador ausente tras `accepted` falta; tras `failed` o `enqueued` queda incierto.

**Informes relacionados:** [Hindsight #5286](https://github.com/vectorize-io/hindsight/issues/5286) y [#5251](https://github.com/vectorize-io/hindsight/issues/5251) motivan conservar los turnos y las pruebas de traspaso. Usted proporciona los eventos; esta versión no analiza automáticamente los diagnósticos de Hindsight.

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
