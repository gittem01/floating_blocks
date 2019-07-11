import random
import numpy as np
import cv2
import time
import bios
import os
from copy import deepcopy

windowName = 'T'
top_size = 4

class fobject:

    def __init__(self, bt, color = 255, pos = [0, 0]):
        self.bt = bios.read(bt)
        self.pos = pos
        self.pos[0] -= len(self.bt[0])//2 + 1
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
                    game.show_map[self.pos[1]+i][self.pos[0]+j] = float(self.bt[i][j]*2)

    def move_control(self, game, key):

        if key == ord("w"):
            rotated = np.rot90(np.array(self.bt), 1, (0, 1)).tolist()

            for i in range(len(rotated)):
                for j in range(len(rotated[0])):
                    if int(rotated[i][j]) >= 1:
                        try:
                            if game.game_map[self.pos[1] + i][self.pos[0] + j]:
                                return
                        except IndexError:
                            return
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
                            return

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

    def draw_next(self, game):
        for i in range(len(self.bt)):
            for j in range(len(self.bt[0])):
                if int(self.bt[i][j]) >= 1:
                    game.draw_block([i - top_size + 1, game.game_size[1]//2-len(self.bt[0])//2 + j],
                                    color=(0, 0, 255))


class game:
    def __init__(self, game_size=[0, 0], block_size = 1):
        self.game_size  = game_size

        self.game_map = np.zeros((self.game_size[0], self.game_size[1])).tolist()
        self.game_map[-1] = np.ones((self.game_size[1])).tolist()

        self.show_map = deepcopy(self.game_map)
        self.block_size = block_size
        self.img = np.zeros(((self.game_size[0]+top_size)*self.block_size,
                    self.game_size[1]*self.block_size, 3), np.uint8)

    def draw_game(self):

        for i in range(len(self.show_map)):
            for j in range(len(self.show_map[0])):
                if self.show_map[i][j]:
                    self.draw_block([i, j], color=(i*9, 255, j*9))
                    if self.show_map[i][j]>1:# Coloring
                        #self.draw_block([i, j], color=(0, 0, 255))
                        pass

    def draw_block(self, pos, opt=1, color = 255):
        bs = self.block_size
        self.img[(pos[0]+top_size)*bs+1:(pos[0]+top_size)*bs+bs, pos[1]*bs+1:pos[1]*bs + bs] = color

    def line_clear(self):
        for i in range(len(self.game_map)-1):
            if 0 not in self.game_map[i]:
                self.game_map.pop(i)
                self.game_map.insert(0, [0 for i in range(len(self.game_map[0]))])
