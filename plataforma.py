import pygame

class Plataforma:
    """
    Clase que representa una plataforma en el juego.

    Atributos:
        rect (pygame.Rect): Rectangulo que define la posición y dimensiones de la plataforma.
        imagen (pygame.Surface): Imagen que representa la apariencia visual de la plataforma.

    Métodos:
        __init__(x, y, ancho, alto, imagen): Inicializa una nueva instancia de la clase Plataforma.
        draw(pantalla): Dibuja la plataforma en la pantalla en su posicion definida por 'rect'.
        obtener_rectangulo_colision(): Devuelve el rectángulo de colision de la plataforma.
    """

    def __init__(self, x, y, ancho, alto, imagen):
        """
        Inicializa una nueva instancia de la clase Plataforma.

        Parámetros:
            x (int): Coordenada X de la esquina superior izquierda de la plataforma.
            y (int): Coordenada Y de la esquina superior izquierda de la plataforma.
            ancho (int): Ancho de la plataforma.
            alto (int): Alto de la plataforma.
            imagen (str): Ruta de la imagen que se usara para la plataforma.
        """
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.imagen = pygame.image.load(r'Imagenes\Plataformas\NonSLiced.png')
        self.imagen = pygame.transform.scale(imagen, (ancho, alto))

    def draw(self, pantalla):
        """
        Dibuja la plataforma en la pantalla.

        Parámetros:
            pantalla (pygame.Surface): Superficie donde se dibujará la plataforma.
        """
        pantalla.blit(self.imagen, self.rect.topleft)

    def obtener_rectangulo_colision(self):
        """
        Devuelve el rectangulo de colisión de la plataforma.

        Retorna:
            pygame.Rect: El rectangulo que define la colisión de la plataforma.
        """
        return self.rect
