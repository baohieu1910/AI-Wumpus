from Agent import Agent
from GameState import GameState
from KB import KnowledgeBase
from WumpusNode import WumpusNode
from Search import *


class AgentBrain(Agent):
    def __init__(self, world, starting_node):  # Starting node = (1,1)
        self.state = GameState(world)
        self.state.add_state(WumpusNode(starting_node.row, starting_node.col, world))
        self.agent = Agent(state=starting_node.name)
        self.KB = KnowledgeBase()
        self.KB.add(["~P" + str(starting_node.name)])
        self.KB.add(["~W" + str(starting_node.name)])
        self.exit = False
        self.move = []
        self.starting_node = starting_node
        self.world = world
        self.currentState = Action.RIGHT
        self.killing_wumpus = False
        self.scream = False

    def getAction(self):
        current_node = self.state.state[self.agent.currPos]
        tile_at_loc = self.world.listTiles[current_node.row][current_node.col]

        if current_node.name in self.state.unvisited_safe:
            self.state.unvisited_safe.remove(current_node.name)

        if self.scream == True:
            if self.agent.currDirection == Action.UP:
                self.state.unvisited_safe.append(current_node.up)
                self.clearKB(current_node.up)
            elif self.agent.currDirection == Action.LEFT:
                self.state.unvisited_safe.append(current_node.left)
                self.clearKB(current_node.left)
            elif self.agent.currDirection == Action.DOWN:
                self.state.unvisited_safe.append(current_node.down)
                self.clearKB(current_node.down)
            elif self.agent.currDirection == Action.RIGHT:
                self.state.unvisited_safe.append(current_node.right)
                self.clearKB(current_node.right)
            self.scream = False

        for item in self.state.visited[-10:]:
            row, col = item.split(',')
            tile = self.world.listTiles[int(row)][int(col)]
            if not tile.getStench() and self.KB.check(["~S" + str(item)]):
                self.clear_stench_KB(item)

        if current_node.name == self.starting_node.name and tile_at_loc.getBreeze():
            self.move.append(Action.CLIMB)

        if not self.exit and not self.killing_wumpus:
            if tile_at_loc.getStench():
                self.handle_stench(current_node)
                self.check_wumpus(current_node)
            elif not tile_at_loc.getStench():
                self.handle_no_stench(current_node)
            if tile_at_loc.getBreeze():
                self.handle_breeze(current_node)
            elif not tile_at_loc.getBreeze():
                self.handle_no_breeze(current_node)
            self.check_safe(current_node)
            if tile_at_loc.getGold():
                return Action.GRAB
            if not self.killing_wumpus:
                if len(self.state.unvisited_safe) > 0:
                    search = Search(self.state.state, self.agent.currPos, self.state.unvisited_safe[-1:],
                                    self.state.visited, self.agent.currDirection)
                    cost_path = search.unicost()
                    self.move = self.move_list(cost_path)
                else:
                    self.exit = True
                    search = Search(self.state.state, self.agent.currPos, self.starting_node.name,
                                    self.state.visited, self.agent.currDirection)
                    cost_path = search.unicost()
                    self.move = self.move_list(cost_path)

        if self.move:
            move = self.move.pop(0)
            if move == Action.SHOOT:
                self.killing_wumpus = False
            return move

    def clear_stench_KB(self, node):
        self.KB.KB.remove(['S' + node])

    def clearKB(self, node):
        node_name = 'W' + node
        remove = []
        for item in self.KB.KB:
            if node_name in item:
                remove.append(item)
        for item in remove:
            self.KB.KB.remove(item)

    def handle_breeze(self, current_node):
        sentence = []
        prefix = 'P'
        current_prefix = 'B'
        if current_node.up not in self.state.visited and current_node.up != 'Wall':
            sentence.append(prefix + current_node.up)
        if current_node.left not in self.state.visited and current_node.left != 'Wall':
            sentence.append(prefix + current_node.left)
        if current_node.down not in self.state.visited and current_node.down != 'Wall':
            sentence.append(prefix + current_node.down)
        if current_node.right not in self.state.visited and current_node.right != 'Wall':
            sentence.append(prefix + current_node.right)
        self.KB.add(sentence)
        self.KB.add([current_prefix + current_node.name])

    def handle_stench(self, current_node):
        sentence = []
        prefix = 'W'
        current_prefix = 'S'
        if current_node.up not in self.state.visited and current_node.up != 'Wall':
            sentence.append(prefix + current_node.up)
        if current_node.left not in self.state.visited and current_node.left != 'Wall':
            sentence.append(prefix + current_node.left)
        if current_node.down not in self.state.visited and current_node.down != 'Wall':
            sentence.append(prefix + current_node.down)
        if current_node.right not in self.state.visited and current_node.right != 'Wall':
            sentence.append(prefix + current_node.right)
        self.KB.add(sentence)
        self.KB.add([current_prefix + current_node.name])

    def handle_no_stench(self, current_node):
        prefix = '~W'
        if current_node.right not in self.state.visited and current_node.right != 'Wall':
            self.KB.add([prefix + current_node.right])
        if current_node.up not in self.state.visited and current_node.up != 'Wall':
            self.KB.add([prefix + current_node.up])
        if current_node.left not in self.state.visited and current_node.left != 'Wall':
            self.KB.add([prefix + current_node.left])
        if current_node.down not in self.state.visited and current_node.down != 'Wall':
            self.KB.add([prefix + current_node.down])

    def handle_no_breeze(self, current_node):
        prefix = '~P'
        if current_node.up not in self.state.visited and current_node.up != 'Wall':
            self.KB.add([prefix + current_node.up])
        if current_node.left not in self.state.visited and current_node.left != 'Wall':
            self.KB.add([prefix + current_node.left])
        if current_node.down not in self.state.visited and current_node.down != 'Wall':
            self.KB.add([prefix + current_node.down])
        if current_node.right not in self.state.visited and current_node.right != 'Wall':
            self.KB.add([prefix + current_node.right])

    def check_safe(self, current_node):
        if current_node.up != 'Wall' and current_node.up not in self.state.visited and current_node.up not in self.state.unvisited_safe:
            if self.KB.check(['W' + current_node.up]) and self.KB.check(['P' + current_node.up]):
                self.state.unvisited_safe.append(current_node.up)
        if current_node.left != 'Wall' and current_node.left not in self.state.visited and current_node.left not in self.state.unvisited_safe:
            if self.KB.check(['W' + current_node.left]) and self.KB.check(['P' + current_node.left]):
                self.state.unvisited_safe.append(current_node.left)
        if current_node.down != 'Wall' and current_node.down not in self.state.visited and current_node.down not in self.state.unvisited_safe:
            if self.KB.check(['W' + current_node.down]) and self.KB.check(['P' + current_node.down]):
                self.state.unvisited_safe.append(current_node.down)
        if current_node.right != 'Wall' and current_node.right not in self.state.visited and current_node.right not in self.state.unvisited_safe:
            if self.KB.check(['W' + current_node.right]) and self.KB.check(['P' + current_node.right]):
                self.state.unvisited_safe.append(current_node.right)

    def check_wumpus(self, current_node):
        row = current_node.row
        col = current_node.col
        if current_node.up != "Wall":
            if (self.KB.check(["W" + str(row) + "," + str(col - 1)])
                    and self.KB.check(["~S" + str(row - 1) + "," + str(col - 1)])
                    or self.KB.check(["W" + str(row) + "," + str(col + 1)])
                    and self.KB.check(["~S" + str(row - 1) + "," + str(col + 1)])):
                self.kill_wumpus("Up")
        if current_node.left != "Wall":
            if (self.KB.check(["W" + str(row - 1) + "," + str(col)])
                    and self.KB.check(["~S" + str(row - 1) + "," + str(col - 1)])
                    or self.KB.check(["W" + str(row + 1) + "," + str(col)])
                    and self.KB.check(["~S" + str(row + 1) + "," + str(col - 1)])):
                self.kill_wumpus("Left")
        if current_node.down != "Wall":
            if (self.KB.check(["W" + str(row) + "," + str(col - 1)])
                    and self.KB.check(["~S" + str(row + 1) + "," + str(col - 1)])
                    or self.KB.check(["W" + str(row) + "," + str(col + 1)])
                    and self.KB.check(["~S" + str(row + 1) + "," + str(col + 1)])):
                self.kill_wumpus("Down")
        if current_node.right != "Wall":
            if (self.KB.check(["W" + str(row - 1) + "," + str(col)])
                    and self.KB.check(["~S" + str(row - 1) + "," + str(col + 1)])
                    or self.KB.check(["W" + str(row + 1) + "," + str(col)])
                    and self.KB.check(["~S" + str(row + 1) + "," + str(col + 1)])):
                self.kill_wumpus("Right")

    def kill_wumpus(self, direction):
        self.killing_wumpus = True
        self.move = []
        if direction == 'Up':
            if self.agent.currDirection == Action.UP:
                self.move.insert(0, Action.SHOOT)
            elif self.agent.currDirection != Action.UP:
                self.agent.currDirection = Action.UP
                self.move.insert(0, Action.SHOOT)
                self.move.insert(0, Action.UP)
        elif direction == 'Left':
            if self.agent.currDirection == Action.LEFT:
                self.move.insert(0, Action.SHOOT)
            elif self.agent.currDirection != Action.LEFT:
                self.agent.currDirection = Action.LEFT
                self.move.insert(0, Action.SHOOT)
                self.move.insert(0, Action.LEFT)
        elif direction == 'Down':
            if self.agent.currDirection == Action.DOWN:
                self.move.insert(0, Action.SHOOT)
            elif self.agent.currDirection != Action.DOWN:
                self.agent.currDirection = Action.DOWN
                self.move.insert(0, Action.SHOOT)
                self.move.insert(0, Action.DOWN)
        elif direction == 'Right':
            if self.agent.currDirection == Action.RIGHT:
                self.move.insert(0, Action.SHOOT)
            elif self.agent.currDirection != Action.RIGHT:
                self.agent.currDirection = Action.RIGHT
                self.move.insert(0, Action.SHOOT)
                self.move.insert(0, Action.RIGHT)

    def move_list(self, path):
        direction = self.agent.currDirection
        state = self.agent.currPos
        current_node = self.state.state[state]
        move_list = []
        for item in path:
            row, col = item.split(',')
            new_state = WumpusNode(int(row), int(col), self.world)
            self.state.add_state(new_state)

            if str(direction.name) == str(Action.UP.name):
                if item == current_node.right:
                    move_list.append(Action.RIGHT)
                    move_list.append(Action.RIGHT)
                    direction = Action.RIGHT
                    current_node = self.state.state[current_node.right]
                elif item == current_node.up:
                    move_list.append(Action.UP)
                    current_node = self.state.state[current_node.up]
                elif item == current_node.down:
                    move_list.append(Action.DOWN)
                    move_list.append(Action.DOWN)
                    direction = Action.DOWN
                    current_node = self.state.state[current_node.down]
                elif item == current_node.left:
                    move_list.append(Action.LEFT)
                    move_list.append(Action.LEFT)
                    direction = Action.LEFT
                    current_node = self.state.state[current_node.left]
            elif str(direction.name) == str(Action.LEFT.name):
                if item == current_node.right:
                    move_list.append(Action.RIGHT)
                    move_list.append(Action.RIGHT)
                    direction = Action.RIGHT
                    current_node = self.state.state[current_node.right]
                elif item == current_node.up:
                    move_list.append(Action.UP)
                    move_list.append(Action.UP)
                    direction = Action.UP
                    current_node = self.state.state[current_node.up]
                elif item == current_node.down:
                    move_list.append(Action.DOWN)
                    move_list.append(Action.DOWN)
                    direction = Action.DOWN
                    current_node = self.state.state[current_node.down]
                elif item == current_node.left:
                    move_list.append(Action.LEFT)
                    current_node = self.state.state[current_node.left]
            elif str(direction.name) == str(Action.DOWN.name):
                if item == current_node.right:
                    move_list.append(Action.RIGHT)
                    move_list.append(Action.RIGHT)
                    direction = Action.RIGHT
                    current_node = self.state.state[current_node.right]
                elif item == current_node.up:
                    move_list.append(Action.UP)
                    move_list.append(Action.UP)
                    direction = Action.UP
                    current_node = self.state.state[current_node.up]
                elif item == current_node.down:
                    move_list.append(Action.DOWN)
                    current_node = self.state.state[current_node.down]
                elif item == current_node.left:
                    move_list.append(Action.LEFT)
                    move_list.append(Action.LEFT)
                    direction = Action.LEFT
                    current_node = self.state.state[current_node.left]
            elif str(direction.name) == str(Action.RIGHT.name):
                if item == current_node.right:
                    move_list.append(Action.RIGHT)
                    current_node = self.state.state[current_node.right]
                elif item == current_node.up:
                    move_list.append(Action.UP)
                    move_list.append(Action.UP)
                    direction = Action.UP
                    current_node = self.state.state[current_node.up]
                elif item == current_node.down:
                    move_list.append(Action.DOWN)
                    move_list.append(Action.DOWN)
                    direction = Action.DOWN
                    current_node = self.state.state[current_node.down]
                elif item == current_node.left:
                    move_list.append(Action.LEFT)
                    move_list.append(Action.LEFT)
                    direction = Action.LEFT
                    current_node = self.state.state[current_node.left]

        if self.exit:
            move_list.append(Action.CLIMB)
        if self.agent.currDirection != move_list[0]:
            self.agent.currDirection = move_list[0]
        else:
            self.agent.moveFoward(self.state.state)
        return move_list