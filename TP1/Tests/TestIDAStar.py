import arcade
from TP1.SokobanAlgorithmApplication import AlgorithmShowerApplication
from os.path import isfile

from TP1.GameState import GameState
from TP1.Sokoban import Sokoban
import sys
from TP1.Algorithms.IDAStar import IDAStar

    

def main(initial_state):
    if not isfile(initial_state):
        print(f"Config file not found: {initial_state}")
        exit(1)
    state = GameState.from_filepath(initial_state)
    sokoban = Sokoban(state)
    objectives = []
    for i,r in enumerate(state.static_state):
        for j, e in enumerate(r):
            if e == GameState.END:
                objectives.append((i,j))
    def distance(x,y):
        return abs(x[0]-y[0]) + abs(x[1]-y[1])
    global runs
    runs = 0
    def heuristic(state, g):
        global runs
        h = 0
        p_setted = False
        p_dist_min = 0
        for ice in state[1]:
            p_dist = distance(state[0],ice)
            if not p_setted:
                p_dist_min = p_dist
            else:
                if p_dist_min > p_dist:
                    p_dist_min = p_dist
            min_dist = 0
            setted = False
            for o in objectives:
                dist = distance(ice,o)
                if not setted:
                    min_dist = dist
                    setted = True
                else:
                    if min_dist > dist:
                        min_dist = dist
            if setted:
                h += min_dist
        h += p_dist_min - 1
        return h + g




    algorithm = IDAStar(sokoban,heuristic)
    algorithm.run()
    print(algorithm.statistics)
    shower_app = AlgorithmShowerApplication(sokoban, algorithm.run(), update_rate=1 / 4)
    arcade.run()


if __name__ == "__main__":
    config_file = "./config.txt"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (../config.txt)")
    main(config_file)
