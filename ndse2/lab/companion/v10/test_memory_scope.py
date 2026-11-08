import copy, hashlib, json, unittest
from pathlib import Path
from memory_scope import check_threshold_card

CASE = Path(__file__).resolve().parent.parents[1] / "case_study"


def card(rev, state="CURRENT"):
    p = CASE / f"policies/{rev}.json"
    data = json.loads(p.read_text())
    return {
        "policy_version": data["policy_version"],
        "department": "TREASURY",
        "ceiling_minor": data["departments"]["TREASURY"],
        "source_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "owner": "illustrative policy steward",
        "state": state,
    }, p


class MemoryTests(unittest.TestCase):
    def test_stale_current_label_cannot_override_scope(self):
        c, p = card("v1")
        self.assertEqual(
            "HOLD_STALE_FOR_NEW",
            check_threshold_card(c, p, "approval-eur-v2", "new_decision"),
        )

    def test_refresh_and_preserve_history(self):
        old, p1 = card("v1", "SUPERSEDED")
        new, p2 = card("v2")
        self.assertEqual(
            "HISTORICAL_SOURCE_MATCH_NOT_AUTHORIZATION",
            check_threshold_card(old, p1, "approval-eur-v2", "historical_explanation"),
        )
        self.assertEqual(
            "CURRENT_SOURCE_MATCH_NOT_AUTHORIZATION",
            check_threshold_card(new, p2, "approval-eur-v2", "new_decision"),
        )
        self.assertEqual(500000, old["ceiling_minor"])

    def test_forged_value_and_missing_provenance(self):
        c, p = card("v2")
        c["ceiling_minor"] = 500000
        self.assertEqual(
            "HOLD_UNSUPPORTED_VALUE",
            check_threshold_card(c, p, "approval-eur-v2", "new_decision"),
        )
        c, p = card("v2")
        del c["owner"]
        self.assertEqual(
            "HOLD_MISSING_PROVENANCE",
            check_threshold_card(c, p, "approval-eur-v2", "new_decision"),
        )

    def test_unresolved_or_changed_source(self):
        c, p = card("v2")
        c["state"] = "DISPUTED"
        self.assertEqual(
            "HOLD_UNRESOLVED_STATE",
            check_threshold_card(c, p, "approval-eur-v2", "new_decision"),
        )
        c, p = card("v2")
        c["source_sha256"] = "bad"
        self.assertEqual(
            "HOLD_SOURCE_CHANGED",
            check_threshold_card(c, p, "approval-eur-v2", "new_decision"),
        )


if __name__ == "__main__":
    unittest.main()
