import pygame

class Plataforma:
    def __init__(self, x, y, ancho, alto, imagen):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.imagen = pygame.image.load(r'Imagenes\Plataformas\NonSLiced.png')
        self.imagen = pygame.transform.scale(imagen, (ancho, alto))

    def draw(self, pantalla):
        pantalla.blit(self.imagen, self.rect.topleft)

    def obtener_rectangulo_colision(self):
        return self.rect