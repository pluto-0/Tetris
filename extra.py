import pygame
import random
import tetris
from tetris import Piece, Board, rotate, move_left, move_right, drop_down, make_random_piece, get_cpu_move, possible_states, drop_down2, get_metrics
import pprint
from time import sleep
from collections import deque

BLOCK_SIZE = tetris.BLOCK_SIZE
SCREEN_SIZE = (720, 1280)

def game(piece,next_piece,board,move):
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    board_screen = pygame.Surface((BLOCK_SIZE * board.cols, BLOCK_SIZE * board.rows))
    white_box = pygame.Rect(0, 0, BLOCK_SIZE * board.cols, BLOCK_SIZE * board.rows)
    score = pygame.font.SysFont(None,50)
    score_screen = score.render("SCORE = " + str(board.score), True, 'white')
    next_piece_screen = pygame.Surface((BLOCK_SIZE * 5, BLOCK_SIZE  * 5))
    next_piece_box = pygame.Rect(0, 0, BLOCK_SIZE * 5, BLOCK_SIZE * 5)
    pygame.draw.rect(next_piece_screen, 'white', next_piece_box, 1)
    frame = 0
    cpu_moves = deque()
    moved_down = False
    running = True

    while running:
        if not cpu_moves:
            rotation, direction, offset = move
            for i in range(abs(rotation - piece.rotation)):
                cpu_moves.append('rotate')
            for i in range(offset):
                cpu_moves.append(direction)
            cpu_moves.append('drop')
        if frame % 5 == 0:
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
                clock.tick(5)
                return piece, next_piece, board
            moved_down = False

        screen.fill('black')
        board_screen.fill('black')
        next_piece_screen.fill('black')

        for block in piece.position:
            cords = tetris.convert_cords(block)

            piece_block_object = pygame.Rect(cords[1], cords[0], BLOCK_SIZE-1, BLOCK_SIZE-1)
            pygame.draw.rect(board_screen, piece.color, piece_block_object)
        
        # Kind of reproducing code here, would be better to have a function that 
        # calculates drop down position, but I ran into issues with passing pieces
        # by reference
        ghost_piece = tetris.Piece(board.rows, board.cols, piece.name)
        ghost_piece.position = piece.position
        new_position = ghost_piece.move('d')
        while board.is_legal_position(new_position):
            ghost_piece.position = new_position
            new_position = ghost_piece.move('d')
        
        for block in ghost_piece.position:
            cords = tetris.convert_cords(block)
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
                    cords = tetris.convert_cords([i, j])
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
        clock.tick(5)
        print("sa")

        


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
            board = tetris.Board()
        new_piece = make_random_piece(board)
        piece = next_piece
        next_piece = make_random_piece(board)
    return piece, next_piece, board, moved_down
    
