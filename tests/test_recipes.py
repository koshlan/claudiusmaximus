import unittest

from espresso_calc import build_recipe
from espresso_calc.cli import run


class BuildRecipeTests(unittest.TestCase):
    def test_single_espresso(self):
        r = build_recipe("espresso", shots=1)
        self.assertEqual((r.beans_g, r.espresso_ml, r.milk_ml), (9, 30, 0))

    def test_double_cappuccino_is_one_to_two(self):
        r = build_recipe("cappuccino", shots=2, milk_type="whole")
        self.assertEqual((r.beans_g, r.espresso_ml, r.milk_ml), (18, 60, 120))

    def test_latte_fills_cup(self):
        r = build_recipe("latte", shots=2, milk_type="oat", cup_size="medium")
        self.assertEqual(r.espresso_ml + r.milk_ml, 360)

    def test_cortado_equal_milk(self):
        r = build_recipe("cortado", shots=2, milk_type="soy")
        self.assertEqual(r.milk_ml, r.espresso_ml)

    def test_americano_adds_water(self):
        r = build_recipe("americano", shots=2)
        self.assertEqual(r.hot_water_ml, 120)

    def test_milk_drink_requires_milk_type(self):
        with self.assertRaises(ValueError):
            build_recipe("latte", shots=2, cup_size="small")


class CliTests(unittest.TestCase):
    def test_interactive_flow_retries_bad_input(self):
        answers = iter(["latte", "triple", "double", "goat", "oat", "3"])
        text = run(ask=lambda _prompt: next(answers))
        self.assertIn("18 g", text)
        self.assertIn("60 ml of espresso", text)
        self.assertIn("420 ml of oat milk", text)


if __name__ == "__main__":
    unittest.main()
