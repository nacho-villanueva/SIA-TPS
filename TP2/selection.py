from TP2.character import Character


def elite_selection():
    def _elite_selection(collection: list[Character], k):
        sorted_collection = sorted(collection, reverse=True)
        selection = sorted_collection * (k // len(sorted_collection))
        selection += sorted_collection[:k % len(sorted_collection)]
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
