import pygame as py

class Block:
    def __init__(self, exists, color):
        self.exists = exists
        self.color = color

class Board:
    def __init__(self, state, bottom, points, level, alive):
        self.state = state
        self.alive = alive
        self.bottom = bottom
        self.points = points
        self.level = level


    # Erases a given set of rows and adds points
    def erase(self, rows):
        for row in rows:
            for column in row:
                self.state[row[column]].exists = False

        if(rows.len() == 1):
            self.points += (40 * level)
            for column in self.bottom:
                self.bottom[column] += 1

        elif(rows.len() == 2):
            self.points += (100 * level)
            for column in self.bottom:
                self.bottom[column] += 2

        elif(row.len() == 3):
            self.points += (300 * level)
            for column in self.bottom:
                self.bottom[column] += 3

        elif(row.len() == 4):
            self.points += (1200 * level)
            for column in self.bottom:
                self.bottom[column] += 4

    # Updates board after piece hits bottom
    def update(self):

        # Kills player if any blocks are at the top
        for block in self.state[0]:
            if (block.exists):
                self.alive = False

        # Erases rows if they are full
        for row in range(self.state(19, 0, -1)):
            rows = []
            if(isfull(row)):
                rows += row
        self.erase[rows]

        # Moves blocks down if row below them is empty
        for row in range(state(19, 0, -1)):
            if((isempty(row)) & (not isempty(row + 1))):
                for column in row:
                    self.state[row[column]].exists = True
                    self.state[(row + 1)[column]].exists = False
                    self.bottom[column] += 1

    def draw_blocks(self, screen):
        for row in self.state:
            for column in row:
                if(self.state[row[column]].exists):
                    py.draw.rect(screen, self.state[row[column]].color, (250 + row, 100 + column, 30, 30))


# Functions to deterimine if a row is empty or full
def isempty(row):
    for block in row:
        if(block.exists):
            return False
    return True

def isfull(row):
    for block in row:
        if(not(block.exists)):
            return False
    return True

def draw_lines(screen):
    indices = ((280, 100), (280, 700), (310, 100), (310, 700), (340, 100), (340, 700), (370, 100), (370, 700), (400, 100), (400, 700), (430, 100), (430, 700), (460, 100), (460, 700), (490, 100), (490, 700), (520, 100), (520, 700), (250, 130), (550, 130), (250, 160), (550, 160), (250, 190), (550, 190), (250, 220), (550, 220), (250, 250), (550, 250), (250, 280), (550, 280), (250, 310), (550, 310), (250, 340), (550, 340), (250, 370), (550, 370), (250, 400), (550, 400), (250, 430), (550, 430),      (250, 460), (550, 460), (250, 490), (550, 490), (250, 520), (550, 520), (250, 550), (550, 550), (250, 580), (550, 580), (250, 610), (550, 610), (250, 640), (550, 640), (250, 670), (550, 670))
    index = 0
    while(index < 56):
        py.draw.aaline(screen, (0, 0, 0), indices[index], indices[index + 1])
        index += 2
