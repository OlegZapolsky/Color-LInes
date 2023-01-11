import pygame
import random


class Ball:
    def __init__(self, rsize):
        self.r_size = rsize
        self.indent = 2

    def draw_ball(self, x, y, c):
        pygame.draw.ellipse(sc, c[0], (12 + x * 64, 12 + y * 64, self.r_size, self.r_size))
        board.record(x, y, c[1])


class Board:
    def __init__(self, width, height):
        self.points = 0
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 64

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(55, 55, 55), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def record(self, x, y, c):
        self.board[y][x] = c

    def get_board(self):
        s = self.board
        return s

    def draw_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != 0:
                    ball.draw_ball(j, i, (color_def(str(self.board[i][j])), self.board[i][j]))

    def generate_emp_list(self):
        emp_list = []
        s = self.board
        for i in range(len(s)):
            for j in range(len(s[i])):
                if s[i][j] == 0:
                    emp_list.append((j, i))
        return emp_list

    def collection_check(self):
        removed_balls = []
        s = self.board
        for i in range(9):
            color = ''
            line = []
            if s[i].count(0) < 5:
                for j in range(9):
                    if s[i][j] != 0:
                        if len(line) == 0:
                            color = s[i][j]
                            line.append((j, i))
                        elif len(line) > 0 and s[i][j] == color:
                            line.append((j, i))
                        elif len(line) > 0 and s[i][j] != color:
                            if len(line) >= 5:
                                removed_balls += line
                                line = []
                            elif len(line) < 5:
                                line = []
                                line.append((j, i))
                                color = s[i][j]
                    elif s[i][j] == 0:
                        if len(line) > 0:
                            if len(line) >= 5:
                                removed_balls += line
                                line = []
                            elif len(line) < 5:
                                line = []
            if len(line) >= 5:
                removed_balls += line

        for j in range(9):
            color = ''
            line = []
            for i in range(9):
                if s[i][j] != 0:
                    if len(line) == 0:
                        color = s[i][j]
                        line.append((j, i))
                    elif len(line) > 0 and s[i][j] == color:
                        line.append((j, i))
                    elif len(line) > 0 and s[i][j] != color:
                        if len(line) >= 5:
                            removed_balls += line
                            line = []
                        elif len(line) < 5:
                            line = []
                            line.append((j, i))
                            color = s[i][j]
                elif s[i][j] == 0:
                    if len(line) > 0:
                        if len(line) >= 5:
                            removed_balls += line
                            line = []
                        elif len(line) < 5:
                            line = []
            if len(line) >= 5:
                removed_balls += line
        self.points += len(removed_balls) * (len(removed_balls) - 4)
        for i in removed_balls:
            self.board[i[1]][i[0]] = 0


def color_def(w):
    colors = {'R': (255, 0, 0), 'G': (0, 255, 0), 'B': (0, 0, 255), 'P': (140, 0, 255),
              'Y': (255, 255, 0), 'O': (255, 165, 0)}
    n = colors[w]
    return n


board = Board(9, 9)
ball = Ball(60)
col = [((255, 0, 0), 'R'), ((0, 255, 0), 'G'), ((0, 0, 255), 'B'), ((140, 0, 255), 'P'),
       ((255, 255, 0), 'Y'), ((255, 165, 0), 'O')]
size = width, height = 596, 596
sc = pygame.display.set_mode(size)
running = True
move = False
sc.fill((195, 195, 195))
for i in range(3):
    s = board.generate_emp_list()
    x, y = random.choice(s)
    ball.draw_ball(x, y, random.choice(col))
while running:
    s = board.get_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            ex = (event.pos[0] - 10) // 64
            ey = (event.pos[1] - 10) // 64
            if not move and s[ey][ex] != 0:
                move = True
                c = s[ey][ex]
                board.record(ex, ey, 0)
            elif move and s[ey][ex] == 0:
                board.record(ex, ey, c)
                move = False
                c = 0
                for i in range(3):
                    s = board.generate_emp_list()
                    x, y = random.choice(s)
                    ball.draw_ball(x, y, random.choice(col))
            board.collection_check()
    sc.fill((195, 195, 195))
    board.render(sc)
    board.draw_board()
    pygame.display.flip()