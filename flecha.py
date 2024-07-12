import pygame
from contantes import * 

class Flecha:
    def __init__(self, x, y, direccion):
        self.x = x
        self.y = y
        self.velocidad = 10 * direccion
        self.direccion = direccion
        self.img = pygame.image.load(r'Imagenes\arrow\arrow_.png')

    def move(self):
        self.x += self.velocidad

    def draw_flecha(self, pantalla):
        pantalla.blit(self.img, (self.x, self.y))

    def flecha_fuera(self):
        return self.x < 0 or self.x > 800
