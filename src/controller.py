from constants import *

class ManualAgent():
    def __init__(self):
        self.currentState = Action.RIGHT

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