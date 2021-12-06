import pygame as py
import Board
import PieceSelector

# Initializing all necessary variables for game loop
py.init()
screen = py.display.set_mode((800, 800))
Running = True
frame = 300

# Game Loop
while Running:
    events = py.event.get()
    py.draw.rect(screen, (255, 255, 255), (250, 100, 300, 600), width = 1)
    Board.draw_lines(screen)

    piece = PieceSelector.selector()
    for row in piece.shape:
        for block in row:
            if block == 1:
                py.draw.rect(screen, piece.color, )

        py.draw.rect(screen, piece.color, ())

    for event in events:
        if event.type == py.QUIT:
            py.quit()
    py.display.update()
