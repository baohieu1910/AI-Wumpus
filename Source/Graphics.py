from tkinter import *
from Constants import *

class Graphics:
    def __init__(self, world):
        self.root = Tk()
        self.root.title("WUMPUS WORLD")
        self.root.geometry("+200+50")

        self.canvas = Canvas(self.root, width=64 * world.col + NOTE_WIDTH, height=64 * world.row + 64,
                             background='white')
        self.outputFrame = Frame(self.root)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.outputFrame.pack(side="right", fill="both", expand=False)
        self.displayScore = None

        # Define the image file paths
        image_files = {
            'DOOR': DOOR,
            'TILE': TILE,
            'GOLD_TILE': GOLD_TILE,
            'WUMPUS': WUMPUS,
            'GOLD': GOLD,
            'BREEZE': BREEZE,
            'STENCH': STENCH,
            'PIT': PIT,
            'TERRAIN': TERRAIN,
            'PLAYER_DOWN': PLAYER_DOWN,
            'PLAYER_UP': PLAYER_UP,
            'PLAYER_LEFT': PLAYER_LEFT,
            'PLAYER_RIGHT': PLAYER_RIGHT,
            'ARROW_DOWN': ARROW_DOWN,
            'ARROW_UP': ARROW_UP,
            'ARROW_LEFT': ARROW_LEFT,
            'ARROW_RIGHT': ARROW_RIGHT,
            'SCORE': SCORE
        }

        # Load the images using a loop
        images = {}
        for name, file_path in image_files.items():
            images[name] = PhotoImage(file=file_path)

        # Assign the images to instance variables
        self.DOOR = images['DOOR']
        self.TILE = images['TILE']
        self.GOLD_TILE = images['GOLD_TILE']
        self.WUMPUS = images['WUMPUS']
        self.GOLD = images['GOLD']
        self.BREEZE = images['BREEZE']
        self.STENCH = images['STENCH']
        self.PIT = images['PIT']
        self.TERRAIN = images['TERRAIN']
        self.PLAYER_DOWN = images['PLAYER_DOWN']
        self.PLAYER_UP = images['PLAYER_UP']
        self.PLAYER_LEFT = images['PLAYER_LEFT']
        self.PLAYER_RIGHT = images['PLAYER_RIGHT']
        self.ARROW_DOWN = images['ARROW_DOWN']
        self.ARROW_UP = images['ARROW_UP']
        self.ARROW_LEFT = images['ARROW_LEFT']
        self.ARROW_RIGHT = images['ARROW_RIGHT']
        self.SCORE = images['SCORE']