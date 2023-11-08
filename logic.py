from hueristics import get_squareness_and_holes

board_rows, board_cols = 20, 10
BLOCK_SIZE = 30

class Board:
    def __init__(self, rows=20, cols=10):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.state = [[None for i in range(cols)] for j in range(rows)]

    def find_full_rows(self):
        num_lines = 0
        lines_to_clear = []
        for i, row in enumerate(self.state):
            if None not in row:
                num_lines += 1
                lines_to_clear.append(i)
                if num_lines == 4: break
        return lines_to_clear
    
    # Currently O(N^2), but probably can reduce to linear
    def clear_lines(self, lines_to_clear):
        for index in lines_to_clear:
            self.state[index] = [None for i in range(self.cols)]
            for j in range(index, -1, -1):
                if j == 0:
                    self.state[j] = [None for x in range(self.cols)]
                else:
                    self.state[j] = self.state[j-1]

    def update(self):
        rows_to_clear = self.find_full_rows()
        self.clear_lines(rows_to_clear)
        for block in self.state[0]:
            if block is not None:
                return False
        self.score += score_increases[len(rows_to_clear)]
        return True
    
    def is_legal_position(self, piece):
        for block in piece:
            if block[0] < 0: continue
            if (block[1] < 0 or block[1] >= self.cols or block[0] >= self.rows
                or self.state[block[0]][block[1]] != None):
                return False
        return True
    
    def place_piece(self, piece):
        for block in piece.position:
            self.state[block[0]][block[1]] = piece.color
        
            
class Piece:
    def __init__(self, board_rows, board_cols, name):
        self.board_rows = board_rows
        self.board_cols = board_cols
        self.name = name
        self.rotation = 0
        self.position = initial_positions[name]
        self.color = colors[name]
    
    # We cannot directly change the values of the piece object yet
    # because we do not know if the rotation is valid.
    # Same holds for move function
    def rotate(self):
        new_rotation = (self.rotation + 1) % 4
        adjust = rotations[self.name][new_rotation]
        new_position = [[x[0], x[1]] for x in self.position]
        for i, block in enumerate(new_position):
            block[0] += adjust[i][0]
            block[1] += adjust[i][1]
        return new_position
    
    def move(self, direction):
        movements = {'l': [0, -1], 'r': [0, 1], 'd': [1, 0], 'u': [-1, 0]}
        adjust = movements[direction]
        new_position = [[x[0], x[1]] for x in self.position]
        for block in new_position:
            block[0] += adjust[0]
            block[1] += adjust[1]
        return new_position

initial_positions = {
    'line': [[-1, board_cols//2 - 2], [-1, board_cols//2 - 1],
                [-1, board_cols//2], [-1, board_cols//2 + 1]],
    'square': [[-2, board_cols//2 - 1], [-2, board_cols//2],
                [-1, board_cols//2 - 1], [-1, board_cols//2]],
    't': [[-2, board_cols//2], [-1, board_cols//2 - 1],
            [-1, board_cols//2], [-1, board_cols//2 + 1]],
    'l': [[-2, board_cols//2 + 1], [-1, board_cols//2 -1],
            [-1, board_cols//2], [-1, board_cols//2 + 1]],
    'reverse_l': [[-2, board_cols//2 - 1], [-1, board_cols//2 -1],
                    [-1, board_cols//2], [-1, board_cols//2 + 1]],
    'z': [[-2, board_cols//2 - 1], [-2, board_cols//2],
            [-1, board_cols//2], [-1, board_cols//2 + 1]],
    'reverse_z': [[-1, board_cols//2 - 1], [-2, board_cols//2],
            [-1, board_cols//2], [-2, board_cols//2 + 1]]
}

colors = {
    'line': 'cyan',
    'square': 'yellow',
    't': 'purple',
    'l': 'orange',
    'reverse_l': 'pink',
    'z': 'red',
    'reverse_z': 'green'
}

# There is not closed formula for rotating a piece,
# as they all rotate in different ways, so these dicts
# represent the changes in position for each block from
# the previous rotation pattern.  The first number is the change
# of row and the second is the change of column.  We can use these to simply
# add to each of the blocks positions to obtain the rotated position.
line_rotations = {1: [[-1, 2], [0, 1], [1, 0], [2, -1]],
                2: [[2, 1], [1, 0], [0, -1], [-1, -2]],
                3: [[1, -2], [0, -1], [-1, 0], [-2, 1]],
                0: [[-2, -1], [-1, 0], [0, 1], [1, 2]]
}

square_rotations = {1: [[0, 0] for i in range(4)],
                    2: [[0, 0] for i in range(4)],
                    3: [[0, 0] for i in range(4)],
                    0: [[0, 0] for i in range(4)]
}

t_rotations = {1: [[1, 1], [-1, 1], [0, 0], [1, -1]],
                2: [[1, -1], [1, 1], [0, 0], [-1, -1]],
                3: [[-1, -1], [1, -1], [0, 0], [-1, 1]],
                0: [[-1, 1], [-1, -1], [0, 0], [1, 1]]
}


l_rotations = {1: [[2, 0], [-1, 1], [0, 0], [1, -1]],
                2: [[0, -2], [1, 1], [0, 0], [-1, -1]],
                3: [[-2, 0], [1, -1], [0, 0], [-1, 1]],
                0: [[0, 2], [-1, -1], [0, 0], [1, 1]]
}

reverse_l_rotations = {1: [[0, 2], [-1, 1], [0, 0], [1, -1]],
                        2: [[2, 0], [1, 1], [0, 0], [-1, -1]],
                        3: [[0, -2], [1, -1], [0, 0], [-1, 1]],
                        0: [[-2, 0], [-1, -1], [0, 0], [1, 1]]
}

z_rotations = {1: [[0, 2], [1, 1], [0, 0], [1, -1]],
                2: [[2, 0], [1, -1], [0, 0], [-1, -1]],
                3: [[0, -2], [-1, -1], [0, 0], [-1, 1]],
                0: [[-2, 0], [-1, 1], [0, 0], [1, 1]]
}

reverse_z_rotations = {1: [[-1, 1], [1, 1], [0, 0], [2, 0]],
                        2: [[1, 1], [1, -1], [0, 0], [0, -2]],
                        3: [[1, -1], [-1, -1], [0, 0], [-2, 0]],
                        0: [[-1, -1], [-1, 1], [0, 0], [0, 2]]
}

rotations = {'line': line_rotations,
            'square': square_rotations,
            't': t_rotations,
            'l': l_rotations,
            'reverse_l': reverse_l_rotations,
            'z': z_rotations,
            'reverse_z': reverse_z_rotations
}

score_increases = {0:0, 1: 800, 2: 1200, 3: 1800, 4: 2000}

def convert_cords(cords):
    return [cords[0] * BLOCK_SIZE, cords[1] * BLOCK_SIZE]

pieces = ['line', 'square', 't', 'l', 'reverse_l', 'z', 'reverse_z']
