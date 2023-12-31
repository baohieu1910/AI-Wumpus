from Search import *

class Agent:
    def __init__(self, pos):
        self.currPos = pos
        self.currDirection = Action.RIGHT
        self.hasGold = False
        self.killedWumpus = False
        self.leaving = False

    # Check wall and move forward
    def moveFoward(self, state):
        directions = {
            Action.UP: 'up',
            Action.LEFT: 'left',
            Action.DOWN: 'down',
            Action.RIGHT: 'right'
        }

        next_pos = getattr(state[self.currPos], directions[self.currDirection])
        if next_pos != 'Wall':
            self.currPos = next_pos