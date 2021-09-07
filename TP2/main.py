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


def load_generation_from_file(role: CharacterRole):
    generation_zero = []
    f = open(os.path.join("results", f"initial_population.txt"), "r")
    lines = f.readlines()
    dl = DatasetLibrary()
    for line in lines:
        line = line.replace("\n", "")
        line = line.split(",")
        lastname = line[0]
        height = float(line[1])
        weapon = dl.get_item(DatasetLibrary.DatasetType.WEAPON, int(line[2]))
        armour = dl.get_item(DatasetLibrary.DatasetType.ARMOUR, int(line[3]))
        boots = dl.get_item(DatasetLibrary.DatasetType.BOOTS, int(line[4]))
        gloves = dl.get_item(DatasetLibrary.DatasetType.GLOVES, int(line[5]))
        helmet = dl.get_item(DatasetLibrary.DatasetType.HELMET, int(line[6]))
        character = Character(role, height, Gear(weapon=weapon, armour=armour, boots=boots, gloves=gloves, helmet=helmet), lastname)
        generation_zero.append(character)
    f.close()

    return generation_zero


def create_generation_zero(k: int, role: CharacterRole, precision: int):
    generation_zero = []
    multiplier = 10 ** precision
    dl = DatasetLibrary()
    fake = Faker()

    f = open(os.path.join("results", f"initial_population.txt"), "w")

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

        f.write(
            f"{last_name},{height},{weapon.item_id},{armour.item_id},{boots.item_id},{gloves.item_id},{helmet.item_id}\n")

    f.close()

    return generation_zero


def run(run_number=None):
    config = Config()
    print("Creating generation zero...")
    initial_population = create_generation_zero(config.population_size,
                                                CharacterRole.get_role_by_role_name(config.role), config.precision)

    # initial_population = load_generation_from_file(CharacterRole.get_role_by_role_name(config.role))

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
    print(f"{algorithm.max_fitness_character.lastname}")
    max_fit = algorithm.run()
    output_results[run_number] = max_fit


def main():
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

    output_results = [0] * config.run_instances
    threads = []
    if config.run_instances > 1:
        for i in range(config.run_instances):
            threads.append(threading.Thread(target=lambda: run(i)))
            threads[i].start()
        for t in threads:
            t.join()
    else:
        run(0)

    f = open(os.path.join("results", f"results.txt"), "w")
    for r in output_results:
        if isinstance(r, Character):
            f.write(f"{r.lastname}:{r.fitness}\n")
    f.close()


if __name__ == "__main__":
    main()
