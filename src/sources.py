import random
import numpy as np
import cv2
import time
import bios

windowName = 'Drawing'

class fobject:
    def __init__(self, bt, color = 255, pos = [0, 0]):
        self.bt = bios.read(bt)
        self.pos = pos
        self.color = color
    def rotate(self, spin = (0, 1)):
        self.bt = np.rot90(np.array(self.bt), 1, spin).tolist()

    def draw_obj(self, game):
        ret = False
        for i in range(len(self.bt)):
            for j in range(len(self.bt[0])):
                if game.game_map[self.pos[1] + len(self.bt)][self.pos[0]+j] and self.bt[i][j]:
                    ret = True
                if self.bt[i][j]:
                    game.game_map[self.pos[1]+i][self.pos[0]+j] = float(self.bt[i][j])
        return ret


class game:
    def __init__(self, game_size=[0, 0], block_size = 1):
        self.game_size  = game_size
        self.game_map = np.zeros((self.game_size[0], self.game_size[1])).tolist()
        self.game_map[-1] = np.ones((self.game_size[1])).tolist()
        self.block_size = block_size
        self.img = np.zeros((self.game_size[0]*self.block_size,
                    self.game_size[1]*self.block_size, 3), np.uint8)

    def draw_game(self):

        for i in range(len(self.game_map)):
            for j in range(len(self.game_map[0])):
                if self.game_map[i][j]:
                    self.draw_block([i, j], (255, 255, 0))

    def draw_block(self, pos, color = 255):
        bs = self.block_size
        self.img[pos[0]*bs:pos[0]*bs+bs, pos[1]*bs:pos[1]*bs + bs] = color

    def clear_block(self):

        self.game_map = np.rot90(np.array((self.game_map), np.uint8)).tolist()
        for i in range(len(self.game_map[0])-1):
            t = len(self.game_map[0]) - 2 - i
            for j in range(len(self.game_map)):
                if not self.game_map[j][t]:
                    self.game_map[j][:t] = [0 for i in range(len(self.game_map[j][:t]))]

        self.game_map = np.rot90(np.array((self.game_map), np.uint8), 1, (1, 0)).tolist()
