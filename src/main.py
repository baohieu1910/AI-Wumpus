import world, graphics
from menu import Menu
from constants import *

if __name__ == "__main__":
    wumpus_world = world.WumpusWorld()
    menu = Menu()
    state = menu.run()
    map = int(state[-1])

    wumpus_world.read_Map(MAP_LIST[map - 1])
    board = graphics.Board(wumpus_world)
    board.createWorld()
    board.mainloop()

