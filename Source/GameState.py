import World

class GameState:
    def __init__(self,world):
        self.visited = []
        self.safeUnvisited = []
        self.state = dict()

    def addState(self, node):
        directions = ['up', 'down', 'right', 'left']

        for direction in directions:
            if getattr(node, direction) == '':
                setattr(node, direction, 'Wall')

        self.state[node.name] = node

        if node.name not in self.visited:
            self.visited.append(node.name)