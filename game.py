import pygame
import random
from enum import Enum

class Difficulty(Enum):
    EASY = 0.10
    INTERMEDIATE = 0.12
    ADVANCED = 0.15
    EXPERT = 0.17
    MASTER = 0.20

class Color(Enum):
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 255)
    RED = (255, 0, 0)
    PURPLE = ()
    MAROON = ()
    TURQUOISE = ()
    BLACK = ()
    GRAY = ()

class Game():

    def __init__(self, size: tuple[int, int], mines: int = 0, difficulty: Difficulty = Difficulty.EASY, blocksize: int = 20) -> None:
        self.size = size
        self.mines = mines
        if self.mines <= 0:
            self.mines = round(self.size[0] * self.size[1] * difficulty.value)

        pygame.init()
        self.screen = pygame.display.set_mode(tuple(i * blocksize for i in self.size))
        self.reset()

    def reset(self) -> None:
        self.move_count = 0;

    def generateMinefield(self, size: tuple[int, int], mines: int, placeholder: tuple[int, int], symbol: int = -2) -> list[list[int]]:
        placeholder = placeholder[0] * placeholder[1]
        fields = size[0] * size[1]
        minefield = [-2 for _ in range(fields)]
        for i in random.sample(range(fields - 1), mines):
            minefield[i] = -1;
        minefield = [[minefield[x * size[1] + y] for y in range(size[1])] for x in range(size[0])]
        return minefield

    def play_move(self, move: tuple[int, int]) -> (bool, bool, int):
        if (self.move_count == 0):
            self.minefield = self.generateMinefield(self.size, self.mines, move)
            self.minefield[move[1]][move[0]] = "\033[32m" + str(self.get_mine_count(move))

        self.move_count += 1

        for row in self.minefield:
            for sym in row:
                if sym == -1:
                    print("\033[41m M \033[0m", end="")
                elif sym == -2:
                    print("\033[40m   \033[0m", end="")
                else:
                    print(f"\033[40m {sym} \033[0m", end="")
            print("")

        return False, False, 0
    
    def get_mine_count(self, pos: tuple[int, int]) -> int:

        fields = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

        if pos[1] == 0:
            for _ in range(3):
                fields.pop(0)
        elif pos[1] == self.size[1] - 1:
            for _ in range(3):
                fields.pop()
        if pos[0] == 0:
            fields = list(filter(lambda i: i[1] != -1, fields))
        elif pos[0] == self.size[0] - 1:
            fields = list(filter(lambda i: i[1] != 1, fields))

        mine_counter = 0

        for i in fields:
            if self.minefield[pos[1] + i[0]][pos[0] + i[1]] == -1:
                mine_counter += 1
                
        print(fields)
        return mine_counter

    def exit(self):
        pygame.quit()

game = Game((16, 16), difficulty=Difficulty.MASTER)
game.play_move((5, 5))

'''
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    pygame.display.flip()
    clock.tick(60)
'''

pygame.quit()