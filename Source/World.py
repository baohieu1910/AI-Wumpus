from Tile import Tile
from random import randrange


class WumpusWorld:
    def __init__(self):
        """Initialize an empty board"""
        self.height = 0
        self.width = 0
        self.numGold = 0
        self.numWumpus = 0
        self.listTiles = []
        self.doorPos = None

    def getAdjacents(self, i, j):
        adj = []
        if i - 1 >= 0:
            adj.append((i - 1, j))
        if i + 1 <= self.height - 1:
            adj.append((i + 1, j))
        if j - 1 >= 0:
            adj.append((i, j - 1))
        if j + 1 <= self.width - 1:
            adj.append((i, j + 1))
        return adj

    def readMap(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.read().splitlines()
                lines = lines[1:]
                self.height = len(lines)

                tiles = []
                for line in lines:
                    tiles.append(line.split('.'))
                self.width = len(tiles[0])

                # Empty tiles map
                for i in range(self.height):
                    tile_line = []
                    for j in range(self.width):
                        tile_line.append(Tile())
                    self.listTiles.append(tile_line)

                # Tile's objects
                for i in range(self.height):
                    for j in range(self.width):
                        if 'A' in tiles[i][j]:
                            (self.listTiles[i][j]).setPlayer()
                            self.doorPos = (i, j)
                        if 'G' in tiles[i][j]:
                            (self.listTiles[i][j]).setGold()
                            self.numGold += 1
                        if 'P' in tiles[i][j]:
                            (self.listTiles[i][j]).setPit()
                            adj = self.getAdjacents(i, j)
                            for a in adj:
                                (self.listTiles[a[0]][a[1]]).setBreeze()
                        if 'W' in tiles[i][j]:
                            (self.listTiles[i][j]).setWumpus()
                            self.numWumpus += 1
                            adj = self.getAdjacents(i, j)
                            for a in adj:
                                (self.listTiles[a[0]][a[1]]).setStench()

        except IOError:
            return None

    def grabGold(self, i, j):
        self.numGold -= 1
        self.listTiles[i][j].removeGold()

    def killWumpus(self, i, j):
        self.numWumpus -= 1
        self.listTiles[i][j].removeWumpus()
        adj = self.getAdjacents(i, j)
        for a in adj:
            if self.listTiles[a[0]][a[1]].getStench():
                self.listTiles[a[0]][a[1]].removeStench()

    def movePlayer(self, before_i, before_j, after_i, after_j):
        self.listTiles[before_i][before_j].removePlayer()
        self.listTiles[after_i][after_j].setPlayer()

    def leftGold(self):
        return bool(self.numGold)

    def leftWumpus(self):
        return bool(self.numWumpus)
