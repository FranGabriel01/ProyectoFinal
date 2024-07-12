import pygame
from contantes import *
from flecha import Flecha
from utilidades import golpe_sonido

class Personaje:
    '''
    Clase para representar al personaje del juego utilizando Pygame.

    Attributes:
        x (int): La coordenada x del personaje.
        y (int): La coordenada y del personaje.
        velx (int): La velocidad horizontal del personaje.
        vely (int): La velocidad vertical del personaje.
        gravedad (int): La fuerza de gravedad que afecta al personaje.
        en_plataforma (bool): Indica si el personaje esta sobre una plataforma.
        mirar_derecha (bool): Indica si el personaje está mirando hacia la derecha.
        mirar_izquierda (bool): Indica si el personaje está mirando hacia la izquierda.
        caminar_indice (int): Indice para la animación de caminar.
        jump (bool): Indica si el personaje está saltando.
        saltar_indice (int): Índice para la animacion de salto.
        saltar_derecha (bool): Indica si el personaje esta saltando hacia la derecha.
        saltar_izquierda (bool): Indica si el personaje esta saltando hacia la izquierda.
        idle_indice (int): Indice para la animación de estado inactivo.
        attack_indice (int): Indice para la animacion de ataque.
        flechas (list): Lista de flechas disparadas por el personaje.
        cd (int): Tiempo de cooldown entre disparos.
        atacando (bool): Indica si el personaje esta atacando.
        colision (pygame.Rect): Rectángulo de colision del personaje.
        hp (int): Puntos de vida del personaje.
        vidas (int): Numero de vidas del personaje.
        vivo (bool): Indica si el personaje está vivo.
        tiempo_ultimo_golpe (int): Tiempo del último golpe recibido.
        COOLDOWN_DAÑO (int): Tiempo de cooldown entre golpes recibidos.
        score (int): Puntaje del personaje.
        walk_r (list): Lista de imágenes para la animacion de caminar a la derecha.
        walk_l (list): Lista de imágenes para la animacion de caminar a la izquierda.
        attack_r (list): Lista de imágenes para la animacion de ataque hacia la derecha.
        attack_l (list): Lista de imágenes para la animacion de ataque hacia la izquierda.
    '''
    def __init__(self, x, y):
        '''
        Inicializa un nuevo personaje.

        Args:
            x (int): La coordenada x inicial del personaje.
            y (int): La coordenada y inicial del personaje.
        '''
        self.x = x
        self.y = y
        self.velx = 10
        self.vely = 0
        self.gravedad = 1
        self.en_plataforma = False
        self.mirar_derecha = False
        self.mirar_izquierda = True
        self.caminar_indice = 0
        self.jump = False
        self.saltar_indice = 0
        self.saltar_derecha = False
        self.saltar_izquierda = False
        self.idle_indice = 0
        self.attack_indice = 0
        self.flechas = []
        self.cd = 0
        self.atacando = False
        self.colision = pygame.Rect(self.x, self.y, 48, 44)
        self.hp = 40
        self.vidas = 1
        self.vivo = True
        self.tiempo_ultimo_golpe = 0
        self.COOLDOWN_DAÑO = 50
        self.score = 0

        self.walk_r = [pygame.image.load(f'Imagenes/run/run_{i}.png') for i in range(1, 10)]
        self.walk_l = [pygame.transform.flip(img, True, False) for img in self.walk_r]
        self.attack_r = [pygame.image.load(f'Imagenes/2_atk/2_atk_{i}.png') for i in range(1, 15)]
        self.attack_l = [pygame.transform.flip(img, True, False) for img in self.attack_r]

    def mover_personaje(self, usuarioInput, lista_plataformas):
        '''
        Mueve el personaje basado en la entrada del usuario y las plataformas.

        Args:
            usuarioInput (dict): Entrada del usuario.
            lista_plataformas (list): Lista de plataformas en el juego.
        '''
        if usuarioInput[pygame.K_d] and self.x <= ANCHO - 60:
            self.x += self.velx
            self.mirar_derecha = True
            self.mirar_izquierda = False
        elif usuarioInput[pygame.K_a] and self.x >= 0:
            self.x -= self.velx
            self.mirar_derecha = False
            self.mirar_izquierda = True
        else:
            self.caminar_indice = 0

        if not self.en_plataforma:
            self.y += self.vely
            self.vely += self.gravedad

        self.en_plataforma = False
        for plataforma in lista_plataformas:
            if self.colision.colliderect(plataforma.obtener_rectangulo_colision()):
                self.y = plataforma.rect.top - self.colision.height
                self.vely = 0
                self.en_plataforma = True
                break

    def draw(self, pantalla):
        '''
        Dibuja el personaje en la pantalla.

        Args:
            pantalla (pygame.Surface): La superficie de la ventana del juego.
        '''
        self.colision = pygame.Rect(self.x, self.y, 48, 44)
        # pygame.draw.rect(pantalla, RED, self.colision, 1)
        pygame.draw.rect(pantalla, (255, 0, 0), (10, 10, 40, 10))
        if self.hp >= 0:
            pygame.draw.rect(pantalla, (0, 255, 0), (10, 10, self.hp, 10))
        if self.atacando:
            if self.attack_indice >= 14:
                self.attack_indice = 0
                self.atacando = False
            if self.mirar_izquierda:
                pantalla.blit(self.attack_l[self.attack_indice], (self.x, self.y))
            elif self.mirar_derecha:
                pantalla.blit(self.attack_r[self.attack_indice], (self.x, self.y))
            self.attack_indice += 1
        else:
            if self.caminar_indice >= 9:
                self.caminar_indice = 0
            if self.mirar_izquierda:
                pantalla.blit(self.walk_l[self.caminar_indice], (self.x, self.y))
                self.caminar_indice += 1
            elif self.mirar_derecha:
                pantalla.blit(self.walk_r[self.caminar_indice], (self.x, self.y))
                self.caminar_indice += 1

    def saltar(self, usuarioInput):
        '''
        Hace que el personaje salte si esta en una plataforma y se presiona la tecla de espacio.

        Args:
            usuarioInput (dict): Entrada del usuario.
        '''
        if usuarioInput[pygame.K_SPACE] and self.en_plataforma:
            self.jump = True
            self.en_plataforma = False
            self.vely = -20
        if self.jump:
            self.y += self.vely
            self.vely += self.gravedad

    def direccion(self):
        '''
        Devuelve la direccion en la que el personaje está mirando.

        Returns:
            int: 1 si el personaje mira a la derecha, -1 si mira a la izquierda.
        '''
        if self.mirar_derecha:
            return 1
        if self.mirar_izquierda:
            return -1

    def actualizar_cooldown(self):
        '''
        Actualiza el tiempo de cooldown entre disparos.
        '''
        if self.cd >= 30:
            self.cd = 0
        elif self.cd > 0:
            self.cd += 1

    def disparar(self, userInput, enemigos):
        '''
        Dispara una flecha si se presiona la tecla G y el cooldown es 0.

        Args:
            userInput (dict): Entrada del usuario.
            enemigos (list): Lista de enemigos en el juego.
        '''
        self.hit(enemigos)
        self.actualizar_cooldown()
        if userInput[pygame.K_g] and self.cd == 0:
            golpe_sonido.play()
            flecha = Flecha(self.x, self.y, self.direccion())
            self.flechas.append(flecha)
            self.cd = 1
            self.atacando = True
        for flecha in self.flechas:
            flecha.move()
            if flecha.flecha_fuera():
                self.flechas.remove(flecha)

    def hit(self, enemigos):
        '''
        Verifica si una flecha golpea a un enemigo y reduce su hp si es asi.

        Args:
            enemigos (list): Lista de enemigos en el juego.
        '''
        for boss in enemigos:
            for flecha in self.flechas:
                if boss.colision[0] < flecha.x < boss.colision[0] + boss.colision[2] and boss.colision[1] < flecha.y < boss.colision[1] + boss.colision[3]:
                    boss.hp -= 10
                    self.flechas.remove(flecha)

    def obtener_rectangulo_colision(self):
        '''
        Obtiene el rectangulo de colision del personaje.

        Returns:
            pygame.Rect: El rectangulo de colision del personaje.
        '''
        return self.colision

    def sobre_plataforma(self, lista_plataformas):
        '''
        Verifica si el personaje esta sobre una plataforma.

        Args:
            lista_plataformas (list): Lista de plataformas en el juego.

        Returns:
            bool: True si el personaje esta sobre una plataforma, False en caso contrario.
        '''
        colision_plataforma = False
        for plataforma in lista_plataformas:
            if self.colision.colliderect(plataforma.obtener_rectangulo_colision()) and self.y + self.colision.height <= plataforma.rect.top + self.vely:
                self.y = plataforma.rect.top - self.colision.height
                colision_plataforma = True
                break
        return colision_plataforma

    def colision_con_enemigos(self, enemigos):
        '''
        Verifica si el personaje colisiona con algun enemigo y reduce su hp si es así.

        Args:
            enemigos (list): Lista de enemigos en el juego.
        '''
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_golpe > self.COOLDOWN_DAÑO:
            for enemigo in enemigos:
                if self.colision.colliderect(enemigo.obtener_rectangulo_colision()):
                    self.hp -= 1
                    self.tiempo_ultimo_golpe = ahora
                    if self.hp <= 0:
                        self.vivo = False 
                    break


    
