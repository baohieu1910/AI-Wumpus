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
        if self.currDirection == Action.UP and state[self.currPos].up != 'Wall':
            self.currPos = state[self.currPos].up
        elif self.currDirection == Action.LEFT and state[self.currPos].left != 'Wall':
            self.currPos = state[self.currPos].left
        elif self.currDirection == Action.DOWN and state[self.currPos].down != 'Wall':
            self.currPos = state[self.currPos].down
        elif self.currDirection == Action.RIGHT and state[self.currPos].right != 'Wall':
            self.currPos = state[self.currPos].right