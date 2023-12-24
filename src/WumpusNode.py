class WumpusNode():
    def __init__(self, row, col, world):
        self.name = str(row) + ',' + str(col)
        self.row = row
        self.col = col
        adjacents = world.get_Adjacents(row,col)
        self.left = ''
        self.right = ''
        self.up = ''
        self.down = ''
        for adjacent in adjacents:
            if adjacent[0] == row - 1:
                self.up = str(adjacent[0]) + ',' + str(adjacent[1])
            elif adjacent[0] == row + 1:
                self.down = str(adjacent[0]) + ',' + str(adjacent[1])
            elif adjacent[1] == col + 1:
                self.right = str(adjacent[0]) + ',' + str(adjacent[1])
            elif adjacent[1] == col - 1:
                self.left = str(adjacent[0]) + ',' + str(adjacent[1])
