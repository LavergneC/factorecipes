import pytest

from main.factorecipes import FactoRecipes


class TestFactoRecipes:
    def test_simple_recipe_usage(self):
        facto_recipes = FactoRecipes()
        facto_recipes.add_recipe(
            recipe_name="jambon beurre",
            ingredients={"jambon": 2, "beurre": 5},
        )
        facto_recipes.add_need(name="jambon beurre", quantity=2)

        assert facto_recipes.compute_needs() == {
            "jambon beurre": 2,
            "jambon": 4,
            "beurre": 10,
        }

    def test_recipe_redefinition(self):
        facto_recipes = FactoRecipes()
        facto_recipes.add_recipe(
            recipe_name="jambon beurre",
            ingredients={"jambon": 2, "beurre": 5},
        )

        with pytest.raises(
            RuntimeError,
            match="The recipe 'jambon beurre' was already defined",
        ):
            facto_recipes.add_recipe(
                recipe_name="jambon beurre",
                ingredients={"jambon": 2, "beurre": 5, "pain": 1},
            )

    def test_two_recipe_usage_one_level(self):
        facto_recipes = FactoRecipes()
        facto_recipes.add_recipe(
            recipe_name="jambon beurre",
            ingredients={"jambon": 2, "beurre": 5},
        )
        facto_recipes.add_recipe(
            recipe_name="beurre fromage",
            ingredients={"fromage": 3, "beurre": 5},
        )
        facto_recipes.add_need(name="jambon beurre", quantity=2)
        facto_recipes.add_need(name="beurre fromage", quantity=3)

        assert facto_recipes.compute_needs() == {
            "jambon beurre": 2,
            "beurre fromage": 3,
            "jambon": 4,
            "beurre": 25,
            "fromage": 9,
        }
