from TP1.GameState import GameState

def get_heuristic1(sokoban):
    state = sokoban.state
    objectives = []
    for i,r in enumerate(state.static_state):
        for j, e in enumerate(r):
            if e == GameState.END:
                objectives.append((i,j))
    def distance(x,y):
        return abs(x[0]-y[0]) + abs(x[1]-y[1])
    def heuristic(sokoban):
        state = sokoban.state.save_state()
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
        return h
    return heuristic
