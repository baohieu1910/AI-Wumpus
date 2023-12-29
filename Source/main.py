from World import WumpusWorld
from Board import Board
from Menu import Menu
from Constants import *

if __name__ == "__main__":
    wumpus_world = WumpusWorld()
    menu = Menu()
    state = menu.run()
    map = int(state[-1])

    wumpus_world.readMap(MAP_LIST[map - 1])
    board = Board(wumpus_world)
    board.createWorld()
    board.run()

