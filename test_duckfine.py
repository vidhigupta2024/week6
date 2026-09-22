import unittest

try:
    from duckfine import DuckFine
except ModuleNotFoundError:
    from du import DuckFine


class TestDuckFine(unittest.TestCase):
    def test_initializes_member_id_and_total_owed(self):
        fine = DuckFine("member-42")

        self.assertEqual(fine.member_id, "member-42")
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_rejects_negative_days_late(self):
        fine = DuckFine("member-42")

        with self.assertRaisesRegex(ValueError, "days_late must not be negative"):
            fine.charge(-1)

    def test_charge_has_no_fee_within_the_grace_period(self):
        fine = DuckFine("member-42")

        result = fine.charge(2)

        self.assertEqual(result, 0.0)
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_applies_standard_daily_fee_after_grace_period(self):
        fine = DuckFine("member-42")

        result = fine.charge(4)

        self.assertEqual(result, 1.0)
        self.assertEqual(fine.total_owed, 1.0)

    def test_charge_applies_deluxe_fee_and_caps_it_at_maximum(self):
        fine = DuckFine("member-42")

        result = fine.charge(20, deluxe=True)

        self.assertEqual(result, 5.0)
        self.assertEqual(fine.total_owed, 5.0)


if __name__ == "__main__":
    unittest.main()
