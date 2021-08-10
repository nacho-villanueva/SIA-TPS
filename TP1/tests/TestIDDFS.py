import arcade

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
from TP1.algorithms.IDDFS import IDDFS
from TP1.tests.algorithmShower import AlgorithmShowerApplication

state = GameState.from_filepath("../config.txt")

game = Sokoban(state)

iddfs = IDDFS(game, 100)

solution = iddfs.run(minimum_depth=70)

print(len(solution))

if solution:
    state = GameState.from_filepath("../config.txt")
    asa = AlgorithmShowerApplication(Sokoban(state), solution, update_rate=0.25, move_automatically=False)
    arcade.run()
