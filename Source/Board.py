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
        self.scoreFont = font.Font(family='TimesNewRoman', size=22)

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

    def createCellRow(self):
        for i in range(self.world.row):
            cellRows = []
            for j in range(self.world.col):
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

    def createWarningRow(self):
        for i in range(self.world.row):
            warningRows = []
            for j in range(self.world.col):
                locOfWarning = []
                locOfCell = self.world.listTiles[i][j]
                if locOfCell.getBreeze():
                    locOfWarning.append(self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.BREEZE, anchor=NW))
                    print((64 * j, 64 * i))
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

    def createTerrainRow(self):
        for i in range(self.world.row):
            terrainRows = []
            for j in range(self.world.col):
                locOfCell = self.world.listTiles[i][j]
                if locOfCell.getPlayer():
                    self.player = self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.PLAYER_RIGHT, anchor=NW)
                    self.agentPos = (i, j)
                    terrainRows.append(None)
                else:
                    terrainRows.append(self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.TERRAIN, anchor=NW))
            self.terrains.append(terrainRows)

    def drawNote(self):
        notes = {self.graphic.GOLD: ": Gold",
                 self.graphic.BREEZE: ": Breeze",
                 self.graphic.PIT: ": Pit",
                 self.graphic.STENCH: ": Stench",
                 self.graphic.WUMPUS: ": Wumpus"}

        self.graphic.canvas.create_text(64 * 11 + 32, 64 * 0 + 16, fill='#FF0000', font=self.scoreFont, text="Note", anchor=NW)
        self.graphic.canvas.create_text(64 * 10, 64 * 0 + 16, fill='#FF0000', font=self.scoreFont, text="_________________", anchor=NW)

        for i in range(len(notes)):
            self.graphic.canvas.create_image(64 * 10 + 10, 64 * (i + 1), image=list(notes.keys())[i], anchor = NW)
            self.graphic.canvas.create_text(64 * 11 + 10, 64 * (i + 1) + 16, font=self.scoreFont, text=list(notes.values())[i], anchor=NW)

    def drawWorld(self):
        self.drawNote()

        for i in range(self.world.row):
            tilesRow = []
            for j in range(self.world.col):
                tilesRow.append(self.graphic.canvas.create_image(64 * j, 64 * i, image=self.graphic.TILE, anchor=NW))
            self.tiles.append(tilesRow)

        self.graphic.canvas.delete(self.tiles[self.world.doorPos[0]][self.world.doorPos[1]])
        self.tiles[self.world.doorPos[0]][self.world.doorPos[1]] = self.graphic.canvas.create_image(
            64 * self.world.doorPos[1], 64 * self.world.doorPos[0], image=self.graphic.DOOR, anchor=NW)

        self.createCellRow()
        self.createWarningRow()
        self.createTerrainRow()

        initNode = WumpusNode(self.agentPos[0], self.agentPos[1], self.world)
        self.agent = AgentBrain(self.world, initNode)

        self.graphic.canvas.create_rectangle(0, 64 * self.world.row, 64 * self.world.col,
                                             64 * self.world.row + 64, fill='#85888a')
        self.graphic.canvas.create_image(64, 64 * self.world.row + 16, image=self.graphic.SCORE, anchor=NW)
        self.graphic.displayScore = self.graphic.canvas.create_text(64 + 64, 64 * self.world.row + 16, fill='#ffff00',
                                                                    font=self.scoreFont, text=str(self.score), anchor=NW)

        # Output frame
        self.buttonStep = Button(self.graphic.outputFrame, text='RUN BY STEP', height=2, width=30,
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

    def validPos(self, pos):
        return pos[0] >= 0 and pos[0] <= self.world.row - 1 and pos[1] >= 0 and pos[1] <= self.world.col - 1

    def update_score(self, penalty):
        self.score -= penalty
        self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))

    def move_agent(self, x_change, y_change):
        next_pos = (self.agentPos[0] + x_change, self.agentPos[1] + y_change)
        fixed_x = y_change * 64
        fixed_y = x_change * 64
        return next_pos, fixed_x, fixed_y

    def moveForward(self, action):
        nextPos = None
        x = 0
        y = 0
        if action == Action.LEFT:
            nextPos = self.move_agent(0, -1)[0]
            x = self.move_agent(0, -1)[1]
        elif action == Action.RIGHT:
            nextPos= self.move_agent(0, 1)[0]
            x = self.move_agent(0, 1)[1]

        elif action == Action.UP:
            nextPos = self.move_agent(-1, 0)[0]
            y = self.move_agent(-1, 0)[2]
        elif action == Action.DOWN:
            nextPos = self.move_agent(1, 0)[0]
            y = self.move_agent(1, 0)[2]

        if self.validPos(nextPos):
            self.world.movePlayer(self.agentPos[0], self.agentPos[1], nextPos[0], nextPos[1])
            self.agentPos = nextPos
            if self.terrains[self.agentPos[0]][self.agentPos[1]]:
                self.graphic.canvas.delete(self.terrains[self.agentPos[0]][self.agentPos[1]])
                self.terrains[self.agentPos[0]][self.agentPos[1]] = None
            self.graphic.canvas.move(self.player, x, y)
            self.agent.currentState = action

            self.update_score(10)
            self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))

            tile_at_loc = self.world.listTiles[self.agentPos[0]][self.agentPos[1]]
            if tile_at_loc.getPit() or tile_at_loc.getWumpus():
                self.update_score(10000)
                self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))
                self.graphic.canvas.update()
                time.sleep(0.5)
                text = 'Pit' if tile_at_loc.getPit() else 'Wumpus'
                self.endGame(text)


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
        for i in range(self.world.row):
            for j in range(self.world.col):
                if self.terrains[i][j]:
                    self.graphic.canvas.delete(self.terrains[i][j])
        self.buttonRun['state'] = DISABLED
        self.buttonStep['state'] = DISABLED

    def senseObject(self):
        if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getStench() and \
                self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getBreeze():
            self.actionArea.insert(END, 'Warning: Stench, Breeze\n')
        else:
            if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getStench():
                self.actionArea.insert(END, 'Warning: Stench\n')
            if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getBreeze():
                self.actionArea.insert(END, 'Warning: Breeze\n')

    def changeRunMode(self, key):
        self.runMode = key
        self.runGame()

    def run(self):
        self.senseObject()
        self.actionArea.see(END)
        action = self.agent.getAction()
        if action == Action.DOWN:
            if action == self.agent.currentState:
                self.actionArea.insert(END, 'Action: Move forward\n')
                self.moveForward(action)
            else:
                self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_DOWN)
                self.actionArea.insert(END, 'Action: Face down\n')
                self.agent.currentState = Action.DOWN
        elif action == Action.UP:
            if action == self.agent.currentState:
                self.actionArea.insert(END, 'Action: Move forward\n')
                self.moveForward(action)
            else:
                self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_UP)
                self.actionArea.insert(END, 'Action: Face up\n')
                self.agent.currentState = Action.UP
        elif action == Action.LEFT:
            if action == self.agent.currentState:
                self.actionArea.insert(END, 'Action: Move forward\n')
                self.moveForward(action)
            else:
                self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_LEFT)
                self.actionArea.insert(END, 'Action: Face left\n')
                self.agent.currentState = Action.LEFT
        elif action == Action.RIGHT:
            if action == self.agent.currentState:
                self.actionArea.insert(END, 'Action: Move forward\n')
                self.moveForward(action)
            else:
                self.graphic.canvas.itemconfigure(self.player, image=self.graphic.PLAYER_RIGHT)
                self.actionArea.insert(END, 'Action: Face right\n')
                self.agent.currentState = Action.RIGHT
        elif action == Action.SHOOT:
            self.actionArea.insert(END, 'Action: Shoot arrow\n')
            self.shootForward(self.agent.currentState)
        elif action == Action.GRAB:
            self.actionArea.insert(END, 'Action: Grab gold\n')
            self.grabGold()
        elif action == Action.CLIMB:
            self.actionArea.insert(END, 'Action: Climb out\n')
            self.actionArea.see(END)
            if self.agentPos == self.world.doorPos:
                self.score += 10
                self.graphic.canvas.itemconfig(self.graphic.displayScore, text=str(self.score))
                self.endGame("Climb")

        self.actionArea.see(END)
        self.graphic.root.update()
        self.graphic.root.after(DELAY)


    def runGame(self):
        self.gameState = RUNNING

        if self.runMode == 1:
            while self.gameState == RUNNING:
                self.run()
            self.graphic.root.mainloop()

        elif self.runMode == 0:
            if self.gameState == RUNNING:
                self.run()
            self.graphic.root.mainloop()

        else:
            self.graphic.root.mainloop()