import copy, json, unittest
from pathlib import Path
from decimal import Decimal
from measurement import aggregate, active_effort


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.events = json.loads(
            Path(__file__).with_name("measurement_events.json").read_text()
        )

    def test_original_arithmetic(self):
        result = aggregate(self.events)
        self.assertEqual(result["human"]["person_minutes"], Decimal(680))
        self.assertEqual(result["assisted"]["person_minutes"], Decimal(780))
        self.assertEqual(result["human"]["minutes_per_accepted"], Decimal(85))
        self.assertEqual(result["assisted"]["minutes_per_accepted"], Decimal(780) / 9)
        self.assertEqual(result["assisted"]["expansion"], "HOLD")

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            aggregate(self.events + [self.events[0]])

    def test_unit_rejected(self):
        records = copy.deepcopy(self.events)
        records[2]["unit"] = "tokens"
        with self.assertRaises(ValueError):
            aggregate(records)

    def test_parallel_actors(self):
        self.assertEqual(
            active_effort(
                [
                    {"actor": "A", "start": 0, "end": 10},
                    {"actor": "B", "start": 0, "end": 10},
                ]
            ),
            (20, 10),
        )

    def test_same_actor_overlap_rejected(self):
        with self.assertRaises(ValueError):
            active_effort(
                [
                    {"actor": "A", "start": 0, "end": 10},
                    {"actor": "A", "start": 5, "end": 12},
                ]
            )


if __name__ == "__main__":
    unittest.main()
