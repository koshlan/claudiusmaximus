"""Interactive command-line prompts for the espresso calculator."""

from typing import Callable, Sequence

from .recipes import CUP_SIZES_ML, DRINKS, MILK_TYPES, build_recipe


def choose(prompt: str, options: Sequence[str], ask: Callable[[str], str] = input) -> str:
    """Ask until the user picks one of `options` (by number or name)."""
    menu = "\n".join(f"  {i}. {opt}" for i, opt in enumerate(options, 1))
    while True:
        answer = ask(f"{prompt}\n{menu}\n> ").strip().lower()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        if answer in options:
            return answer
        print(f"Sorry, '{answer}' isn't an option. Please try again.")


def run(ask: Callable[[str], str] = input) -> str:
    print("Welcome to the espresso drink calculator!\n")
    drink_name = choose("Which drink would you like?", list(DRINKS), ask)
    drink = DRINKS[drink_name]

    strength = choose("Single or double shot?", ["single", "double"], ask)
    shots = 2 if strength == "double" else 1

    milk_type = cup_size = None
    if drink.uses_milk:
        print(f"\nA {drink_name} is made with milk - a few questions about that.")
        milk_type = choose("What kind of milk would you like?", list(MILK_TYPES), ask)
        if drink.milk_rule == "fill_cup":
            sizes = ", ".join(f"{k} = {v} ml" for k, v in CUP_SIZES_ML.items())
            cup_size = choose(f"What cup size? ({sizes})", list(CUP_SIZES_ML), ask)

    recipe = build_recipe(drink_name, shots=shots, milk_type=milk_type, cup_size=cup_size)
    text = recipe.instructions()
    print("\n" + text)
    return text


def main() -> None:
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")


if __name__ == "__main__":
    main()
