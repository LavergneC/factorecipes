from collections import defaultdict

import yaml

type RecipeName = str
type IngredientName = str
type RecipeIngredients = dict[IngredientName, float]


class FactoRecipes:
    def __init__(self) -> None:
        self._recipes: dict[RecipeName, RecipeIngredients] = {}
        self._basic_ingredients: set[IngredientName] = set()
        self._needs_to_compute = defaultdict(float)

    def load_recipes_file(self, path: str):
        with open(path) as config_file:
            data: dict = yaml.load(config_file, Loader=yaml.FullLoader)
            self._basic_ingredients = {
                ingredient for ingredient in data["basic-ingredients"].split()
            }
            self._recipes = data["recipes"]

    def add_need(self, name: str, quantity: float) -> None:
        self._needs_to_compute[name] += quantity

    def compute_needs(self) -> dict[str, float]:
        self._running_needs = defaultdict(float)

        while len(self._needs_to_compute) != 0:
            self._compute_current_needs()

        return self._running_needs

    def add_basic_ingredient(self, name: IngredientName) -> None:
        self._basic_ingredients.add(name)

    def add_recipe(self, recipe_name: str, ingredients: dict[str, float]) -> None:
        if recipe_name in self._recipes.keys():
            raise RuntimeError(f"The recipe '{recipe_name}' was already defined")
        self._recipes[recipe_name] = ingredients

    def _compute_current_needs(self) -> None:
        new_needs = defaultdict(float)

        for ingredient, quantity in self._needs_to_compute.items():
            self._running_needs[ingredient] += quantity

            # If it's a basic ingredient nothing more to do
            if ingredient in self._basic_ingredients:
                continue

            if ingredient not in self._recipes.keys():
                raise RuntimeError(f"Missing recipe for '{ingredient}'")

            recipe: RecipeIngredients = self._recipes[ingredient]

            for recipe_ingredient, recipe_ingredient_quantity in recipe.items():
                new_needs[recipe_ingredient] += recipe_ingredient_quantity * quantity

        self._needs_to_compute = new_needs


if __name__ == "__main__":
    facto_recipes = FactoRecipes()
    facto_recipes.load_recipes_file("factorio.yaml")

    facto_recipes.add_need(name="missile-jaune", quantity=800)
    facto_recipes.add_need(name="munition-rouge", quantity=400)
    facto_recipes.add_need(name="obus-bleu", quantity=150)

    print(facto_recipes.compute_needs())
