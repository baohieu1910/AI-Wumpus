import world, tile, controller
from tkinter import *
from tkinter import font
from tkinter import scrolledtext
import time

import agent
from WumpusNode import WumpusNode
from constants import *
from AgentBrain import AgentBrain
DELAY = 10

class Board:
    def __init__(self, world):
        self.root = Tk()
        self.root.title("WUMPUS WORLD")
        self.root.geometry("+200+50")

        self.canvas = Canvas(self.root, width=64 * world.width, height=64 * world.height + 64, background='white')
        self.outputFrame = Frame(self.root)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.outputFrame.pack(side="right", fill="both", expand=False)
        
        # KB and Action
        self.KBArea = None
        self.actionArea = None
        self.buttonStep = None
        self.buttonRun = None
        self.buttonFont = font.Font(size=10)

        self.runMode = -1

        self.world = world

        self.tiles = []
        self.objects = []
        self.warnings = []
        self.terrains = []
        self.player = None
        self.display_score = None
        self.scoreFont = font.Font(family='KacstBook', size=22)

        # Load images
        self.DOOR = PhotoImage(file=DOOR)
        self.TILE = PhotoImage(file=TILE)
        self.GOLD_TILE = PhotoImage(file=GOLD_TILE)
        self.WUMPUS = PhotoImage(file=WUMPUS)
        self.GOLD = PhotoImage(file=GOLD)
        self.BREEZE = PhotoImage(file=BREEZE)
        self.STENCH = PhotoImage(file=STENCH)
        self.PIT = PhotoImage(file=PIT)
        self.TERRAIN = PhotoImage(file=TERRAIN)
        self.PLAYER_DOWN = PhotoImage(file=PLAYER_DOWN)
        self.PLAYER_UP = PhotoImage(file=PLAYER_UP)
        self.PLAYER_LEFT = PhotoImage(file=PLAYER_LEFT)
        self.PLAYER_RIGHT = PhotoImage(file=PLAYER_RIGHT)
        self.ARROW_DOWN = PhotoImage(file=ARROW_DOWN)
        self.ARROW_UP = PhotoImage(file=ARROW_UP)
        self.ARROW_LEFT = PhotoImage(file=ARROW_LEFT)
        self.ARROW_RIGHT = PhotoImage(file=ARROW_RIGHT)
        self.SCORE = PhotoImage(file=SCORE)

        # Game state
        self.gameState = NOT_RUNNING

        self.agent = None # PL agent
        self.agentPos = None

        # Score
        self.score = 0


    ############################# CREATE WORLD #############################

    def createWorld(self):
        for i in range(self.world.height):
            tiles_line = []
            for j in range(self.world.width):
                tiles_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.TILE, anchor=NW))
            self.tiles.append(tiles_line)


        self.canvas.delete(self.tiles[self.world.doorPos[0]][self.world.doorPos[1]])
        self.tiles[self.world.doorPos[0]][self.world.doorPos[1]] = self.canvas.create_image(64 * self.world.doorPos[1], 64 * self.world.doorPos[0], image=self.DOOR, anchor=NW)


        for i in range(self.world.height):
            objects_line = []
            for j in range(self.world.width):
                tile_at_loc = self.world.listTiles[i][j]
                if tile_at_loc.getPit():
                    objects_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.PIT, anchor=NW))
                elif tile_at_loc.getWumpus():
                    objects_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.WUMPUS, anchor=NW))
                elif tile_at_loc.getGold():
                    self.canvas.delete(self.tiles[i][j])
                    self.tiles[i][j] = self.canvas.create_image(64 * j, 64 * i, image=self.GOLD_TILE, anchor=NW)
                    objects_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.GOLD, anchor=NW))
                else:
                    objects_line.append(None)
            self.objects.append(objects_line)


        warningFont = font.Font(family='Verdana', size=10)
        for i in range(self.world.height):
            warnings_line = []
            for j in range(self.world.width):
                warning_at_loc = []
                tile_at_loc = self.world.listTiles[i][j]
                first_cord = (i, j)
                if tile_at_loc.getBreeze():
                    warning_at_loc.append(self.canvas.create_image(64 * j, 64 * i, image=self.BREEZE, anchor=NW))
                else:
                    warning_at_loc.append(None)
                if tile_at_loc.getStench():
                    warning_at_loc.append(self.canvas.create_image(64 * j, 64 * i, image=self.STENCH, anchor=NW))
                else:
                    warning_at_loc.append(None)
                if not tile_at_loc.getBreeze() and not tile_at_loc.getStench():
                    warnings_line.append(None)
                else:
                    warnings_line.append(warning_at_loc)
            self.warnings.append(warnings_line)

        for i in range(self.world.height):
            terrains_line = []
            for j in range(self.world.width):
                tile_at_loc = self.world.listTiles[i][j]
                if tile_at_loc.getPlayer():
                    self.player = self.canvas.create_image(64 * j, 64 * i, image=self.PLAYER_RIGHT, anchor=NW)
                    self.agentPos = (i, j)
                    terrains_line.append(None)
                else:
                    terrains_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.TERRAIN, anchor=NW))
            self.terrains.append(terrains_line)

        # Init PL agent
        starting_node = WumpusNode(self.agentPos[0], self.agentPos[1], self.world)
        self.agent = AgentBrain(self.world, starting_node)

        self.canvas.create_rectangle(0, 64 * self.world.height, 64 * self.world.width, 64 * self.world.height + 64, fill='#85888a')
        self.canvas.create_image(64, 64 * self.world.height + 16, image=self.SCORE, anchor=NW)
        self.score_display = self.canvas.create_text(64 + 64, 64 * self.world.height + 16, fill='#ffff00', font=self.scoreFont, text=str(self.score), anchor=NW)


        # Output frame
        self.buttonStep = Button(self.outputFrame, text='STEP', height=2, width=30, command=lambda: self.changeRunMode(0))
        self.buttonRun = Button(self.outputFrame, text='RUN ALL', height=2, width=30, command=lambda: self.changeRunMode(1))
        self.buttonStep['font'] = self.buttonFont
        self.buttonRun['font'] = self.buttonFont

        self.actionArea = scrolledtext.ScrolledText(self.outputFrame, wrap=WORD, width=40, height=26, font=('Verdana', 15))

        self.buttonStep.grid(row=0, column=0)
        self.buttonRun.grid(row=0, column=1)
        self.actionArea.grid(row=1, column=0, columnspan=2)

    ############################# ACTIONS #############################
    
    def validPos(self, pos):
        return pos[0] >= 0 and pos[0] <= self.world.height - 1 and pos[1] >= 0 and pos[1] <= self.world.width - 1


    def moveForward(self, action): # action: current action
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
                self.canvas.delete(self.terrains[self.agentPos[0]][self.agentPos[1]])
                self.terrains[self.agentPos[0]][self.agentPos[1]] = None
            
            self.canvas.move(self.player, fixed_x, fixed_y)
            self.agent.currentState = action

            self.score -= 10
            self.canvas.itemconfig(self.score_display, text=str(self.score))

            tile_at_loc = self.world.listTiles[self.agentPos[0]][self.agentPos[1]]
            if tile_at_loc.getPit():
                self.score -= 10000
                self.canvas.itemconfig(self.score_display, text=str(self.score))
                self.canvas.update()
                time.sleep(0.5)
                self.endGame("Pit")
            elif tile_at_loc.getWumpus():
                self.score -= 10000
                self.canvas.itemconfig(self.score_display, text=str(self.score))
                self.canvas.update()
                time.sleep(0.5)
                self.endGame("Wumpus")


    def shootForward(self, direction): # direction: current state
        arrow = None
        arrow_loc = None
        if self.agent.currentState == Action.LEFT:
            arrow_loc = (self.agentPos[0], self.agentPos[1] - 1)
            arrow = self.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0], image=self.ARROW_LEFT, anchor=NW)
        elif self.agent.currentState == Action.RIGHT:
            arrow_loc = (self.agentPos[0], self.agentPos[1] + 1)
            arrow = self.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0], image=self.ARROW_RIGHT, anchor=NW)
        elif self.agent.currentState == Action.UP:
            arrow_loc = (self.agentPos[0] - 1, self.agentPos[1])
            arrow = self.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0], image=self.ARROW_UP, anchor=NW)
        elif self.agent.currentState == Action.DOWN:
            arrow_loc = (self.agentPos[0] + 1, self.agentPos[1])
            arrow = self.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0], image=self.ARROW_DOWN, anchor=NW)

        self.canvas.update()
        time.sleep(0.5)
        self.canvas.delete(arrow)

        self.score -= 100
        self.canvas.itemconfig(self.score_display, text=str(self.score))


        if self.world.listTiles[arrow_loc[0]][arrow_loc[1]].getWumpus():
            self.agent.scream = True
            # UPDATE WORLD
            self.world.killWumpus(arrow_loc[0], arrow_loc[1])

            # UPDATE BOARD
            if self.terrains[arrow_loc[0]][arrow_loc[1]]:
                self.canvas.delete(self.terrains[arrow_loc[0]][arrow_loc[1]])
                self.terrains[arrow_loc[0]][arrow_loc[1]] = None
                
            self.canvas.delete(self.objects[arrow_loc[0]][arrow_loc[1]])
            self.objects[arrow_loc[0]][arrow_loc[1]] = None

            adj = self.world.get_Adjacents(arrow_loc[0], arrow_loc[1])
            for a in adj:
                if not self.world.listTiles[a[0]][a[1]].getStench():
                    self.canvas.delete(self.warnings[a[0]][a[1]][1])
                    self.warnings[a[0]][a[1]][1] = None

            # END GAME ?
            if not self.world.leftWumpus() and not self.world.leftGold():
                self.actionArea.insert(END, 'ACTION: Clear map\n')
                self.endGame("Clear")


    def grabGold(self):
        if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getGold():
            self.score += 100
            self.canvas.itemconfig(self.score_display, text=str(self.score))

            # UPDATE WORLD
            self.world.grabGold(self.agentPos[0], self.agentPos[1])

            # UPDATE BOARD
            self.canvas.delete(self.objects[self.agentPos[0]][self.agentPos[1]])
            self.objects[self.agentPos[0]][self.agentPos[1]] = None

            self.canvas.delete(self.tiles[self.agentPos[0]][self.agentPos[1]])
            self.tiles[self.agentPos[0]][self.agentPos[1]] = self.canvas.create_image(64 * self.agentPos[1], 64 * self.agentPos[0], image=self.TILE, anchor=NW)

                # Overlapping handle            
            if self.warnings[self.agentPos[0]][self.agentPos[1]]:
                if (self.warnings[self.agentPos[0]][self.agentPos[1]])[0]:
                    self.canvas.tag_raise(self.warnings[self.agentPos[0]][self.agentPos[1]][0], self.tiles[self.agentPos[0]][self.agentPos[1]])
                if (self.warnings[self.agentPos[0]][self.agentPos[1]])[1]:
                    self.canvas.tag_raise(self.warnings[self.agentPos[0]][self.agentPos[1]][1], self.tiles[self.agentPos[0]][self.agentPos[1]])
            self.canvas.tag_raise(self.player, self.tiles[self.agentPos[0]][self.agentPos[1]])

            if not self.world.leftWumpus() and not self.world.leftGold():
                self.actionArea.insert(END, 'ACTION: Clear map\n')
                self.endGame("Clear")


    def endGame(self, reason):
        self.gameState = NOT_RUNNING
        for i in range(self.world.height):
            for j in range(self.world.width):
                if self.terrains[i][j]:
                    self.canvas.delete(self.terrains[i][j])
        self.buttonRun['state'] = DISABLED
        self.buttonStep['state'] = DISABLED


    def senseObject(self):
        if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getStench() and self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getBreeze():
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
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_DOWN)
                        self.actionArea.insert(END, 'ACTION: Face down\n')
                        self.agent.currentState = Action.DOWN
                elif action == Action.UP:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_UP)
                        self.actionArea.insert(END, 'ACTION: Face up\n')
                        self.agent.currentState = Action.UP
                elif action == Action.LEFT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_LEFT)
                        self.actionArea.insert(END, 'ACTION: Face left\n')
                        self.agent.currentState = Action.LEFT
                elif action == Action.RIGHT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_RIGHT)
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
                        self.canvas.itemconfig(self.score_display, text=str(self.score))
                        self.endGame("Climb")
                
                # self.senseObject()
                self.actionArea.see(END)
                self.root.update()
                self.root.after(DELAY)

            self.root.mainloop()

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
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_DOWN)
                        self.actionArea.insert(END, 'ACTION: Face down\n')
                        self.agent.currentState = Action.DOWN
                elif action == Action.UP:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_UP)
                        self.actionArea.insert(END, 'ACTION: Face up\n')
                        self.agent.currentState = Action.UP
                elif action == Action.LEFT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_LEFT)
                        self.actionArea.insert(END, 'ACTION: Face left\n')
                        self.agent.currentState = Action.LEFT
                elif action == Action.RIGHT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_RIGHT)
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
                        self.canvas.itemconfig(self.score_display, text=str(self.score))
                        self.endGame("Climb")
                
                # self.senseObject()
                self.actionArea.see(END)
                self.root.update()
                self.root.after(DELAY)

            self.root.mainloop()

        else:
            self.root.mainloop()