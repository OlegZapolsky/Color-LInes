import pygame
import random

blue = pygame.image.load(r"data/blue.png")
green = pygame.image.load(r"data/green.png")
orange = pygame.image.load(r"data/orange.png")
purple = pygame.image.load(r"data/purple.png")
red = pygame.image.load(r"data/red.png")
yellow = pygame.image.load(r"data/yellow.png")


class Ball:
    def __init__(self, rsize):
        self.r_size = rsize
        self.indent = 2

    def draw_ball(self, x, y, c):
        sc.blit(color_def(c[1]), (10 + x * 64, 54 + y * 64))
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
                    x * self.cell_size + self.left, y * self.cell_size + self.top + 44, self.cell_size,
                    self.cell_size), 1)
        pygame.draw.rect(screen, pygame.Color(55, 55, 55), (456, 10, 128, 40), 2)

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
        text = font.render(f'{self.points}', 1, (0, 0, 0))
        sc.blit(text, (460, 16))

    def generate_emp_list(self):
        emp_list = []
        s = self.board
        for i in range(len(s)):
            for j in range(len(s[i])):
                if s[i][j] == 0:
                    emp_list.append((j, i))
        return emp_list

    def board_clear(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = 0

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
    colors = {'R': red, 'G': green, 'B': blue, 'P': purple, 'Y': yellow, 'O': orange}
    n = colors[w]
    return n


pygame.init()
clock = pygame.time.Clock()
board = Board(9, 9)
ball = Ball(60)
col = [((255, 0, 0), 'R'), ((0, 255, 0), 'G'), ((0, 0, 255), 'B'), ((140, 0, 255), 'P'),
       ((255, 255, 0), 'Y'), ((255, 165, 0), 'O')]
size = width, height = 596, 640
sc = pygame.display.set_mode(size)
font_size = 52
font = pygame.font.Font(None, font_size)
c = [(0, 255, 0), (0, 0, 255), (140, 0, 255), (255, 255, 0), (255, 165, 0), (255, 50, 180)]


def menu():
    start = False
    while not start:
        sc.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 238 < event.pos[0] < 358 and 290 < event.pos[1] < 350:
                    play()
                    break
        for i in range(10):
            pygame.draw.circle(sc, random.choice(c), (random.randint(10, 580),
                                                      random.randint(10, 630)), random.randint(5, 60))
        text = font.render('START', 5, (255, 0, 0))
        sc.blit(text, (242, 304))
        text = font.render('Color Lines', 5, (255, 0, 0))
        sc.blit(text, (200, 160))
        pygame.draw.rect(sc, (255, 0, 0), (236, 290, 124, 60), 4)
        pygame.display.flip()
        clock.tick(12)


def play():
    move = False
    running = True
    font_size = 36
    for i in range(3):
        s1 = board.generate_emp_list()
        x, y = random.choice(s1)
        ball.draw_ball(x, y, random.choice(col))
    while running:
        s1 = board.generate_emp_list()
        s = board.get_board()
        if len(s1) < 3:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        board.board_clear()
                        menu()
                        break
                sc.fill((0, 0, 0))
                text = font.render('GAME OVER', 10, (255, 0, 0))
                sc.blit(text, (180, 304))
                pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                ex = (event.pos[0] - 10) // 64
                ey = (event.pos[1] - 54) // 64
                if not move and s[ey][ex] != 0 and event.pos[1] >= 44:
                    move = True
                    c = s[ey][ex]
                    board.record(ex, ey, 0)
                elif move and s[ey][ex] == 0:
                    board.record(ex, ey, c)
                    move = False
                    c = 0
                    for i in range(3):
                        x, y = random.choice(s1)
                        ball.draw_ball(x, y, random.choice(col))
                board.collection_check()
        sc.fill((195, 195, 195))
        board.render(sc)
        board.draw_board()
        pygame.display.flip()


menu()