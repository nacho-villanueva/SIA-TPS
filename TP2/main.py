import json
import random
import pandas as pd

from TP2.character import Character, CharacterRole
from TP2.constants import *
from TP2.genetic_algorithm import GeneticAlgorithm

from TP2.items.armour import Armour
from TP2.items.boots import Boots
from TP2.items.gloves import Gloves
from TP2.items.helmet import Helmet
from TP2.items.weapon import Weapon


# TODO: quizas se puede mover a otro archivo
def create_generation_zero(armours: pd.DataFrame, boots: pd.DataFrame, gloves: pd.DataFrame, helmets: pd.DataFrame,
                           weapons: pd.DataFrame, k: int, role: CharacterRole, precision: int):
    generation_zero = []
    multiplier = 10 ** precision
    for i in range(k):
        height = random.randint(MIN_HEIGHT * multiplier, MAX_HEIGHT * multiplier) / multiplier

        gear = []

        # Pick random armour
        random_armour_index = random.randint(0, len(armours) - 1)
        armour_row = armours.iloc[random_armour_index]
        new_armour = Armour(armour_row["Fu"], armour_row["Ag"], armour_row["Ex"], armour_row["Re"], armour_row["Vi"])
        gear.append(new_armour)

        # Pick random boots
        random_boots_index = random.randint(0, len(boots) - 1)
        boots_row = boots.iloc[random_boots_index]
        new_boots = Boots(boots_row["Fu"], boots_row["Ag"], boots_row["Ex"], boots_row["Re"], boots_row["Vi"])
        gear.append(new_boots)

        # Pick random gloves
        random_gloves_index = random.randint(0, len(gloves) - 1)
        gloves_row = gloves.iloc[random_gloves_index]
        new_gloves = Gloves(gloves_row["Fu"], gloves_row["Ag"], gloves_row["Ex"], gloves_row["Re"], gloves_row["Vi"])
        gear.append(new_gloves)

        # Pick random helmet
        random_helmet_index = random.randint(0, len(helmets) - 1)
        helmet_row = helmets.iloc[random_helmet_index]
        new_helmet = Helmet(helmet_row["Fu"], helmet_row["Ag"], helmet_row["Ex"], helmet_row["Re"], helmet_row["Vi"])
        gear.append(new_helmet)

        # Pick random weapon
        random_weapon_index = random.randint(0, len(weapons) - 1)
        weapon_row = weapons.iloc[random_weapon_index]
        new_weapon = Weapon(weapon_row["Fu"], weapon_row["Ag"], weapon_row["Ex"], weapon_row["Re"], weapon_row["Vi"])
        gear.append(new_weapon)

        character = Character(role, height, gear, "Mendez")
        generation_zero.append(character)

    for character in generation_zero:
        print(character)


if __name__ == "__main__":
    file = open("config.json")
    config_dict = json.load(file)
    algorithm = GeneticAlgorithm(
        select_a=selection_functions[config_dict["selection_algorithm_1"]],
        crossover=crossover_functions[config_dict["crossover_algorithm"]],
        mutate=mutation_functions[config_dict["mutation_algorithm"]],
        stop=stop_conditions[config_dict["stop_condition"]],
        repopulate_a=selection_functions[config_dict["replacement_algorithm_1"]],
        fill_type=implementations[config_dict["implementation"]],
        population_size=config_dict["population_size"],
        select_b=selection_functions[config_dict["selection_algorithm_2"]],
        select_coefficient=config_dict["A"],
        repopulate_b=selection_functions[config_dict["replacement_algorithm_2"]],
        repopulate_coefficient=config_dict["B"]
    )

    population_size = config_dict["population_size"]
    role_name = config_dict["role"]
    character_role = CharacterRole.get_role_by_role_name(role_name)
    precision = config_dict["precision"]

    print("Reading files...")

    armours_dataset = pd.read_csv(config_dict["armours_dataset_path"], sep='\t')
    armours_df = pd.DataFrame(data=armours_dataset)

    boots_dataset = pd.read_csv(config_dict["boots_dataset_path"], sep='\t')
    boots_df = pd.DataFrame(data=boots_dataset)

    gloves_dataset = pd.read_csv(config_dict["gloves_dataset_path"], sep='\t')
    gloves_df = pd.DataFrame(data=gloves_dataset)

    helmets_dataset = pd.read_csv(config_dict["helmets_dataset_path"], sep='\t')
    helmets_df = pd.DataFrame(data=helmets_dataset)

    weapons_dataset = pd.read_csv(config_dict["weapons_dataset_path"], sep='\t')
    weapons_df = pd.DataFrame(data=weapons_dataset)

    create_generation_zero(armours_df, boots_df, gloves_df, helmets_df, weapons_df, population_size, character_role, precision)
