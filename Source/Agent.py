from Search import *

class Agent:
    def __init__(self, state):
        self.current_state = state
        self.current_direction = Action.RIGHT
        self.has_gold = False
        self.has_killed_wumpus = False
        self.is_leaving = False

    # Check wall and move forward
    def move_foward(self, state):
        if self.current_direction == Action.UP and state[self.current_state].up != 'Wall':
            self.current_state = state[self.current_state].up
        elif self.current_direction == Action.LEFT and state[self.current_state].left != 'Wall':
            self.current_state = state[self.current_state].left
        elif self.current_direction == Action.DOWN and state[self.current_state].down != 'Wall':
            self.current_state = state[self.current_state].down
        elif self.current_direction == Action.RIGHT and state[self.current_state].right != 'Wall':
            self.current_state = state[self.current_state].right
    def getAction(self, key):
        if key == 'w':
            return Action.UP
        if key == 'a':
            return Action.LEFT
        if key == 's':
            return Action.DOWN
        if key == 'd':
            return Action.RIGHT
        if key == 'f':
            return Action.SHOOT
        if key == 'g':
            return Action.GRAB
        if key == 'c':
            return Action.CLIMB
        return None