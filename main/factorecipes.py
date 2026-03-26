from collections import defaultdict

type RecipeName = str
type IngredientName = str
type RecipeIngredients = dict[IngredientName, int]


class FactoRecipes:
    def __init__(self) -> None:
        self._recipes: dict[RecipeName, RecipeIngredients] = {}
        self._basic_ingredients: set[IngredientName] = set()
        self._needs_to_compute = defaultdict(int)

    def add_basic_ingredient(self, name: IngredientName) -> None:
        self._basic_ingredients.add(name)

    def add_recipe(self, recipe_name: str, ingredients: dict[str, int]) -> None:
        if recipe_name in self._recipes.keys():
            raise RuntimeError(f"The recipe '{recipe_name}' was already defined")
        self._recipes[recipe_name] = ingredients

    def add_need(self, name: str, quantity: int) -> None:
        self._needs_to_compute[name] += quantity

    def compute_needs(self) -> dict[str, int]:
        self._running_needs = defaultdict(int)

        while len(self._needs_to_compute) != 0:
            self._compute_current_needs()

        return self._running_needs

    def _compute_current_needs(self) -> None:
        new_needs = defaultdict(int)

        for ingredient, quantity in self._needs_to_compute.items():
            self._running_needs[ingredient] += quantity

            # If it's a basic ingredient nothing more to do
            if ingredient in self._basic_ingredients:
                continue

            if ingredient not in self._recipes.keys():
                raise RuntimeError(f"Missing recipe for '{ingredient}'")

            recipe = self._recipes[ingredient]

            for recipe_ingredient, recipe_ingredient_quantity in recipe.items():
                new_needs[recipe_ingredient] += recipe_ingredient_quantity * quantity

        self._needs_to_compute = new_needs
