import pygame
from contantes import *

class Enemy:
    def __init__(self, x, y, start_x, end_x, speed, direccion):
        self.x = x
        self.y = y
        self.start_x = start_x
        self.end_x = end_x
        self.speed = speed
        self.direccion = direccion 
        self.stepIndex = 0
        self.colision = pygame.Rect(self.x, self.y, 30, 50)
        self.hp = 40  
        self.vivo = True
        self.num_disparos = 0  
        self.score = 0

        self.walk_l_enemigo = [pygame.image.load(f'Imagenes/Heavy Bandit/Run/HeavyBandit_Run_{i}.png') for i in range(1, 7)]
        self.walk_r_enemigo = [pygame.transform.flip(img, True, False) for img in self.walk_l_enemigo]

    def step(self):
        if self.stepIndex >= len(self.walk_l_enemigo) * 3:
            self.stepIndex = 0

    def draw(self, pantalla):
        self.colision = pygame.Rect(self.x, self.y-10, 30, 50)
        # pygame.draw.rect(pantalla, RED, self.colision, 1)
        self.step()
        if self.direccion == 1:
            index = min(self.stepIndex // 3, len(self.walk_r_enemigo) - 1)
            pantalla.blit(self.walk_r_enemigo[index], (self.x, self.y))
        else:
            index = min(self.stepIndex // 3, len(self.walk_l_enemigo) - 1)
            pantalla.blit(self.walk_l_enemigo[index], (self.x, self.y))
        self.stepIndex += 1

    def move(self):
        self.x += self.speed * self.direccion
        if self.x >= self.end_x:
            self.direccion = -1
        elif self.x <= self.start_x:
            self.direccion = 1

    def recibir_disparo(self):
        self.hp -= 1
        if self.hp <= 0:
            self.vivo = False

    def esta_vivo(self):
        return self.vivo

    def obtener_rectangulo_colision(self):
        return self.colision