import pygame
from contantes import *

class Enemy:
    """
    Clase que representa un enemigo en el juego.

    Atributos:
        x (int): Coordenada X del enemigo.
        y (int): Coordenada Y del enemigo.
        start_x (int): Posición inicial en X para el movimiento.
        end_x (int): Posición final en X para el movimiento.
        speed (int): Velocidad de movimiento del enemigo.
        direccion (int): Dirección en la que se mueve el enemigo (1 o -1).
        stepIndex (int): Índice para la animación del enemigo.
        colision (pygame.Rect): Rectángulo que define la colisión del enemigo.
        hp (int): Puntos de vida del enemigo.
        vivo (bool): Estado del enemigo (vivo o muerto).
        num_disparos (int): Contador de disparos realizados por el enemigo.
        score (int): Puntuación del enemigo.
        walk_l_enemigo (list): Lista de imágenes para la animación al caminar hacia la izquierda.
        walk_r_enemigo (list): Lista de imágenes para la animación al caminar hacia la derecha.

    Métodos:
        step(): Actualiza el índice de pasos para la animación.
        draw(pantalla): Dibuja el enemigo en la pantalla en su posición actual.
        move(): Mueve al enemigo entre las posiciones inicial y final.
        recibir_disparo(): Reduce los puntos de vida del enemigo al recibir un disparo.
        esta_vivo(): Verifica si el enemigo sigue vivo.
        obtener_rectangulo_colision(): Devuelve el rectángulo de colisión del enemigo.
    """

    def __init__(self, x, y, start_x, end_x, speed, direccion):
        """
        Inicializa una nueva instancia de la clase Enemy.

        Parámetros:
            x (int): Coordenada X del enemigo.
            y (int): Coordenada Y del enemigo.
            start_x (int): Posición inicial en X para el movimiento.
            end_x (int): Posición final en X para el movimiento.
            speed (int): Velocidad de movimiento del enemigo.
            direccion (int): Dirección inicial del movimiento (1 para derecha, -1 para izquierda).
        """
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
        """
        Actualiza el índice de pasos para la animación del enemigo.
        Resetea el índice al llegar al final de la secuencia de animación.
        """
        if self.stepIndex >= len(self.walk_l_enemigo) * 3:
            self.stepIndex = 0

    def draw(self, pantalla):
        """
        Dibuja el enemigo en la pantalla.

        Parámetros:
            pantalla (pygame.Surface): Superficie donde se dibujará el enemigo.
        """
        self.colision = pygame.Rect(self.x, self.y - 10, 30, 50)
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
        """
        Mueve al enemigo entre las posiciones inicial y final.
        Cambia la dirección al alcanzar un límite.
        """
        self.x += self.speed * self.direccion
        if self.x >= self.end_x:
            self.direccion = -1
        elif self.x <= self.start_x:
            self.direccion = 1

    def recibir_disparo(self):
        """
        Reduce los puntos de vida del enemigo al recibir un disparo.
        Si los puntos de vida llegan a cero, el enemigo se marca como muerto.
        """
        self.hp -= 1
        if self.hp <= 0:
            self.vivo = False

    def esta_vivo(self):
        """
        Verifica si el enemigo sigue vivo.

        Retorna:
            bool: True si el enemigo está vivo, False en caso contrario.
        """
        return self.vivo

    def obtener_rectangulo_colision(self):
        """
        Devuelve el rectángulo de colisión del enemigo.

        Retorna:
            pygame.Rect: El rectángulo que define la colisión del enemigo.
        """
        return self.colision
