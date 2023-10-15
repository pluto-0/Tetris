import pygame
import random
import logic
import pprint

BLOCK_SIZE = logic.BLOCK_SIZE
SCREEN_SIZE = (720, 1280)

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    board = logic.Board()
    board_screen = pygame.Surface((BLOCK_SIZE * board.cols, BLOCK_SIZE * board.rows))
    white_box = pygame.Rect(0, 0, BLOCK_SIZE * board.cols, BLOCK_SIZE * board.rows)
    piece = make_random_piece(board)
    score = pygame.font.SysFont(None,50)
    score_screen = score.render("SCORE = " + str(board.score), True, 'white')
    frame = 0
    moved_down = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    piece, board, moved_down = move_down(piece, board, moved_down)
                elif event.key == pygame.K_RIGHT:
                    move_right(piece, board)
                elif event.key == pygame.K_LEFT:
                    move_left(piece, board)
                elif event.key == pygame.K_UP:
                    rotate(piece, board)
                elif event.key == pygame.K_SPACE:
                    piece, board = drop_down(piece, board)
            elif event.type == pygame.QUIT:
                running = False
           
        if frame % 15 == 0:
            if not moved_down:
                piece, board, moved_down = move_down(piece, board, moved_down)
            moved_down = False

        screen.fill('black')
        board_screen.fill('black')

        for block in piece.position:
            cords = logic.convert_cords(block)

            piece_block_object = pygame.Rect(cords[1], cords[0], BLOCK_SIZE-1, BLOCK_SIZE-1)
            pygame.draw.rect(board_screen, piece.color, piece_block_object)

        for i, row in enumerate(board.state):
            for j, column in enumerate(row):
                if column != None:
                    cords = logic.convert_cords([i, j])
                    board_block_object = pygame.Rect(cords[1], cords[0], BLOCK_SIZE-1, BLOCK_SIZE-1)
                    pygame.draw.rect(board_screen, column, board_block_object)
        
        score_screen.fill('black')
        score_screen = score.render("SCORE = " + str(board.score), True, 'white')
        screen.blit(score_screen, [20, 20])
        
        pygame.draw.rect(board_screen, 'white', white_box, 1)
        pygame.Surface.blit(screen, board_screen, find_white_box_cords(board))

        pygame.display.flip()
        frame += 1
        clock.tick(60)
        


def find_white_box_cords(board):
    return ((SCREEN_SIZE[0] - (BLOCK_SIZE * board.cols)) // 2,
             (SCREEN_SIZE[1] - (BLOCK_SIZE * board.rows)) // 2)

def make_random_piece(board):
    piece_name = random.choice(logic.pieces)
    return logic.Piece(board.rows, board.cols, piece_name)

def move_down(piece, board, moved_down):
    new_position = piece.move('d')
    if board.is_legal_position(new_position):
        moved_down = True
        piece.position = new_position
    else:
        board.place_piece(piece)
        if not board.update():
            board = logic.Board()
        new_piece = make_random_piece(board)
        piece = make_random_piece(board)
    return piece, board, moved_down
    
def move_right(piece, board):
    new_position = piece.move('r')
    if board.is_legal_position(new_position):
        piece.position = new_position

def move_left(piece, board):
    new_position = piece.move('l')
    if board.is_legal_position(new_position):
        piece.position = new_position

def rotate(piece, board):
    new_position = piece.rotate()
    if board.is_legal_position(new_position):
        piece.rotation = (piece.rotation + 1) % 4
        piece.position = new_position

def drop_down(piece, board):
    new_position = piece.move('d')
    while board.is_legal_position(new_position):
        piece.position = new_position
        new_position = piece.move('d')
    board.place_piece(piece)
    if not board.update():
        board = logic.Board()
    piece = make_random_piece(board)
    return piece, board
    
if __name__ == '__main__':
    main()