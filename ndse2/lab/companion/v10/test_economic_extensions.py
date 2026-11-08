from decimal import Decimal
import unittest
from economic_extensions import break_even_minutes, net_optional_cost, local_period_cost


class EconomicsTests(unittest.TestCase):
    def test_indifference_and_sensitivity(self):
        self.assertEqual(Decimal(3), break_even_minutes(3, 60))
        self.assertEqual(Decimal(6), break_even_minutes(3, 30))
        self.assertEqual(Decimal(0), net_optional_cost(3, 3, 60))
        self.assertGreater(net_optional_cost(3, 2, 60), 0)
        self.assertLess(net_optional_cost(3, 4, 60), 0)

    def test_invalid_inputs(self):
        for x in (-1, "NaN", True):
            with self.assertRaises(ValueError):
                break_even_minutes(x, 60)
        with self.assertRaises(ValueError):
            break_even_minutes(3, 0)


class LocalCostTests(unittest.TestCase):
    def test_units_and_allocation(self):
        r = local_period_cost(
            active_watts=100,
            active_hours=2,
            idle_watts=10,
            idle_hours=8,
            price_per_kwh="0.5",
            allocated_hardware_cost=2,
            support_cost=1,
            accepted_changes=2,
        )
        self.assertEqual(Decimal("0.28"), r["kwh"])
        self.assertEqual(Decimal("3.14"), r["total_allocated_cost"])
        self.assertEqual(Decimal("1.57"), r["cost_per_accepted_change"])

    def test_zero_accepted_is_undefined(self):
        r = local_period_cost(
            active_watts=0,
            active_hours=0,
            idle_watts=0,
            idle_hours=0,
            price_per_kwh=0,
            allocated_hardware_cost=2,
            support_cost=0,
            accepted_changes=0,
        )
        self.assertIsNone(r["cost_per_accepted_change"])


if __name__ == "__main__":
    unittest.main()
