#!/usr/bin/env python3
"""Check that all explicit run markers remain in one Hindsight document."""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

MESSAGES = {
    "en": ("Run history", "present", "missing", "No run markers supplied."),
    "fr": ("Historique des exécutions", "présent", "absent", "Aucun marqueur d'exécution fourni."),
    "es": ("Historial de ejecuciones", "presente", "ausente", "No se proporcionaron marcadores de ejecución."),
}


def document_text(data):
    if isinstance(data, str):
        return data
    if not isinstance(data, dict):
        raise ValueError("document must be an object or a string")
    for key in ("original_text", "text", "content"):
        if isinstance(data.get(key), str):
            return data[key]
    if isinstance(data.get("document"), dict):
        return document_text(data["document"])
    raise ValueError("document has no original_text, text or content")


def fetch_document(base_url, bank, document, timeout=10):
    path = "/v1/default/banks/{}/documents/{}".format(
        urllib.parse.quote(bank, safe=""), urllib.parse.quote(document, safe="")
    )
    url = base_url.rstrip("/") + path
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.load(response)


def check(text, markers):
    if not markers:
        raise ValueError("at least one marker is required")
    if len(markers) != len(set(markers)) or any(not marker for marker in markers):
        raise ValueError("markers must be nonempty and unique")
    return {"total": len(markers), "present": [m for m in markers if m in text],
            "missing": [m for m in markers if m not in text]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("demo", "check"))
    parser.add_argument("--snapshot", type=Path, help="saved Hindsight document JSON")
    parser.add_argument("--base-url", default="http://127.0.0.1:8888")
    parser.add_argument("--bank")
    parser.add_argument("--document")
    parser.add_argument("--expect", action="append", default=[], help="unique marker retained in each run")
    parser.add_argument("--lang", choices=MESSAGES, default="en")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            data = json.loads((Path(__file__).parent / "fixtures" / "second-run.json").read_text())
            markers = ["OUTCOME:run-1", "OUTCOME:run-2"]
        elif args.snapshot:
            data = json.loads(args.snapshot.read_text())
            markers = args.expect
        elif args.bank and args.document:
            data = fetch_document(args.base_url, args.bank, args.document)
            markers = args.expect
        else:
            parser.error("check requires --snapshot or --bank and --document")
        result = check(document_text(data), markers)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        title, good, bad, _ = MESSAGES[args.lang]
        print(title)
        for marker in markers:
            # A supplied marker can contain user data; print only its ordinal.
            status = good if marker in result["present"] else bad
            print(f"run {markers.index(marker) + 1}: {status}")
    return 1 if args.command == "check" and result["missing"] else 0


if __name__ == "__main__":
    sys.exit(main())
