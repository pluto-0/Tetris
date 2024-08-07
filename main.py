import pygame
import random
import logic
from logic import Piece, Board, rotate, move_left, move_right, drop_down, make_random_piece, get_cpu_move, possible_moves, drop_down2, get_metrics
import pprint
from time import sleep
from collections import deque
from agent import Agent

BLOCK_SIZE = logic.BLOCK_SIZE
SCREEN_SIZE = (720, 1280)

'''
test_board = Board()
for i in range(3):
    test_board.state[17][i] = 'green'
test_piece = Piece(test_board.rows, test_board.cols, 'line')
pprint.pprint(possible_moves(test_piece, test_board))
'''

def main():
    player_type = input("Human or computer player? ")
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    board = logic.Board()
    board_screen = pygame.Surface((BLOCK_SIZE * board.cols, BLOCK_SIZE * board.rows))
    white_box = pygame.Rect(0, 0, BLOCK_SIZE * board.cols, BLOCK_SIZE * board.rows)
    piece = make_random_piece(board)
    next_piece = make_random_piece(board)
    score = pygame.font.SysFont(None,50)
    score_screen = score.render("SCORE = " + str(board.score), True, 'white')
    next_piece_screen = pygame.Surface((BLOCK_SIZE * 5, BLOCK_SIZE  * 5))
    next_piece_box = pygame.Rect(0, 0, BLOCK_SIZE * 5, BLOCK_SIZE * 5)
    pygame.draw.rect(next_piece_screen, 'white', next_piece_box, 1)
    frame = 0
    total_scores = []
    agent = Agent(board)
    cpu_moves = deque()
    moved_down = False
    running = True
    agent = Agent(board)

    while running:
        if player_type[0] == 'h':
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        piece, next_piece, board, moved_down = move_down(piece, next_piece, board, moved_down)
                    elif event.key == pygame.K_RIGHT:
                        move_right(piece, board)
                    elif event.key == pygame.K_LEFT:
                        move_left(piece, board)
                    elif event.key == pygame.K_UP:
                        rotate(piece, board)
                    elif event.key == pygame.K_SPACE:
                        piece, next_piece, board = drop_down(piece, next_piece, board)
                elif event.type == pygame.QUIT:
                    running = False
        else:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.QUIT:
                    running = False
            if not cpu_moves:
                rotation, direction, offset = get_cpu_move(piece, agent)
                neg_mod = {-1: 3, -2: 2, -3: 1}
                diff = rotation - piece.rotation
                if diff < 0:
                    diff = neg_mod[diff]
                for i in range(diff):
                    cpu_moves.append('rotate')
                for i in range(offset):
                    cpu_moves.append(direction)
                cpu_moves.append('drop')
            if frame % 2 == 0:
                next_move = cpu_moves.popleft()
                if next_move == 'rotate':
                    rotate(piece, board)
                elif next_move == 'l':
                    move_left(piece, board)
                elif next_move == 'r':
                    move_right(piece, board)
                else:
                    piece, next_piece, board = drop_down(piece, next_piece, board)
        if frame % 15 == 0:
            if not moved_down:
                piece, next_piece, board, moved_down = move_down(piece, next_piece, board, moved_down)
            moved_down = False

        screen.fill('black')
        board_screen.fill('black')
        next_piece_screen.fill('black')

        for block in piece.position:
            cords = logic.convert_cords(block)

            piece_block_object = pygame.Rect(cords[1], cords[0], BLOCK_SIZE-1, BLOCK_SIZE-1)
            pygame.draw.rect(board_screen, piece.color, piece_block_object)
        
        # Kind of reproducing code here, would be better to have a function that 
        # calculates drop down position, but I ran into issues with passing pieces
        # by reference
        ghost_piece = logic.Piece(board.rows, board.cols, piece.name)
        ghost_piece.position = piece.position
        new_position = ghost_piece.move('d')
        while board.is_legal_position(new_position):
            ghost_piece.position = new_position
            new_position = ghost_piece.move('d')
        
        for block in ghost_piece.position:
            cords = logic.convert_cords(block)
            ghost_block = pygame.Rect(cords[1], cords[0], BLOCK_SIZE-1, BLOCK_SIZE-1)
            pygame.draw.rect(board_screen, 'grey', ghost_block, 1)

        
        for block in next_piece.position:
            cords = [block[0] * BLOCK_SIZE + 90, block[1] * BLOCK_SIZE - 90]
            if next_piece.name == 'square':
                cords[1] += 15
                cords[0] += 15
            elif next_piece.name == 'line':
                cords[1] += 15
            next_piece_block = pygame.Rect(cords[1], cords[0], BLOCK_SIZE-1, BLOCK_SIZE-1)
            pygame.draw.rect(next_piece_screen, next_piece.color, next_piece_block)

        for i, row in enumerate(board.state):
            for j, column in enumerate(row):
                if column != None:
                    cords = logic.convert_cords([i, j])
                    board_block_object = pygame.Rect(cords[1], cords[0], BLOCK_SIZE-1, BLOCK_SIZE-1)
                    pygame.draw.rect(board_screen, column, board_block_object)
        
        score_screen.fill('black')
        score_screen = score.render("SCORE = " + str(board.score), True, 'white')
        screen.blit(score_screen, [20, 20])

        pygame.draw.rect(next_piece_screen, 'white', next_piece_box, 1)
        pygame.Surface.blit(screen, next_piece_screen, [SCREEN_SIZE[0] - 5 * BLOCK_SIZE, 0])

        pygame.draw.rect(board_screen, 'white', white_box, 1)
        pygame.Surface.blit(screen, board_screen, find_white_box_cords(board))
    
        pygame.display.flip()
        frame += 1
        clock.tick(60)
        


def find_white_box_cords(board):
    return ((SCREEN_SIZE[0] - (BLOCK_SIZE * board.cols)) // 2,
             (SCREEN_SIZE[1] - (BLOCK_SIZE * board.rows)) // 2)

def move_down(piece, next_piece, board, moved_down):
    new_position = piece.move('d')
    if board.is_legal_position(new_position):
        moved_down = True
        piece.position = new_position
    else:
        board.place_piece(piece)
        if not board.update():
            board.reset()
        new_piece = make_random_piece(board)
        piece = next_piece
        next_piece = make_random_piece(board)
    return piece, next_piece, board, moved_down
    
if __name__ == '__main__':
    main()