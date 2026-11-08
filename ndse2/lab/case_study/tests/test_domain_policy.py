import unittest
from pathlib import Path
from approval_lab.domain import Transaction, ValidationError
from approval_lab.policy import Policy
from approval_lab.legacy import legacy_route

ROOT = Path(__file__).resolve().parents[1]


def tx(**overrides):
    base = {
        "transaction_id": "T-100",
        "amount_minor": 300000,
        "currency": "EUR",
        "department": "TREASURY",
        "risk": "LOW",
        "requester": "demo-user",
        "cross_border": False,
    }
    base.update(overrides)
    return Transaction(**base)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.v1 = Policy.from_file(ROOT / "policies/v1.json")
        self.v2 = Policy.from_file(ROOT / "policies/v2.json")

    def test_boundary_is_inclusive(self):
        self.assertEqual(
            "AUTO_APPROVAL_ELIGIBLE", self.v2.evaluate(tx(amount_minor=300000)).status
        )
        self.assertEqual(
            "REVIEW_REQUIRED", self.v2.evaluate(tx(amount_minor=300001)).status
        )

    def test_high_risk_never_auto_eligible(self):
        self.assertEqual(
            "HIGH_RISK", self.v1.evaluate(tx(risk="HIGH", amount_minor=1)).reason_code
        )

    def test_cross_border_never_auto_eligible(self):
        self.assertEqual(
            "CROSS_BORDER",
            self.v2.evaluate(tx(cross_border=True, amount_minor=1)).reason_code,
        )

    def test_unknown_department_fails_closed(self):
        self.assertEqual(
            "REVIEW_REQUIRED",
            self.v1.evaluate(tx(department="UNLISTED", amount_minor=1)).status,
        )

    def test_negative_and_zero_invalid(self):
        for n in (0, -2):
            with self.assertRaises(ValidationError):
                tx(amount_minor=n)

    def test_bool_not_valid_integer_money(self):
        with self.assertRaises(ValidationError):
            tx(amount_minor=True)

    def test_float_not_valid_money(self):
        with self.assertRaises(ValidationError):
            tx(amount_minor=5000.0)

    def test_unknown_risk_invalid(self):
        with self.assertRaises(ValidationError):
            tx(risk="MEDIUM")

    def test_non_eur_invalid(self):
        with self.assertRaises(ValidationError):
            tx(currency="USD")

    def test_late_intent_delta_changes_threshold(self):
        self.assertEqual(
            "AUTO_APPROVAL_ELIGIBLE", self.v1.evaluate(tx(amount_minor=400000)).status
        )
        self.assertEqual(
            "REVIEW_REQUIRED", self.v2.evaluate(tx(amount_minor=400000)).status
        )

    def test_never_over_threshold_monotonicity(self):
        for n in range(300001, 500001, 1777):
            self.assertEqual(
                "REVIEW_REQUIRED", self.v2.evaluate(tx(amount_minor=n)).status
            )

    def test_policy_requires_explicit_safe_cross_border_behavior(self):
        with self.assertRaises(ValidationError):
            Policy("vX", "EUR", {"OPS": 100}, "AUTO_APPROVAL_ELIGIBLE")

    def test_legacy_has_observable_bug_in_high_risk_route(self):
        self.assertEqual(
            "AUTO_APPROVAL_ELIGIBLE", legacy_route(tx(risk="HIGH", amount_minor=100))
        )
        self.assertEqual(
            "REVIEW_REQUIRED",
            self.v2.evaluate(tx(risk="HIGH", amount_minor=100)).status,
        )


if __name__ == "__main__":
    unittest.main()
