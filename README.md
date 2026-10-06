# Agent Run History

## New: handoff receipt

`python3 handoff_receipt.py handoff-demo --lang en` shows one retained turn and one uncertain handoff; a successful demonstration exits 0. For saved evidence run `python3 handoff_receipt.py check --events events.json --snapshot document.json --lang en`. `events.json` is an array of `{turn_id, operation_id, marker, phase, mode}` where `phase` is `enqueued`, `accepted` or `failed` and `mode` is `append`, `replace` or `unknown`. The Hindsight document snapshot must contain `original_text`. The receipt never retries a write: an absent marker after `accepted` is missing; after `failed` or `enqueued` it is uncertain.

**Related reports:** [Hindsight #5286](https://github.com/vectorize-io/hindsight/issues/5286) and [#5251](https://github.com/vectorize-io/hindsight/issues/5251) motivate preserving turn and handoff evidence. You must provide the events; this version does not parse Hindsight diagnostics automatically.

**Check that a memory document still contains the outcomes of every agent run.**

[English](README.md) · [Français](README.fr.md) · [Español](README.es.md)

## Related projects

- [Hindsight](https://github.com/vectorize-io/hindsight) — Provides the document API used by the live mode.
- [Issue #4963](https://github.com/vectorize-io/hindsight/issues/4963) — Reports a Pi adapter case where a second run appears to replace the first.
- [agent-capsule](https://github.com/gbesse/agent-capsule) — Replays tool traces; this checker focuses on outcome retention in one memory document.

Links describe technical neighbors, not an affiliation.

## Try it

```sh
python3 run_history.py demo --lang en
```

## What this checks

Reads `original_text` from Hindsight’s documented document GET route or a saved JSON response, then checks explicit run markers. It never edits the bank.

## Use with your data

```sh
python3 run_history.py check --base-url http://127.0.0.1:8888 --bank demo --document conversation:session-1 --expect OUTCOME:run-1 --expect OUTCOME:run-2 --lang en
```

Add a unique `OUTCOME:<run-id>` marker to each retained outcome, then run `check` on the document ID. A missing marker exits 1. Tests cover the HTTP route through a local mock.

## Scope and limits

The tool does not create run markers, reconstruct overwritten data, or diagnose the Pi adapter. Live Hindsight itself was not started for this alpha; verify against your version.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

MIT · v0.1.0-alpha.1
