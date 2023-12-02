import numpy as np
from logic import Piece, Board, rotate, move_left2, move_right2, drop_down2

def get_mse(arr):
    mean = np.mean(arr)
    sum_squared_error = 0
    for num in arr:
        sum_squared_error += (num - mean) ** 2
    return sum_squared_error / len(arr)

def get_squareness_and_holes(board_state):
    heights = [0] * len(board_state[0])
    holes = 0
    columns_found = set()
    for i in range(len(board_state)):
        for j in range(len(board_state[i])):
            if board_state[i][j] is not None and j not in columns_found:
                heights[j] = len(board_state) - i
                columns_found.add(j)
            elif board_state[i][j] is None and j in columns_found:
                holes += 1
    heights.remove(min(heights))

    return {"holes": holes, 'mse': get_mse(heights), 'heights': heights}

# We need many copies bc we don't want to modify original objects
def possible_moves(piece, board):
    possible_states = {}
    for rotation in range(4):
        for direction in ['l', 'r']:
            offset = 0
            piece_copy = Piece(board.rows, board.cols, piece.name)
            while piece_copy.rotation != rotation:
                rotate(piece_copy, board)
            for i in range(10):
                offset += 1
                piece_copy2 = Piece(board.rows, board.cols, piece.name)
                piece_copy2.position = piece_copy.position
                board_copy = Board()
                for i, row in enumerate(board_copy.state):
                    for j, col in enumerate(row):
                        board_copy.state[i][j] = board.state[i][j]
                new_state = drop_down2(piece_copy2, piece_copy, board_copy)[2].state
                possible_states[(rotation, direction, offset)] = new_state
                if direction == 'l':
                    move_left2(piece_copy, board)
                else:
                    move_right2(piece_copy, board)
    return possible_states