from Agent import Agent
from GameState import GameState
from KB import KnowledgeBase
from WumpusNode import WumpusNode
from Search import *

directions = {
            Action.UP: 'up',
            Action.LEFT: 'left',
            Action.DOWN: 'down',
            Action.RIGHT: 'right'
        }
class AgentBrain():
    def __init__(self, world, initNode):
        self.state = GameState(world)
        self.state.addState(WumpusNode(initNode.row, initNode.col, world))
        self.agent = Agent(initNode.name)
        self.KB = KnowledgeBase()
        self.KB.add(["~P" + str(initNode.name)])
        self.KB.add(["~W" + str(initNode.name)])
        self.exit = False
        self.move = []
        self.initNode = initNode
        self.world = world
        self.currentState = Action.RIGHT
        self.killingWumpus = False
        self.scream = False

    def getAction(self):
        currNode = self.state.state[self.agent.currPos]
        locTile = self.world.listTiles[currNode.row][currNode.col]

        if currNode.name in self.state.safeUnvisited:
            self.state.safeUnvisited.remove(currNode.name)

        if self.scream:
            direction = self.agent.currDirection
            attribute = directions.get(direction)
            if attribute:
                adjacent_node_name = getattr(currNode, attribute, None)
                if adjacent_node_name:
                    self.state.safeUnvisited.append(adjacent_node_name)
                    self.clearKB(adjacent_node_name)
                self.scream = False

        for item in self.state.visited[-10:]:
            row, col = item.split(',')
            tile = self.world.listTiles[int(row)][int(col)]
            if not tile.getStench() and self.KB.check(["~S" + str(item)]):
                self.KB.KB.remove(['S' + item])

        if currNode.name == self.initNode.name and locTile.getBreeze():
            self.move.append(Action.CLIMB)

        if not self.exit and not self.killingWumpus:
            stench = locTile.getStench()
            breeze = locTile.getBreeze()

            self.handleStench(currNode, stench)
            if stench:
                self.handleWumpus(currNode)

            self.handleBreeze(currNode, breeze)

            self.addSafeNode(currNode)

            if locTile.getGold():
                return Action.GRAB

            if not self.killingWumpus:
                if len(self.state.safeUnvisited) > 0:
                    search = Search(self.state.state, self.agent.currPos, self.state.safeUnvisited[-1:],
                                        self.state.visited, self.agent.currDirection)
                    costPath = search.unicost()
                    self.move = self.moveList(costPath)
                else:
                    self.exit = True
                    search = Search(self.state.state, self.agent.currPos, self.initNode.name,
                                        self.state.visited, self.agent.currDirection)
                    costPath = search.unicost()
                    self.move = self.moveList(costPath)

        if self.move:
            move = self.move.pop(0)
            if move == Action.SHOOT:
                self.killingWumpus = False
            return move

    def clearKB(self, node):
        node_name = 'W' + node
        remove = []
        for item in self.KB.KB:
            if node_name in item:
                remove.append(item)
        for item in remove:
            self.KB.KB.remove(item)

    def handleBreeze(self, current_node, breeze):
        if breeze:
            adjacent_nodes = [current_node.up, current_node.left, current_node.down, current_node.right]
            prefix = 'P'
            sentence = [prefix + node for node in adjacent_nodes
                        if node not in self.state.visited and node != 'Wall']
            self.KB.add(sentence)
            self.KB.add(['B' + current_node.name])
        else:
            prefix = '~P'
            for direction in directions.values():
                node_name = getattr(current_node, direction, None)
                if node_name not in self.state.visited and node_name != 'Wall':
                    self.KB.add([prefix + node_name])

    def handleStench(self, current_node, stench):
        adjacent_nodes = [current_node.up, current_node.left, current_node.down, current_node.right]

        if stench:
            prefix = 'W'
            current_prefix = 'S'
            sentence = [prefix + node for node in adjacent_nodes
                        if node not in self.state.visited and node != 'Wall']
            self.KB.add(sentence)
            self.KB.add([current_prefix + current_node.name])
        else:
            prefix = '~W'
            for direction in directions.values():
                node_name = getattr(current_node, direction, None)
                if node_name not in self.state.visited and node_name != 'Wall':
                    self.KB.add([prefix + node_name])


    def addSafeNode(self, current_node):
        for direction in directions.values():
            adjacent_node_name = getattr(current_node, direction, None)

            if (
                    adjacent_node_name != 'Wall' and
                    adjacent_node_name not in self.state.visited and
                    adjacent_node_name not in self.state.safeUnvisited and
                    self.KB.check(['W' + adjacent_node_name]) and
                    self.KB.check(['P' + adjacent_node_name])
            ):
                self.state.safeUnvisited.append(adjacent_node_name)

    def killWumpus(self, direction):
        self.killingWumpus = True
        self.move = []
        target_direction = str(get_keys_by_value(directions, direction.lower()))
        index = target_direction.find(':')
        dot_index = target_direction.find('.')
        direction = target_direction[dot_index + 1:index]
        target_direction = getattr(Action, direction)

        if self.agent.currDirection != target_direction:
            self.agent.currDirection = target_direction
            self.move.insert(0, Action.SHOOT)
            self.move.insert(0, target_direction)
        else:
            self.move.insert(0, Action.SHOOT)

    def handleWumpus(self, current_node):
        row = current_node.row
        col = current_node.col
        if current_node.up != "Wall":
            if (self.KB.check(["W" + str(row) + "," + str(col - 1)])
                    and self.KB.check(["~S" + str(row - 1) + "," + str(col - 1)])
                    or self.KB.check(["W" + str(row) + "," + str(col + 1)])
                    and self.KB.check(["~S" + str(row - 1) + "," + str(col + 1)])):
                self.killWumpus("Up")
        if current_node.left != "Wall":
            if (self.KB.check(["W" + str(row - 1) + "," + str(col)])
                    and self.KB.check(["~S" + str(row - 1) + "," + str(col - 1)])
                    or self.KB.check(["W" + str(row + 1) + "," + str(col)])
                    and self.KB.check(["~S" + str(row + 1) + "," + str(col - 1)])):
                self.killWumpus("Left")
        if current_node.down != "Wall":
            if (self.KB.check(["W" + str(row) + "," + str(col - 1)])
                    and self.KB.check(["~S" + str(row + 1) + "," + str(col - 1)])
                    or self.KB.check(["W" + str(row) + "," + str(col + 1)])
                    and self.KB.check(["~S" + str(row + 1) + "," + str(col + 1)])):
                self.killWumpus("Down")
        if current_node.right != "Wall":
            if (self.KB.check(["W" + str(row - 1) + "," + str(col)])
                    and self.KB.check(["~S" + str(row - 1) + "," + str(col + 1)])
                    or self.KB.check(["W" + str(row + 1) + "," + str(col)])
                    and self.KB.check(["~S" + str(row + 1) + "," + str(col + 1)])):
                self.killWumpus("Right")



    def moveList(self, path):
        direction = self.agent.currDirection
        state = self.agent.currPos
        current_node = self.state.state[state]
        move_list = []
        for item in path:
            row, col = item.split(',')
            new_state = WumpusNode(int(row), int(col), self.world)
            self.state.addState(new_state)

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
def get_keys_by_value(dictionary, value):
    return [key for key, val in dictionary.items() if val == value]