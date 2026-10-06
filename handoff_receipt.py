#!/usr/bin/env python3
"""Compare emitted agent turns with the durable memory document."""

import argparse
import json
import sys
from pathlib import Path

from run_history import document_text

TEXT = {
    "en": ("Memory handoff receipt", "present", "missing", "uncertain"),
    "fr": ("Reçu de remise en mémoire", "présent", "absent", "incertain"),
    "es": ("Recibo de entrega a memoria", "presente", "ausente", "incierto"),
}


def audit(events, document):
    if not isinstance(events, list) or not events:
        raise ValueError("events must be a nonempty array")
    seen = set()
    rows = []
    for event in events:
        identifier = event["turn_id"]
        marker = event["marker"]
        operation = event["operation_id"]
        if not all(isinstance(x, str) and x for x in (identifier, marker, operation)):
            raise ValueError("turn_id, marker and operation_id must be nonempty strings")
        if identifier in seen:
            raise ValueError("duplicate turn_id")
        seen.add(identifier)
        phase = event["phase"]
        if phase not in ("enqueued", "accepted", "failed"):
            raise ValueError("unsupported phase")
        mode = event.get("mode", "unknown")
        if mode not in ("append", "replace", "unknown"):
            raise ValueError("unsupported mode")
        state = "present" if marker in document else "missing" if phase == "accepted" else "uncertain"
        rows.append({"turn_id": identifier, "operation_id": operation, "mode": mode,
                     "phase": phase, "state": state})
    return {"ok": all(row["state"] == "present" for row in rows), "turns": rows,
            "modes": {mode: sum(row["mode"] == mode for row in rows)
                      for mode in ("append", "replace", "unknown")}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=("handoff-demo", "check"))
    ap.add_argument("--events", type=Path)
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--lang", choices=TEXT, default="en")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.command == "handoff-demo":
            events = [{"turn_id": "turn-1", "operation_id": "op-1", "marker": "OUTCOME:1",
                       "phase": "accepted", "mode": "replace"},
                      {"turn_id": "turn-2", "operation_id": "op-2", "marker": "OUTCOME:2",
                       "phase": "failed", "mode": "unknown"}]
            document = "OUTCOME:1"
        else:
            if not args.events or not args.snapshot:
                ap.error("check requires --events and --snapshot")
            events = json.loads(args.events.read_text())
            document = document_text(json.loads(args.snapshot.read_text()))
        result = audit(events, document)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        title, present, missing, uncertain = TEXT[args.lang]
        words = {"present": present, "missing": missing, "uncertain": uncertain}
        print(title)
        for index, row in enumerate(result["turns"], 1):
            print(f"{index}: {words[row['state']]} ({row['mode']})")
    return 0 if (not result["ok"] if args.command == "handoff-demo" else result["ok"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
