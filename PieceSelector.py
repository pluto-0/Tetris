import random

class Piece:
    def __init__(self, position, shape, index, color):
        self.shape = shape
        self.color = color
        self.index = index
        self.position = position

    def move_right(self, position, shape, index, color):
        self.position[0] += 30

    def move_left(self, position, shape, index, color):
        self.position[0] -= 30

    def move_down(self, position, shape, index, color):
        self.position[1] += 30

square_piece = Piece([0, 0], [[1, 1], [1, 1]], 0, [255, 0, 0])
long_piece = Piece([0, 0], [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], 0, [255, 128, 0])
L_piece = Piece([0, 0], [[1, 0, 0], [1, 0, 0], [1, 1, 0]], 0, [0, 0, 255])
reverse_L_piece = Piece([0, 0], [[0, 0, 1], [0, 0, 1], [0, 1, 1]], 0, [0, 204, 0])
Z_piece = Piece([0, 0], [[1, 1, 0], [0, 1, 1], [0, 0, 0]], 0, [0, 255, 255])
reverse_Z_piece = Piece([0, 0], [[0, 1, 1], [1, 1, 0], [0, 0, 0]], 0, [127, 0, 255])
T_piece = Piece([0, 0], [[0, 1, 0], [1, 1, 1], [0, 0, 0]], 0, [255, 255, 0])

def rotate(piece):
    if (piece == square_piece):
        piece.shape = piece.shape

    elif (piece == long_piece):
        if(piece.index == 3):
            piece.index = 0
        else: piece.index += 1

        if(piece.index == 0 or piece.index == 2):
            piece.shape = [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        elif(piece.index == 1 or piece.index == 3):
            piece.shape = [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]

    elif(piece == L_piece):
        if (piece.index == 3):
            piece.index = 0
        else: piece.index += 1

        if(piece.index == 0):
            piece.shape = [[1, 0, 0], [1, 0, 0], [1, 1, 0]]
        elif(piece.index == 1):
            piece.shape = [[0, 0, 0], [0, 0, 1], [1, 1, 1]]
        elif(piece.index == 2):
            piece.shape = [[1, 1, 0], [0, 1, 0], [0, 1, 0]]
        elif(piece.index == 3):
            piece.shape = [[0, 0, 0], [1, 1, 1], [1, 0, 0]]

    elif(piece == reverse_L_piece):
        if(piece.index == 3):
            piece.index = 0
        else: piece.index += 1

        if(piece.index == 0):
            piece.shape = [[0, 0, 1], [0, 0, 1], [0, 1, 1]]
        elif(piece.index == 1):
            piece.shape = [[0, 0, 0], [1, 1, 1], [0, 0, 1]]
        elif(piece.index == 2):
            piece.shape = [[0, 1, 1], [0, 1, 0], [0, 1, 0]]
        elif(piece.index == 3):
            piece.shape = [[0, 0, 0], [1, 0, 0], [1, 1, 1]]

    elif(piece == Z_piece):
        if(piece.index == 3):
            piece.index = 0
        else: piece.index += 1

        if(piece.index == 0 or piece.index == 2):
            piece.shape = [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
        elif(piece.index == 1 or piece.index == 3):
            piece.shape = [[0, 0, 1], [0, 1, 1], [0, 1, 0]]

    elif(piece == reverse_Z_piece):
        if(piece.index == 3):
            piece.index = 0
        else: piece.index += 1

        if(piece.index == 0 or piece.index == 2):
            piece.shape = [[0, 1, 1], [1, 1, 0], [0, 0, 0]]
        elif(piece.index == 1 or piece.index == 3):
            piece.shape = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]

    elif(piece == T_piece):
        if(piece.index == 3):
            piece.index = 0
        else: piece.index += 1

        if(piece.index == 0):
            piece.shape = [[0, 1, 0], [1, 1, 1], [0, 0, 0]]
        elif(piece.index == 1):
            piece.shape = [[0, 1, 0], [1, 1, 0], [0, 1, 0]]
        elif(piece.index == 2):
            piece.shape = [[0, 0, 0][1, 1, 1], [0, 1, 0]]
        elif(piece.index == 3):
            piece.shape = [[0, 1, 0], [0, 1, 1], [0, 1, 0]]

def selector():
    choice = random.randint(1, 7)

    if(choice == 1):
        return square_piece
    elif(choice == 2):
        return long_piece
    elif(choice == 3):
        return L_piece
    elif(choice == 4):
        return reverse_L_piece
    elif(choice == 5):
        return Z_piece
    elif(choice == 6):
        return reverse_Z_piece
    elif (choice == 7):
        return T_piece
