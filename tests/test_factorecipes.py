import pytest

from main.factorecipes import FactoRecipes


class TestFactoRecipes:
    def test_simple_recipe_usage(self):
        facto_recipes = FactoRecipes()
        facto_recipes.add_basic_ingredient(name="jambon")
        facto_recipes.add_basic_ingredient(name="beurre")

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

    def test_two_recipes_usage_one_level(self):
        facto_recipes = FactoRecipes()
        facto_recipes.add_basic_ingredient(name="jambon")
        facto_recipes.add_basic_ingredient(name="beurre")
        facto_recipes.add_basic_ingredient(name="fromage")

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

    def test_two_recipes_usage_two_levels(self):
        facto_recipes = FactoRecipes()

        facto_recipes.add_basic_ingredient(name="jambon")
        facto_recipes.add_basic_ingredient(name="lait")

        facto_recipes.add_recipe(
            recipe_name="jambon beurre",
            ingredients={"jambon": 2, "beurre": 5},
        )
        facto_recipes.add_recipe(
            recipe_name="beurre",
            ingredients={"lait": 5},
        )
        facto_recipes.add_need(name="jambon beurre", quantity=2)

        assert facto_recipes.compute_needs() == {
            "jambon beurre": 2,
            "jambon": 4,
            "beurre": 10,
            "lait": 50,
        }

    def test_missing_recipe(self):
        facto_recipes = FactoRecipes()
        facto_recipes.add_recipe(
            recipe_name="beurre",
            ingredients={"lait": 2},
        )
        facto_recipes.add_need(name="beurre", quantity=2)

        with pytest.raises(RuntimeError, match="Missing recipe for 'lait'"):
            facto_recipes.compute_needs()

    def test_with_float(self):
        facto_recipes = FactoRecipes()
        facto_recipes.add_basic_ingredient(name="sable")

        facto_recipes.add_recipe(
            recipe_name="chateau de sable",
            ingredients={"sable": 50.5},
        )
        facto_recipes.add_need(name="chateau de sable", quantity=3)

        assert facto_recipes.compute_needs() == {"chateau de sable": 3, "sable": 151.5}

    def test_simple_file_loading(self):
        facto_recipes = FactoRecipes()
        facto_recipes.load_recipes_file("tests/import_files/simple_test_file.yaml")

        assert facto_recipes._basic_ingredients == {"jambon", "beurre"}
        assert facto_recipes._recipes == {"jambon-beurre": {"jambon": 2, "beurre": 5}}
