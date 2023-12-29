import World, Tile
from tkinter import *
from tkinter import font
from tkinter import scrolledtext
import time
from Graphics import Graphics
import Agent
from WumpusNode import WumpusNode
from Constants import *
from AgentBrain import AgentBrain

DELAY = 10


class Board:
    def __init__(self, world):

        self.graphic = Graphics(world)
        self.actionArea = None
        self.buttonStep = None
        self.buttonRun = None
        self.buttonFont = font.Font(size=10)
        self.scoreFont = font.Font(family='KacstBook', size=22)

        self.runMode = -1

        self.world = world

        self.tiles = []
        self.objects = []
        self.warnings = []
        self.terrains = []
        self.player = None
        # Game state
        self.gameState = NOT_RUNNING

        self.agent = None
        self.agentPos = None

        # Score
        self.score = 0

    def createWorld(self):
        for i in range(self.world.height):
            tilesRow = []
            for j in range(self.world.width):
                tilesRow.append(self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.TILE, anchor=NW))
            self.tiles.append(tilesRow)

        self.graphic.canvas.delete(self.tiles[self.world.doorPos[0]][self.world.doorPos[1]])
        self.tiles[self.world.doorPos[0]][self.world.doorPos[1]] = self.graphic.canvas.create_image(
            64 * self.world.doorPos[1], 64 * self.world.doorPos[0], image=self.graphic.DOOR, anchor=NW)

        for i in range(self.world.height):
            cellRows = []
            for j in range(self.world.width):
                locOfCell = self.world.listTiles[i][j]
                if locOfCell.getPit():
                    cellRows.append(self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.PIT, anchor=NW))
                elif locOfCell.getWumpus():
                    cellRows.append(self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.WUMPUS, anchor=NW))
                elif locOfCell.getGold():
                    self.graphic.canvas.delete(self.tiles[i][j])
                    self.tiles[i][j] = self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.GOLD_TILE, anchor=NW)
                    cellRows.append(self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.GOLD, anchor=NW))
                else:
                    cellRows.append(None)
            self.objects.append(cellRows)

        for i in range(self.world.height):
            warningRows = []
            for j in range(self.world.width):
                locOfWarning = []
                locOfCell = self.world.listTiles[i][j]
                if locOfCell.getBreeze():
                    locOfWarning.append(self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.BREEZE, anchor=NW))
                else:
                    locOfWarning.append(None)
                if locOfCell.getStench():
                    locOfWarning.append(self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.STENCH, anchor=NW))
                else:
                    locOfWarning.append(None)
                if not locOfCell.getBreeze() and not locOfCell.getStench():
                    warningRows.append(None)
                else:
                    warningRows.append(locOfWarning)
            self.warnings.append(warningRows)

        for i in range(self.world.height):
            terrainRows = []
            for j in range(self.world.width):
                locOfCell = self.world.listTiles[i][j]
                if locOfCell.getPlayer():
                    self.player = self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.PLAYER_RIGHT, anchor=NW)
                    self.agentPos = (i, j)
                    terrainRows.append(None)
                else:
                    terrainRows.append(self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.TERRAIN, anchor=NW))
            self.terrains.append(terrainRows)

        # Init PL agent
        initNode = WumpusNode(self.agentPos[0], self.agentPos[1], self.world)
        self.agent = AgentBrain(self.world, initNode)

        self.graphic.canvas.create_rectangle(0, 64 * self.world.height, 64 * self.world.width,
                                             64 * self.world.height + 64, fill='#85888a')
        self.graphic.canvas.create_image(64, 64 * self.world.height + 16, image=self.graphic.SCORE, anchor=NW)
        self.graphic.displayScore = self.graphic.canvas.create_text(64 + 64, 64 * self.world.height + 16, fill='#ffff00',
                                                            font=self.scoreFont, text=str(self.score), anchor=NW)

        # Output frame
        self.buttonStep = Button(self.graphic.outputFrame, text='STEP', height=2, width=30,
                                 command=lambda: self.changeRunMode(0))
        self.buttonRun = Button(self.graphic.outputFrame, text='RUN ALL', height=2, width=30,
                                command=lambda: self.changeRunMode(1))
        self.buttonStep['font'] = self.buttonFont
        self.buttonRun['font'] = self.buttonFont

        self.actionArea = scrolledtext.ScrolledText(self.graphic.outputFrame, wrap=WORD, width=40, height=26,
                                                    font=('Verdana', 15))

        self.buttonStep.grid(row=0, column=0)
        self.buttonRun.grid(row=0, column=1)
        self.actionArea.grid(row=1, column=0, columnspan=2)

    ############################# ACTIONS #############################

    def validPos(self, pos):
        return pos[0] >= 0 and pos[0] <= self.world.height - 1 and pos[1] >= 0 and pos[1] <= self.world.width - 1

    def moveForward(self, action):  # action: current action
        nextPos = None
        fixed_x = 0
        fixed_y = 0

        if action == Action.LEFT:
            nextPos = (self.agentPos[0], self.agentPos[1] - 1)
            fixed_x = -64
        elif action == Action.RIGHT:
            nextPos = (self.agentPos[0], self.agentPos[1] + 1)
            fixed_x = 64
        elif action == Action.UP:
            nextPos = (self.agentPos[0] - 1, self.agentPos[1])
            fixed_y = -64
        elif action == Action.DOWN:
            nextPos = (self.agentPos[0] + 1, self.agentPos[1])
            fixed_y = 64

        if self.validPos(nextPos):
            self.world.movePlayer(self.agentPos[0], self.agentPos[1], nextPos[0], nextPos[1])
            self.agentPos = nextPos

            if self.terrains[self.agentPos[0]][self.agentPos[1]]:
                self.graphic.canvas.delete(self.terrains[self.agentPos[0]][self.agentPos[1]])
                self.terrains[self.agentPos[0]][self.agentPos[1]] = None

            self.graphic.canvas.move(self.player, fixed_x, fixed_y)
            self.agent.currentState = action

            self.score -= 10
            self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))

            tile_at_loc = self.world.listTiles[self.agentPos[0]][self.agentPos[1]]
            if tile_at_loc.getPit():
                self.score -= 10000
                self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))
                self.graphic.canvas.update()
                time.sleep(0.5)
                self.endGame("Pit")
            elif tile_at_loc.getWumpus():
                self.score -= 10000
                self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))
                self.graphic.canvas.update()
                time.sleep(0.5)
                self.endGame("Wumpus")

    def shootForward(self, direction):  # direction: current state
        arrow = None
        arrow_loc = None
        if self.agent.currentState == Action.LEFT:
            arrow_loc = (self.agentPos[0], self.agentPos[1] - 1)
            arrow = self.graphic.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0],
                                                     image=self.graphic.ARROW_LEFT, anchor=NW)
        elif self.agent.currentState == Action.RIGHT:
            arrow_loc = (self.agentPos[0], self.agentPos[1] + 1)
            arrow = self.graphic.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0],
                                                     image=self.graphic.ARROW_RIGHT, anchor=NW)
        elif self.agent.currentState == Action.UP:
            arrow_loc = (self.agentPos[0] - 1, self.agentPos[1])
            arrow = self.graphic.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0], image=self.graphic.ARROW_UP,
                                                     anchor=NW)
        elif self.agent.currentState == Action.DOWN:
            arrow_loc = (self.agentPos[0] + 1, self.agentPos[1])
            arrow = self.graphic.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0],
                                                     image=self.graphic.ARROW_DOWN, anchor=NW)

        self.graphic.canvas.update()
        time.sleep(0.5)
        self.graphic.canvas.delete(arrow)

        self.score -= 100
        self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))

        if self.world.listTiles[arrow_loc[0]][arrow_loc[1]].getWumpus():
            self.agent.scream = True
            # UPDATE WORLD
            self.world.killWumpus(arrow_loc[0], arrow_loc[1])

            # UPDATE BOARD
            if self.terrains[arrow_loc[0]][arrow_loc[1]]:
                self.graphic.canvas.delete(self.terrains[arrow_loc[0]][arrow_loc[1]])
                self.terrains[arrow_loc[0]][arrow_loc[1]] = None

            self.graphic.canvas.delete(self.objects[arrow_loc[0]][arrow_loc[1]])
            self.objects[arrow_loc[0]][arrow_loc[1]] = None

            adj = self.world.getAdjacents(arrow_loc[0], arrow_loc[1])
            for a in adj:
                if not self.world.listTiles[a[0]][a[1]].getStench():
                    self.graphic.canvas.delete(self.warnings[a[0]][a[1]][1])
                    self.warnings[a[0]][a[1]][1] = None

            # END GAME ?
            if not self.world.leftWumpus() and not self.world.leftGold():
                self.actionArea.insert(END, 'ACTION: Clear map\n')
                self.endGame("Clear")

    def grabGold(self):
        if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getGold():
            self.score += 100
            self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))

            # UPDATE WORLD
            self.world.grabGold(self.agentPos[0], self.agentPos[1])

            # UPDATE BOARD
            self.graphic.canvas.delete(self.objects[self.agentPos[0]][self.agentPos[1]])
            self.objects[self.agentPos[0]][self.agentPos[1]] = None

            self.graphic.canvas.delete(self.tiles[self.agentPos[0]][self.agentPos[1]])
            self.tiles[self.agentPos[0]][self.agentPos[1]] = self.graphic.canvas.create_image(64 * self.agentPos[1],
                                                                                              64 * self.agentPos[0],
                                                                                              image=self.graphic.TILE,
                                                                                              anchor=NW)

            # Overlapping handle
            if self.warnings[self.agentPos[0]][self.agentPos[1]]:
                if (self.warnings[self.agentPos[0]][self.agentPos[1]])[0]:
                    self.graphic.canvas.tag_raise(self.warnings[self.agentPos[0]][self.agentPos[1]][0],
                                                  self.tiles[self.agentPos[0]][self.agentPos[1]])
                if (self.warnings[self.agentPos[0]][self.agentPos[1]])[1]:
                    self.graphic.canvas.tag_raise(self.warnings[self.agentPos[0]][self.agentPos[1]][1],
                                                  self.tiles[self.agentPos[0]][self.agentPos[1]])
            self.graphic.canvas.tag_raise(self.player, self.tiles[self.agentPos[0]][self.agentPos[1]])

            if not self.world.leftWumpus() and not self.world.leftGold():
                self.actionArea.insert(END, 'ACTION: Clear map\n')
                self.endGame("Clear")

    def endGame(self, reason):
        self.gameState = NOT_RUNNING
        for i in range(self.world.height):
            for j in range(self.world.width):
                if self.terrains[i][j]:
                    self.graphic.canvas.delete(self.terrains[i][j])
        self.buttonRun['state'] = DISABLED
        self.buttonStep['state'] = DISABLED

    def senseObject(self):
        if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getStench() and \
                self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getBreeze():
            self.actionArea.insert(END, 'SENSE: Stench, Breeze\n')
        else:
            if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getStench():
                self.actionArea.insert(END, 'SENSE: Stench\n')
            if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getBreeze():
                self.actionArea.insert(END, 'SENSE: Breeze\n')

    def changeRunMode(self, key):
        self.runMode = key
        self.run()

    def run(self):
        self.gameState = RUNNING

        if self.runMode == 1:
            while self.gameState == RUNNING:
                self.senseObject()
                self.actionArea.see(END)
                action = self.agent.getAction()
                if action == Action.DOWN:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_DOWN)
                        self.actionArea.insert(END, 'ACTION: Face down\n')
                        self.agent.currentState = Action.DOWN
                elif action == Action.UP:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_UP)
                        self.actionArea.insert(END, 'ACTION: Face up\n')
                        self.agent.currentState = Action.UP
                elif action == Action.LEFT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_LEFT)
                        self.actionArea.insert(END, 'ACTION: Face left\n')
                        self.agent.currentState = Action.LEFT
                elif action == Action.RIGHT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_RIGHT)
                        self.actionArea.insert(END, 'ACTION: Face right\n')
                        self.agent.currentState = Action.RIGHT
                elif action == Action.SHOOT:
                    self.actionArea.insert(END, 'ACTION: Shoot arrow\n')
                    self.shootForward(self.agent.currentState)
                elif action == Action.GRAB:
                    self.actionArea.insert(END, 'ACTION: Grab gold\n')
                    self.grabGold()
                elif action == Action.CLIMB:
                    self.actionArea.insert(END, 'ACTION: Climb out\n')
                    self.actionArea.see(END)
                    if self.agentPos == self.world.doorPos:
                        self.score += 10
                        self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))
                        self.endGame("Climb")

                # self.senseObject()
                self.actionArea.see(END)
                self.graphic.root.update()
                self.graphic.root.after(DELAY)

            self.graphic.root.mainloop()

        elif self.runMode == 0:
            if self.gameState == RUNNING:
                self.senseObject()
                self.actionArea.see(END)

                action = self.agent.getAction()

                if action == Action.DOWN:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_DOWN)
                        self.actionArea.insert(END, 'ACTION: Face down\n')
                        self.agent.currentState = Action.DOWN
                elif action == Action.UP:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_UP)
                        self.actionArea.insert(END, 'ACTION: Face up\n')
                        self.agent.currentState = Action.UP
                elif action == Action.LEFT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_LEFT)
                        self.actionArea.insert(END, 'ACTION: Face left\n')
                        self.agent.currentState = Action.LEFT
                elif action == Action.RIGHT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_RIGHT)
                        self.actionArea.insert(END, 'ACTION: Face right\n')
                        self.agent.currentState = Action.RIGHT
                elif action == Action.SHOOT:
                    self.actionArea.insert(END, 'ACTION: Shoot arrow\n')
                    self.shootForward(self.agent.currentState)
                elif action == Action.GRAB:
                    self.actionArea.insert(END, 'ACTION: Grab gold\n')
                    self.grabGold()
                elif action == Action.CLIMB:
                    self.actionArea.insert(END, 'ACTION: Climb out\n')
                    self.actionArea.see(END)
                    if self.agentPos == self.world.doorPos:
                        self.score += 10
                        self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))
                        self.endGame("Climb")

                # self.senseObject()
                self.actionArea.see(END)
                self.graphic.root.update()
                self.graphic.root.after(DELAY)

            self.graphic.root.mainloop()

        else:
            self.graphic.root.mainloop()