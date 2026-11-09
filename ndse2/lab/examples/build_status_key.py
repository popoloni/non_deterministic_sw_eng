"""Build the compact bilingual reader key from the full typed state registry."""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "series/STATE_REGISTRY.json"
SELECTED = (
    "approval.decision",
    "intent.gate.structure",
    "intent.gate.authority",
    "intent.gate.acceptance",
    "candidate.oracle",
    "candidate.oracle.acceptance",
    "candidate.governance",
)


def build():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    by_name = {family["namespace"]: family for family in registry["families"]}
    rows = []
    for namespace in SELECTED:
        family = by_name[namespace]
        rows.append(
            {
                "namespace": namespace,
                "kind": "executable_or_declared_status",
                "entity": family["entity"],
                "values": [value["value"] for value in family["values"]],
                "producer": family["transition_or_computation_owner"],
                "permitted_next_action": family["permitted_next_decision"],
                "source": family["source"],
            }
        )
    alias = next(
        item
        for item in registry["prose_aliases_requiring_context"]
        if item["old"] == "READY_FOR_PUBLICATION_REVIEW"
    )
    rows.append(
        {
            "namespace": "publication.paper_example",
            "kind": "prose_alias_not_runtime_enum",
            "entity": alias["entity"],
            "values": [alias["old"]],
            "producer": alias["producer"],
            "permitted_next_action": alias["permitted_next_decision"],
            "source": {"en": alias["EN_locator"], "it": alias["ITA_locator"]},
        }
    )
    result = {
        "schema_version": "ndse-reader-status-key/1.0",
        "source": "series/STATE_REGISTRY.json",
        "source_sha256": hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
        "row_count": len(rows),
        "rows": rows,
        "rule": {
            "en": "A label is interpreted with its entity and producer. Review readiness, authority and acceptance are separate decisions.",
            "it": "Ogni valore si interpreta insieme all'entità e a chi lo produce. Disponibilità alla revisione, autorità e accettazione sono decisioni separate.",
        },
    }
    (ROOT / "series/READER_STATUS_KEY.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for language, suffix in (("en", "EN"), ("it", "ITA")):
        title, headers = (
            (
                "Reader status key",
                ["Entity / check", "Value", "Producer", "Permitted next action"],
            )
            if language == "en"
            else (
                "Guida agli stati per il lettore",
                [
                    "Entità / controllo",
                    "Valore",
                    "Responsabile",
                    "Decisione successiva consentita",
                ],
            )
        )
        text = [
            f"# {title}",
            "",
            result["rule"][language],
            "",
            "| " + " | ".join(headers) + " |",
            "|---|---|---|---|",
        ]
        for row in rows:
            text.append(
                "| "
                + " | ".join(
                    [
                        row["entity"][language],
                        ", ".join(f"`{value}`" for value in row["values"]),
                        row["producer"][language],
                        row["permitted_next_action"][language],
                    ]
                )
                + " |"
            )
        text += [
            "",
            "`READY_FOR_PUBLICATION_REVIEW`: "
            + (
                "paper publication example, outside the executable enums."
                if language == "en"
                else "esempio di pubblicazione su carta, esterno ai valori enumerati eseguibili."
            ),
            "",
            ("Source" if language == "en" else "Fonte")
            + ": `STATE_REGISTRY.json`; `python lab/examples/build_status_key.py`.",
            "",
        ]
        (ROOT / f"series/READER_STATUS_KEY_{suffix}.md").write_text(
            "\n".join(text), encoding="utf-8"
        )
    return {
        "status": "PASS",
        "rows": len(rows),
        "registry_families": len(registry["families"]),
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
