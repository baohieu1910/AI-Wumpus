from tkinter import *
from Constants import *

class Graphics:
    def __init__(self, world):
        self.root = Tk()
        self.root.title("WUMPUS WORLD")
        self.root.geometry("+200+50")

        self.canvas = Canvas(self.root, width=64 * world.col + 64 * 4, height=64 * world.row + 64, background='white')
        self.outputFrame = Frame(self.root)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.outputFrame.pack(side="right", fill="both", expand=False)
        self.displayScore = None
        self.DOOR = PhotoImage(file=DOOR)
        self.TILE = PhotoImage(file=TILE)
        self.GOLD_TILE = PhotoImage(file=GOLD_TILE)
        self.WUMPUS = PhotoImage(file=WUMPUS)
        self.GOLD = PhotoImage(file=GOLD)
        self.BREEZE = PhotoImage(file=BREEZE)
        self.STENCH = PhotoImage(file=STENCH)
        self.PIT = PhotoImage(file=PIT)
        self.TERRAIN = PhotoImage(file=TERRAIN)
        self.PLAYER_DOWN = PhotoImage(file=PLAYER_DOWN)
        self.PLAYER_UP = PhotoImage(file=PLAYER_UP)
        self.PLAYER_LEFT = PhotoImage(file=PLAYER_LEFT)
        self.PLAYER_RIGHT = PhotoImage(file=PLAYER_RIGHT)
        self.ARROW_DOWN = PhotoImage(file=ARROW_DOWN)
        self.ARROW_UP = PhotoImage(file=ARROW_UP)
        self.ARROW_LEFT = PhotoImage(file=ARROW_LEFT)
        self.ARROW_RIGHT = PhotoImage(file=ARROW_RIGHT)
        self.SCORE = PhotoImage(file=SCORE)