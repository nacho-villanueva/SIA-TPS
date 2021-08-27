def elite_selection():
    def _elite_selection(collection, k):
        sorted_collection = sorted(collection)
        selection = sorted_collection * (len(sorted_collection) // k)
        selection += sorted_collection[:len(sorted_collection) % k]
        return selection

    return _elite_selection


def roulette_selection():  # TODO: IMPLEMENTAR
    return []


def universal_selection():  # TODO: IMPLEMENTAR
    return []


def boltzmann_selection():  # TODO: IMPLEMENTAR
    return []


def deterministic_tournament_selection():  # TODO: IMPLEMENTAR
    return []


def stochastic_tournament_selection():  # TODO: IMPLEMENTAR
    return []


def ranking_selection():  # TODO: IMPLEMENTAR
    return []
