import json
import random
import sys
import threading
import os

import pandas as pd

from faker import Faker
from TP2.character import Character, CharacterRole, Gear
from TP2.config import Config
from TP2.constants import *
from TP2.datasets import DatasetLibrary
from TP2.genetic_algorithm import GeneticAlgorithm

output_results = []


def create_generation_zero(k: int, role: CharacterRole, precision: int):
    generation_zero = []
    multiplier = 10 ** precision
    dl = DatasetLibrary()
    fake = Faker()

    for i in range(k):
        height = random.randint(MIN_HEIGHT * multiplier, MAX_HEIGHT * multiplier) / multiplier

        armour = dl.get_random_item(DatasetLibrary.DatasetType.ARMOUR)
        boots = dl.get_random_item(DatasetLibrary.DatasetType.BOOTS)
        gloves = dl.get_random_item(DatasetLibrary.DatasetType.GLOVES)
        helmet = dl.get_random_item(DatasetLibrary.DatasetType.HELMET)
        weapon = dl.get_random_item(DatasetLibrary.DatasetType.WEAPON)

        gear = Gear(weapon=weapon, armour=armour, boots=boots, gloves=gloves, helmet=helmet)

        last_name = fake.last_name()

        character = Character(role, height, gear, last_name)
        generation_zero.append(character)

    return generation_zero


def run(run_number=None):
    config = Config()
    print("Creating generation zero...")
    initial_population = create_generation_zero(config.population_size,
                                                CharacterRole.get_role_by_role_name(config.role), config.precision)

    print("Setting up Genetic Algorithm...")
    algorithm = GeneticAlgorithm(
        select_a=get_selection_function(config.selection_1),
        crossover=get_crossover_function(config.crossover_algorithm),
        mutate=get_mutation_function(config.mutation_algorithm),
        stop=get_stop_condition(config.stop_condition),
        k=config.K,
        repopulate_a=get_selection_function(config.replacement_1),
        fill_type=implementations[config.implementation],
        initial_population=initial_population,
        select_b=get_selection_function(config.selection_2),
        select_coefficient=config.A,
        repopulate_b=get_selection_function(config.replacement_2),
        repopulate_coefficient=config.B
    )

    print("Running...")
    max_fit = algorithm.run()
    output_results[run_number] = max_fit.fitness


def main(instances=1):
    global output_results
    config_file = "./config.json"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (./config.json)")

    file = open(config_file)
    config_dict = json.load(file)

    if config_dict["K"] % 2 != 0:
        print(f"K is not an even number. Setting K = {config_dict['K'] + 1}")
        config_dict['K'] += 1

    config = Config()
    config.setup_config(config_dict)

    print("Reading files...")

    datasets = DatasetLibrary()
    datasets.load_dataset(DatasetLibrary.DatasetType.ARMOUR, config_dict["armours_dataset_path"])
    datasets.load_dataset(DatasetLibrary.DatasetType.BOOTS, config_dict["boots_dataset_path"])
    datasets.load_dataset(DatasetLibrary.DatasetType.GLOVES, config_dict["gloves_dataset_path"])
    datasets.load_dataset(DatasetLibrary.DatasetType.HELMET, config_dict["helmets_dataset_path"])
    datasets.load_dataset(DatasetLibrary.DatasetType.WEAPON, config_dict["weapons_dataset_path"])

    if not os.path.isdir("results"):
        os.makedirs("results")

    output_results = [0] * instances
    threads = []
    if instances > 1:
        for i in range(instances):
            threads.append(threading.Thread(target=lambda: run(i)))
            threads[i].start()
        for t in threads:
            t.join()
    else:
        run(0)

    f = open(os.path.join("results", f"results.txt"), "w")
    for r in output_results:
        f.write(f"{r}\n")
    f.close()


if __name__ == "__main__":
    main(1)
