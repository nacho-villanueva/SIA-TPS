from TP1.GameState import GameState
from TP1.Sokoban import Sokoban, Movement

state = GameState.from_code('''    #### 
#####@ # 
# $ $$$##
#  .#.  #
## #  # #
 # . .  #
 #   ####
 #####   ''')

game = Sokoban(state)
print(game.state)
game.move(Movement.DOWN)
print("--------------------------")
print(game.state)
game.move(Movement.LEFT)
print("--------------------------")
print(game.state)
game.move(Movement.LEFT)
print("--------------------------")
print(game.state)