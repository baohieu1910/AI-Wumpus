class WumpusNode():
    def __init__(self, row, col, world):
        self.name = str(row) + ',' + str(col)
        self.row = row
        self.col = col
        self.adjacents = world.getAdjacents(row, col)

        self.up = ''
        self.left = ''
        self.down = ''
        self.right = ''

        for adjacent in self.adjacents:
            if adjacent[0] == row - 1:
                self.up = str(adjacent[0]) + ',' + str(adjacent[1])
            elif adjacent[0] == row + 1:
                self.down = str(adjacent[0]) + ',' + str(adjacent[1])
            elif adjacent[1] == col + 1:
                self.right = str(adjacent[0]) + ',' + str(adjacent[1])
            elif adjacent[1] == col - 1:
                self.left = str(adjacent[0]) + ',' + str(adjacent[1])
