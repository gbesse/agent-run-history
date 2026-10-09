#!/usr/bin/env python3
"""Show when a failed memory operation has an explicitly completed successor."""

import argparse
import json
import sys
from pathlib import Path

WORDS = {
    "en": {"covered": "Failed operation covered by a completed successor", "unresolved": "Failed operation remains unresolved", "inconclusive": "Successor evidence is incomplete", "invalid": "Invalid operations"},
    "fr": {"covered": "Opération échouée couverte par un successeur terminé", "unresolved": "Opération échouée non résolue", "inconclusive": "Preuve du successeur incomplète", "invalid": "Opérations invalides"},
    "es": {"covered": "Operación fallida cubierta por un sucesor completado", "unresolved": "Operación fallida sin resolver", "inconclusive": "Evidencia del sucesor incompleta", "invalid": "Operaciones no válidas"},
}


def inspect(operations):
    if not isinstance(operations, list) or not operations:
        raise ValueError("nonempty array required")
    index = {}
    for row in operations:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"] or row["id"] in index:
            raise ValueError("unique operation IDs required")
        index[row["id"]] = row
    result = []
    for row in operations:
        if row.get("status") != "failed":
            continue
        successor = index.get(row.get("superseded_by"))
        if not successor:
            state = "inconclusive" if row.get("superseded_by") else "unresolved"
        else:
            source_ids = row.get("source_ids")
            next_ids = successor.get("source_ids")
            same_bank = isinstance(row.get("bank_id"), str) and row.get("bank_id") == successor.get("bank_id")
            explicit_link = successor.get("supersedes") == row["id"]
            same_sources = (isinstance(source_ids, list) and bool(source_ids)
                            and all(isinstance(x, str) and x for x in source_ids)
                            and isinstance(next_ids, list) and all(isinstance(x, str) and x for x in next_ids)
                            and set(source_ids).issubset(set(next_ids)))
            state = "covered" if all((same_bank, explicit_link, same_sources, successor.get("status") == "completed")) else "inconclusive"
        result.append({"id": row["id"], "successor_id": row.get("superseded_by"), "state": state})
    if not result:
        raise ValueError("failed operation required")
    return {"status": "unresolved" if any(r["state"] == "unresolved" for r in result) else "inconclusive" if any(r["state"] == "inconclusive" for r in result) else "covered", "operations": result}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("demo", "check"))
    parser.add_argument("--operations", type=Path)
    parser.add_argument("--lang", choices=WORDS, default="en")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            rows = [{"id": "A", "bank_id": "demo", "source_ids": ["memory-1"], "status": "failed", "superseded_by": "B"},
                    {"id": "B", "bank_id": "demo", "source_ids": ["memory-1", "memory-2"], "status": "completed", "supersedes": "A"}]
        else:
            if not args.operations:
                parser.error("check requires --operations")
            rows = json.loads(args.operations.read_text(encoding="utf-8"))
        report = inspect(rows)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(f"{WORDS[args.lang]['invalid']}: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False) if args.json else WORDS[args.lang][report["status"]])
    return 0 if report["status"] == "covered" else 2


if __name__ == "__main__":
    raise SystemExit(main())
