import json
import random
import pandas as pd

from TP2.character import Character, CharacterRole, Gear
from TP2.constants import *
from TP2.datasets import DatasetLibrary
from TP2.genetic_algorithm import GeneticAlgorithm


# TODO: quizas se puede mover a otro archivo
def create_generation_zero(k: int, role: CharacterRole, precision: int):
    generation_zero = []
    multiplier = 10 ** precision
    for i in range(k):
        height = random.randint(MIN_HEIGHT * multiplier, MAX_HEIGHT * multiplier) / multiplier

        dl = DatasetLibrary()

        armour = dl.get_random_item(DatasetLibrary.DatasetType.ARMOUR)
        boots = dl.get_random_item(DatasetLibrary.DatasetType.BOOTS)
        gloves = dl.get_random_item(DatasetLibrary.DatasetType.GLOVES)
        helmet = dl.get_random_item(DatasetLibrary.DatasetType.HELMET)
        weapon = dl.get_random_item(DatasetLibrary.DatasetType.WEAPON)

        gear = Gear(weapon=weapon, armour=armour, boots=boots, gloves=gloves, helmet=helmet)

        character = Character(role, height, gear, "Mendez")
        generation_zero.append(character)

    for character in generation_zero:
        print(character)

    return generation_zero


if __name__ == "__main__":
    file = open("config.json")
    config_dict = json.load(file)

    population_size = config_dict["population_size"]
    role_name = config_dict["role"]
    character_role = CharacterRole.get_role_by_role_name(role_name)
    precision = config_dict["precision"]

    print("Reading files...")

    datasets = DatasetLibrary()
    datasets.load_dataset(DatasetLibrary.DatasetType.ARMOUR, config_dict["armours_dataset_path"])
    datasets.load_dataset(DatasetLibrary.DatasetType.BOOTS, config_dict["boots_dataset_path"])
    datasets.load_dataset(DatasetLibrary.DatasetType.GLOVES, config_dict["gloves_dataset_path"])
    datasets.load_dataset(DatasetLibrary.DatasetType.HELMET, config_dict["helmets_dataset_path"])
    datasets.load_dataset(DatasetLibrary.DatasetType.WEAPON, config_dict["weapons_dataset_path"])

    initial_population = create_generation_zero(population_size, character_role, precision)

    algorithm = GeneticAlgorithm(
        select_a=selection_functions[config_dict["selection_algorithm_1"]],
        crossover=crossover_functions[config_dict["crossover_algorithm"]],
        mutate=mutation_functions[config_dict["mutation_algorithm"]],
        stop=stop_conditions[config_dict["stop_condition"]],
        k=config_dict["K"],
        repopulate_a=selection_functions[config_dict["replacement_algorithm_1"]],
        fill_type=implementations[config_dict["implementation"]],
        initial_population=initial_population,
        select_b=selection_functions[config_dict["selection_algorithm_2"]],
        select_coefficient=config_dict["A"],
        repopulate_b=selection_functions[config_dict["replacement_algorithm_2"]],
        repopulate_coefficient=config_dict["B"]
    )
