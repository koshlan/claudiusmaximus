# espresso-calc

A very basic interactive Python package that asks what espresso drink you want,
clarifies your milk preferences, and tells you exactly how many grams of beans
to grind, how much espresso to pull, and how much milk to steam.

## Install & run

```bash
pip install -e .
espresso-calc          # or: python -m espresso_calc
```

## Example

```
Which drink would you like?
  1. espresso  2. ristretto  3. lungo  4. americano  5. macchiato
  6. cortado   7. flat white 8. cappuccino 9. latte
> latte
Single or double shot? > double
What kind of milk would you like? > oat
What cup size? (small = 240 ml, medium = 360 ml, large = 480 ml) > medium

=== Your latte ===
1. Grind 18 g of coffee beans (fine espresso grind).
2. Pull 2 normal shots of 30 ml each -> 60 ml of espresso total (aim for 25-30 seconds).
3. Steam 300 ml of oat milk for a medium cup: thin (~1 cm) layer of microfoam.
4. Pour the milk over the espresso and enjoy!
```

## Rules of thumb used

| Item | Value |
|---|---|
| Beans | 9 g per shot (18 g for a double) |
| Shot volume | ristretto 15 ml, normal 30 ml, lungo 60 ml |
| Macchiato | 15 ml dollop of foam |
| Cortado | milk = espresso volume |
| Cappuccino | milk = 2x espresso (half steamed milk, half foam) |
| Flat white | ristretto shots, milk = 4x espresso |
| Latte | milk fills the rest of the chosen cup |
| Americano | 60 ml hot water per shot |

## Tests

```bash
python -m unittest discover -s tests
```
