import World

class GameState:
    def __init__(self,world):
        self.visited = []
        self.safeUnvisited = []
        self.state = dict()

    def addState(self, node):
        if node.left == '':
            node.left = 'Wall'
        if node.right == '':
            node.right = 'Wall'
        if node.up == '':
            node.up = 'Wall'
        if node.down == '':
            node.down = 'Wall'
        self.state[node.name] = node
        if node.name not in self.visited:
            self.visited.append(node.name)