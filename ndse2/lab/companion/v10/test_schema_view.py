import copy, json, sys, tempfile, unittest
from pathlib import Path
from schema_view import encode_view, decode_view

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1] / "case_study"
sys.path.insert(0, str(CASE))
from approval_lab.policy import Policy
from approval_lab.domain import Transaction
from approval_lab.service import ApprovalService


class SchemaViewTests(unittest.TestCase):
    def test_decisions_preserved(self):
        for rev in ("v1", "v2"):
            original = json.loads((CASE / f"policies/{rev}.json").read_text())
            translated = decode_view(encode_view(original))
            self.assertEqual(original, translated)
            a = Policy(**original)
            b = Policy(**translated)
            for amount in (299999, 300000, 300001, 400000, 500000, 500001):
                for risk, cross in (("LOW", False), ("HIGH", False), ("LOW", True)):
                    tx = Transaction(
                        "T-test", amount, "EUR", "TREASURY", risk, "demo", cross
                    )
                    self.assertEqual(a.evaluate(tx), b.evaluate(tx))

    def test_replay_unchanged_across_view_migration(self):
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / "demo.sqlite"
            tx = Transaction("T-old", 400000, "EUR", "TREASURY", "LOW", "demo")
            a = ApprovalService(db, Policy.from_file(CASE / "policies/v1.json"))
            first = a.evaluate(tx, "key-old")
            a.close()
            v2 = json.loads((CASE / "policies/v2.json").read_text())
            b = ApprovalService(db, Policy(**decode_view(encode_view(v2))))
            try:
                self.assertEqual(first, b.evaluate(tx, "key-old"))
                self.assertEqual(1, b.stored_decisions())
            finally:
                b.close()

    def test_invalid_views_fail(self):
        policy = json.loads((CASE / "policies/v2.json").read_text())
        for mutate in (
            lambda v: v["rules"].append(copy.deepcopy(v["rules"][0])),
            lambda v: v["rules"][0].update(limit_minor=3000.0),
            lambda v: v["rules"][0].update(currency="USD"),
            lambda v: v.update(unknown=True),
        ):
            v = encode_view(policy)
            mutate(v)
            with self.assertRaises(ValueError):
                decode_view(v)


if __name__ == "__main__":
    unittest.main()
