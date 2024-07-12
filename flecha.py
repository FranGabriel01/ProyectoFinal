import pygame
from contantes import * 

class Flecha:
    '''
    Clase para representar una flecha en el juego utilizando Pygame.

    Attributes:
        x (int): La coordenada x de la flecha.
        y (int): La coordenada y de la flecha.
        velocidad (int): La velocidad de movimiento de la flecha.
        direccion (int): La direccion en la que se mueve la flecha (1 para derecha, -1 para izquierda).
        img (pygame.Surface): La imagen de la flecha.
    '''
    def __init__(self, x, y, direccion):
        '''
        Inicializa una nueva flecha.

        Args:
            x (int): La coordenada x inicial de la flecha.
            y (int): La coordenada y inicial de la flecha.
            direccion (int): La direccion de la flecha (1 para derecha, -1 para izquierda).
        '''
        self.x = x
        self.y = y
        self.velocidad = 10 * direccion
        self.direccion = direccion
        self.img = pygame.image.load(r'Imagenes\arrow\arrow_.png')

    def move(self):
        '''
        Mueve la flecha en la direccion especificada por su velocidad.
        '''
        self.x += self.velocidad

    def draw_flecha(self, pantalla):
        '''
        Dibuja la flecha en la pantalla.

        Args:
            pantalla (pygame.Surface): La superficie de la ventana del juego.
        '''
        pantalla.blit(self.img, (self.x, self.y))

    def flecha_fuera(self):
        '''
        Verifica si la flecha salio de la pantalla.

        Returns:
            bool: True si la flecha está fuera de los limites de la pantalla, False en caso contrario.
        '''
        return self.x < 0 or self.x > ANCHO
