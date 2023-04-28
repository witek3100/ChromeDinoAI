import math
import random

import pygame
import numpy as np

class PLayer:

    def __init__(self, screen, game):
        self.screen = screen
        self.score = 0
        self.height = 0
        self.velocity = 0
        self.super_jump = 0
        self.rect = pygame.Rect((33, 375 - self.height), (20, 25))
        self.game = game

        self.images = (pygame.image.load('static/dinorl.png'), pygame.image.load('static/dinoll.png'), pygame.image.load('static/dino.png'),
                       pygame.image.load('static/dinodll.png'), pygame.image.load('static/dinodrl.png'), pygame.image.load('static/dinod.png'))
        self.currimg = 0
        self.dimage = 0


    def control(self):
        self.rect = pygame.Rect((33, 375 - self.height), (20, 25))
        self.dimage = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.velocity == 0:
            self.velocity = 0.7
        if keys[pygame.K_SPACE] and self.velocity == 0 and self.super_jump == 0:
            self.velocity = 1.3
            self.super_jump = 50000
        if keys[pygame.K_s]:
            self.rect = pygame.Rect((30, 385 - self.height), (30, 15))
            self.dimage = 3

        self.height += self.velocity

        if self.super_jump > 0:
            self.super_jump -= 1

        if self.height > 0:
            self.velocity -= 0.003
        else:
            self.height = 0
            self.velocity = 0


    def draw(self):

        if self.height > 0:
            image = self.images[2+self.dimage]
        else:
            image = self.images[self.currimg+self.dimage]
            self.currimg = abs(self.currimg-1)

        self.screen.blit(image, (30, 375 - self.height))


    def get_ai_move(self):
        input = self.game.get_game_state_vector()
        result1 = np.array([math.tan(np.dot(input, self.brain[0][i])) for i in range(self.brain[0].shape[0])] + [1])
        result2 = np.array([math.tan(np.dot(result1, self.brain[1][i])) for i in range(self.brain[1].shape[0])] + [1])
        final_result = np.array([math.tan(np.dot(result2, self.brain[2][i])) for i in range(self.brain[2].shape[0])] + [1])
        output = [1 if final_result[0] > final_result[1] else 0, 1 if final_result[2] > final_result[3] else 0]

        self.rect = pygame.Rect((33, 375 - self.height), (20, 25))
        self.dimage = 0

        if output[0] and self.velocity == 0:
            self.velocity = 0.7
        if output[1]:
            self.rect = pygame.Rect((30, 385 - self.height), (30, 15))
            self.dimage = 3

        self.height += self.velocity

        if self.height > 0:
            self.velocity -= 0.003
        else:
            self.height = 0
            self.velocity = 0
    def create_brain(self, input_size, hidden_size, out_size):
        layer1 = np.array([[random.uniform(-1, 1) for i in range(input_size + 1)] for j in range(hidden_size)])
        layer2 = np.array([[random.uniform(-1, 1) for i in range(hidden_size + 1)] for j in range(hidden_size)])
        out_layer = np.array([[random.uniform(-1, 1) for i in range(hidden_size + 1) for j in range(out_size)]])
        self.brain = [layer1, layer2, out_layer]