from collections import defaultdict

type RecipeName = str
type IngredientName = str
type RecipeIngredients = dict[str, int]


class FactoRecipes:
    def __init__(self) -> None:
        self._recipes: dict[RecipeName, RecipeIngredients] = {}
        self._needs = defaultdict(int)

    def add_recipe(self, recipe_name: str, ingredients: dict[str, int]) -> None:
        if recipe_name in self._recipes.keys():
            raise RuntimeError(f"The recipe '{recipe_name}' was already defined")
        self._recipes[recipe_name] = ingredients

    def add_need(self, name: str, quantity: int) -> None:
        self._needs[name] += quantity

    def compute_needs(self) -> dict[str, int]:
        running_needs = defaultdict(int)

        for ingredient, quantity in self._needs.items():
            running_needs[ingredient] += quantity
            recipe = self._recipes[ingredient]

            for recipe_ingredient, recipe_ingredient_quantity in recipe.items():
                running_needs[recipe_ingredient] += (
                    recipe_ingredient_quantity * quantity
                )

        return running_needs
