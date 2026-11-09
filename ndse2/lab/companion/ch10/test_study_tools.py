"""Synthetic software tests only. Not participant data or study outcomes."""

import unittest, copy
from randomize import allocate
from score import analyze, kappa_quadratic


class SoftwareTests(unittest.TestCase):
    def fixture(self):
        keys = [
            dict(
                answer_id="test-a",
                participant_id="fixture-1",
                form="A",
                timepoint="baseline",
            ),
            dict(
                answer_id="test-b",
                participant_id="fixture-2",
                form="B",
                timepoint="day14",
            ),
        ]
        rows = []
        for aid, score in [("test-a", "0"), ("test-b", "2")]:
            for rater in ["unit-r1", "unit-r2"]:
                rows.append(
                    dict(
                        answer_id=aid,
                        rater_id=rater,
                        authority=score,
                        behavior=score,
                        causal=score,
                        negative_test=score,
                        change_impact=score,
                        unsafe_assumption="no",
                        evidence_excerpt="SYNTHETIC SOFTWARE TEST",
                    )
                )
        return rows, keys

    def test_empty_allocation(self):
        with self.assertRaises(ValueError):
            allocate([], 1)

    def test_blank_id(self):
        with self.assertRaises(ValueError):
            allocate([{"participant_id": " "}], 1)

    def test_duplicate_id(self):
        with self.assertRaises(ValueError):
            allocate([{"participant_id": "x"}] * 2, 1)

    def test_reproducible_allocation_and_balance(self):
        rows = [dict(participant_id=str(i), stratum=str(i % 2)) for i in range(12)]
        a, b = allocate(rows, 4)
        self.assertEqual((a, b), allocate(rows, 4))
        self.assertEqual(sum(r["condition"] == "expert_curated" for r in a), 6)
        self.assertTrue(
            all(r["baseline_form"] == "A" and r["delayed_form"] == "B" for r in a)
        )
        self.assertEqual(len(set(r["blind_code"] for r in b)), 12)

    def test_no_ratings(self):
        with self.assertRaisesRegex(ValueError, "NO_REAL_RATINGS"):
            analyze([], [])

    def test_descriptive_arithmetic(self):
        r, k = self.fixture()
        a = analyze(r, k)
        self.assertEqual(a["n_participants"], 2)
        self.assertEqual(
            a["mean_total_score_by_timepoint"], {"baseline": 0, "day14": 10}
        )
        self.assertEqual(a["weighted_kappa_by_dimension"]["authority"], 1)

    def test_undefined_kappa(self):
        self.assertIsNone(kappa_quadratic([1, 1], [1, 1]))

    def test_out_of_range(self):
        r, k = self.fixture()
        r[0]["causal"] = "3"
        with self.assertRaises(ValueError):
            analyze(r, k)

    def test_duplicate_rating(self):
        r, k = self.fixture()
        r.append(r[0].copy())
        with self.assertRaises(ValueError):
            analyze(r, k)

    def test_missing_rater(self):
        r, k = self.fixture()
        with self.assertRaises(ValueError):
            analyze(r[:-1], k)

    def test_wrong_key(self):
        r, k = self.fixture()
        k[0]["timepoint"] = "day7"
        with self.assertRaises(ValueError):
            analyze(r, k)

    def test_mixed_rater_pairs(self):
        r, k = self.fixture()
        r[-1]["rater_id"] = "third"
        with self.assertRaises(ValueError):
            analyze(r, k)

    def test_empty_evidence(self):
        r, k = self.fixture()
        r[0]["evidence_excerpt"] = ""
        with self.assertRaises(ValueError):
            analyze(r, k)

    def test_bad_flag(self):
        r, k = self.fixture()
        r[0]["unsafe_assumption"] = "maybe"
        with self.assertRaises(ValueError):
            analyze(r, k)


if __name__ == "__main__":
    unittest.main()
