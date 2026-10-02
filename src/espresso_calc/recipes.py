"""Drink definitions and the math that turns choices into a recipe."""

from dataclasses import dataclass
from typing import Optional

# Grams of ground coffee per espresso shot.
DOSE_PER_SHOT_G = 9

# Liquid espresso yield per shot, in ml, by extraction style.
SHOT_VOLUME_ML = {
    "ristretto": 15,
    "normal": 30,
    "lungo": 60,
}

# Total cup volumes (ml) offered for latte-style drinks.
CUP_SIZES_ML = {
    "small": 240,
    "medium": 360,
    "large": 480,
}

MILK_TYPES = ("whole", "2%", "skim", "oat", "almond", "soy")

MILK_NOTES = {
    "whole": "Whole milk gives the creamiest, most stable microfoam.",
    "2%": "2% milk foams well but is slightly less rich than whole.",
    "skim": "Skim milk makes stiff, airy foam; it can taste thin in larger drinks.",
    "oat": "Use a 'barista' oat milk for silky foam; avoid overheating (max ~60 C).",
    "almond": "Almond milk foams weakly; use a barista blend and steam gently.",
    "soy": "Soy foams well but can curdle if the milk is too hot or espresso very acidic.",
}


@dataclass(frozen=True)
class Drink:
    name: str
    description: str
    style: str  # key into SHOT_VOLUME_ML
    uses_milk: bool
    # How milk volume is derived. One of: None, "dollop", "equal", "ratio", "fill_cup".
    milk_rule: Optional[str] = None
    milk_ratio: float = 0.0  # used when milk_rule == "ratio" (milk = espresso * ratio)
    foam: str = ""  # foam guidance for the milk
    hot_water_ml_per_shot: int = 0
    default_shots: int = 2


DRINKS = {
    "espresso": Drink("espresso", "A straight shot of espresso.", "normal", False, default_shots=1),
    "ristretto": Drink("ristretto", "A short, concentrated, sweeter shot.", "ristretto", False, default_shots=1),
    "lungo": Drink("lungo", "A long-pulled, milder shot.", "lungo", False, default_shots=1),
    "americano": Drink(
        "americano", "Espresso topped with hot water.", "normal", False, hot_water_ml_per_shot=60
    ),
    "macchiato": Drink(
        "macchiato", "Espresso 'marked' with a spoonful of milk foam.", "normal", True,
        milk_rule="dollop", foam="just a dollop of thick foam on top", default_shots=1,
    ),
    "cortado": Drink(
        "cortado", "Espresso cut with an equal amount of warm milk.", "normal", True,
        milk_rule="equal", foam="very little foam - warm, silky milk",
    ),
    "flat white": Drink(
        "flat white", "Double shot with a thin layer of velvety microfoam.", "ristretto", True,
        milk_rule="ratio", milk_ratio=4.0, foam="thin (~0.5 cm) layer of microfoam",
    ),
    "cappuccino": Drink(
        "cappuccino", "Equal parts espresso, steamed milk and foam.", "normal", True,
        milk_rule="ratio", milk_ratio=2.0, foam="thick (~2 cm) layer of foam",
    ),
    "latte": Drink(
        "latte", "Espresso with plenty of steamed milk.", "normal", True,
        milk_rule="fill_cup", foam="thin (~1 cm) layer of microfoam",
    ),
}

DOLLOP_ML = 15


@dataclass
class Recipe:
    drink: Drink
    shots: int
    beans_g: int
    espresso_ml: int
    milk_ml: int = 0
    milk_type: Optional[str] = None
    cup_size: Optional[str] = None
    hot_water_ml: int = 0

    def instructions(self) -> str:
        lines = [f"=== Your {self.drink.name} ===", self.drink.description, ""]
        per_shot = SHOT_VOLUME_ML[self.drink.style]
        shot_word = "shot" if self.shots == 1 else "shots"
        lines.append(f"1. Grind {self.beans_g} g of coffee beans (fine espresso grind).")
        lines.append(
            f"2. Pull {self.shots} {self.drink.style} {shot_word} of {per_shot} ml each "
            f"-> {self.espresso_ml} ml of espresso total (aim for 25-30 seconds)."
        )
        step = 3
        if self.hot_water_ml:
            lines.append(f"{step}. Add {self.hot_water_ml} ml of hot water (~90 C) to the cup.")
            step += 1
        if self.drink.uses_milk:
            size = f" for a {self.cup_size} cup" if self.cup_size else ""
            lines.append(
                f"{step}. Steam {self.milk_ml} ml of {self.milk_type} milk{size}: "
                f"{self.drink.foam}."
            )
            step += 1
            lines.append(f"{step}. Pour the milk over the espresso and enjoy!")
            lines.append("")
            lines.append(f"Tip: {MILK_NOTES[self.milk_type]}")
        else:
            lines.append(f"{step}. Serve immediately and enjoy!")
        return "\n".join(lines)


def build_recipe(
    drink_name: str,
    shots: Optional[int] = None,
    milk_type: Optional[str] = None,
    cup_size: Optional[str] = None,
) -> Recipe:
    """Compute beans, espresso and milk volumes for the requested drink."""
    if drink_name not in DRINKS:
        raise ValueError(f"Unknown drink: {drink_name!r}")
    drink = DRINKS[drink_name]
    shots = shots or drink.default_shots
    if shots < 1:
        raise ValueError("Need at least one shot.")

    beans_g = shots * DOSE_PER_SHOT_G
    espresso_ml = shots * SHOT_VOLUME_ML[drink.style]
    recipe = Recipe(drink, shots, beans_g, espresso_ml, hot_water_ml=shots * drink.hot_water_ml_per_shot)

    if not drink.uses_milk:
        return recipe

    if milk_type not in MILK_TYPES:
        raise ValueError(f"{drink.name} needs a milk type from {MILK_TYPES}.")
    recipe.milk_type = milk_type

    if drink.milk_rule == "dollop":
        recipe.milk_ml = DOLLOP_ML
    elif drink.milk_rule == "equal":
        recipe.milk_ml = espresso_ml
    elif drink.milk_rule == "ratio":
        recipe.milk_ml = round(espresso_ml * drink.milk_ratio)
    elif drink.milk_rule == "fill_cup":
        if cup_size not in CUP_SIZES_ML:
            raise ValueError(f"{drink.name} needs a cup size from {tuple(CUP_SIZES_ML)}.")
        recipe.cup_size = cup_size
        recipe.milk_ml = CUP_SIZES_ML[cup_size] - espresso_ml
        if recipe.milk_ml <= 0:
            raise ValueError("Too many shots for that cup size.")
    return recipe
