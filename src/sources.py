import random
import numpy as np
import cv2
import time
import bios
from copy import deepcopy

windowName = 'Drawing'

class fobject:
    def __init__(self, bt, color = 255, pos = [1, 1]):
        self.bt = bios.read(bt)
        self.pos = pos
        self.color = color
    def rotate(self, spin = (0, 1)):
        self.bt = np.rot90(np.array(self.bt), 1, spin).tolist()

    def check_block(self, game):
        for i in range(len(self.bt[0])):
            for j in range(len(self.bt)):
                j = len(self.bt) - j - 1
                if int(self.bt[j][i]) >= 1:
                    if game.game_map[self.pos[1] + j + 1][self.pos[0]+i]:
                        return True
                    else:
                        break
        return False

    def draw_obj(self, game):

        for i in range(len(self.bt)):
            for j in range(len(self.bt[0])):
                if int(self.bt[i][j]) >= 1:
                    game.show_map[self.pos[1]+i][self.pos[0]+j] = float(self.bt[i][j])

    def move_control(self, game, key):

        if key == ord("w"):
            self.rotate()

        elif key == ord("s"):
            self.pos[1] += 1

        elif key == ord("a"):

            for i in range(len(self.bt)):
                for j in range(len(self.bt[0])):
                    if int(self.bt[i][j]) >= 1:
                        try:
                            if game.game_map[self.pos[1] + i][self.pos[0] + j - 1]:
                                return
                        except IndexError:
                            continue

            if self.pos[0] > 0:
                self.pos[0] += -1

        elif key == ord("d"):
            for i in range(len(self.bt)):
                for j in range(len(self.bt[0])):
                    j = len(self.bt[0]) - j - 1
                    if int(self.bt[i][j]) >= 1:
                        try:
                            if game.game_map[self.pos[1] + i][self.pos[0] + j + 1]:
                                return
                        except IndexError:
                            continue

            if self.pos[0] < len(game.game_map[0])-len(self.bt[0]):
                self.pos[0] += 1

        else:
            pass

class game:
    def __init__(self, game_size=[0, 0], block_size = 1):
        self.game_size  = game_size

        self.game_map = np.zeros((self.game_size[0], self.game_size[1])).tolist()
        self.game_map[-1] = np.ones((self.game_size[1])).tolist()

        self.show_map = deepcopy(self.game_map)
        self.block_size = block_size
        self.img = np.zeros((self.game_size[0]*self.block_size,
                    self.game_size[1]*self.block_size, 3), np.uint8)

    def draw_game(self):

        for i in range(len(self.show_map)):
            for j in range(len(self.show_map[0])):
                if self.show_map[i][j]:
                    self.draw_block([i, j], color=(255, 255, 0))

    def draw_block(self, pos, opt=1, color = 255):
        bs = self.block_size
        self.img[pos[0]*bs+1:pos[0]*bs+bs-1, pos[1]*bs+1:pos[1]*bs + bs-1] = color
