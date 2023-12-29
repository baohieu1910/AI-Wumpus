from Agent import Agent
from GameState import GameState
from KB import KnowledgeBase
from WumpusNode import WumpusNode
from Search import *


class AgentBrain():
    def __init__(self, world, initNode):
        self.state = GameState(world)
        self.state.add_state(WumpusNode(initNode.row, initNode.col, world))
        self.agent = Agent(initNode.name)
        self.KB = KnowledgeBase()
        self.KB.add(["~P" + str(initNode.name)])
        self.KB.add(["~W" + str(initNode.name)])
        self.exit = False
        self.move = []
        self.initNode = initNode
        self.world = world
        self.currentState = Action.RIGHT
        self.killedWumpus = False
        self.scream = False

    def getAction(self):
        currNode = self.state.state[self.agent.currPos]
        locTile = self.world.listTiles[currNode.row][currNode.col]

        if currNode.name in self.state.safeUnvisited:
            self.state.safeUnvisited.remove(currNode.name)

        if self.scream == True:
            if self.agent.currDirection == Action.UP:
                self.state.safeUnvisited.append(currNode.up)
                self.clearKB(currNode.up)
            elif self.agent.currDirection == Action.LEFT:
                self.state.safeUnvisited.append(currNode.left)
                self.clearKB(currNode.left)
            elif self.agent.currDirection == Action.DOWN:
                self.state.safeUnvisited.append(currNode.down)
                self.clearKB(currNode.down)
            elif self.agent.currDirection == Action.RIGHT:
                self.state.safeUnvisited.append(currNode.right)
                self.clearKB(currNode.right)
            self.scream = False

        for item in self.state.visited[-10:]:
            row, col = item.split(',')
            tile = self.world.listTiles[int(row)][int(col)]
            if not tile.getStench() and self.KB.check(["~S" + str(item)]):
                self.KB.KB.remove(['S' + item])

        if currNode.name == self.initNode.name and locTile.getBreeze():
            self.move.append(Action.CLIMB)

        if not self.exit and not self.killedWumpus:
            stench = False
            breeze = False
            if locTile.getStench():
                stench = True
                self.handleStench(currNode, stench)
                self.handleWumpus(currNode)
            elif not locTile.getStench():
                self.handleStench(currNode, stench)
            if locTile.getBreeze():
                breeze = True
                self.handleBreeze(currNode, breeze)
            elif not locTile.getBreeze():
                self.handleBreeze(currNode, breeze)
            self.addSafeNode(currNode)
            if locTile.getGold():
                return Action.GRAB
            if not self.killedWumpus:
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
                self.killedWumpus = False
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
        if breeze == True:
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
        else:
            prefix = '~P'
            if current_node.up not in self.state.visited and current_node.up != 'Wall':
                self.KB.add([prefix + current_node.up])
            if current_node.left not in self.state.visited and current_node.left != 'Wall':
                self.KB.add([prefix + current_node.left])
            if current_node.down not in self.state.visited and current_node.down != 'Wall':
                self.KB.add([prefix + current_node.down])
            if current_node.right not in self.state.visited and current_node.right != 'Wall':
                self.KB.add([prefix + current_node.right])

    def handleStench(self, current_node, stench):
        if stench == True:
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
        else:
            prefix = '~W'
            if current_node.right not in self.state.visited and current_node.right != 'Wall':
                self.KB.add([prefix + current_node.right])
            if current_node.up not in self.state.visited and current_node.up != 'Wall':
                self.KB.add([prefix + current_node.up])
            if current_node.left not in self.state.visited and current_node.left != 'Wall':
                self.KB.add([prefix + current_node.left])
            if current_node.down not in self.state.visited and current_node.down != 'Wall':
                self.KB.add([prefix + current_node.down])


    def addSafeNode(self, current_node):
        if current_node.up != 'Wall' and current_node.up not in self.state.visited and current_node.up not in self.state.safeUnvisited:
            if self.KB.check(['W' + current_node.up]) and self.KB.check(['P' + current_node.up]):
                self.state.safeUnvisited.append(current_node.up)
        if current_node.left != 'Wall' and current_node.left not in self.state.visited and current_node.left not in self.state.safeUnvisited:
            if self.KB.check(['W' + current_node.left]) and self.KB.check(['P' + current_node.left]):
                self.state.safeUnvisited.append(current_node.left)
        if current_node.down != 'Wall' and current_node.down not in self.state.visited and current_node.down not in self.state.safeUnvisited:
            if self.KB.check(['W' + current_node.down]) and self.KB.check(['P' + current_node.down]):
                self.state.safeUnvisited.append(current_node.down)
        if current_node.right != 'Wall' and current_node.right not in self.state.visited and current_node.right not in self.state.safeUnvisited:
            if self.KB.check(['W' + current_node.right]) and self.KB.check(['P' + current_node.right]):
                self.state.safeUnvisited.append(current_node.right)

    def killWumpus(self, direction):
        self.killedWumpus = True
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