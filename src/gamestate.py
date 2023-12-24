import world

class Game_State:
    def __init__(self,world):
        self.visited = []
        self.unvisited_safe = []
        self.state = dict()
        self.max_row= world.height
        self.max_col = world.width

    def add_state(self,node):
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