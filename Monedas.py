import pygame
from contantes import *

class Moneda:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imagen_moneda = pygame.image.load(r'Imagenes\Coin\coin64.png')
        self.imagen_moneda = pygame.transform.scale(self.imagen_moneda, (32, 32))
        self.colision = pygame.Rect(self.x, self.y, 32, 32)

    def draw(self, pantalla):
        # pygame.draw.rect(pantalla, RED, self.colision, 1) 
        self.colision = pygame.Rect(self.x, self.y, 32, 32)
        pantalla.blit(self.imagen_moneda, self.colision)
