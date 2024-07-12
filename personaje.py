import pygame
from contantes import *
from flecha import Flecha
from utilidades import golpe_sonido

class Personaje:
    def __init__(self, x, y):
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
        if usuarioInput[pygame.K_SPACE] and self.en_plataforma:
            self.jump = True
            self.en_plataforma = False
            self.vely = -20
        if self.jump:
            self.y += self.vely
            self.vely += self.gravedad

    def direccion(self):
        if self.mirar_derecha:
            return 1
        if self.mirar_izquierda:
            return -1

    def actualizar_cooldown(self):
        if self.cd >= 30:
            self.cd = 0
        elif self.cd > 0:
            self.cd += 1

    def disparar(self, userInput, enemigos):
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
        for boss in enemigos:
            for flecha in self.flechas:
                if boss.colision[0] < flecha.x < boss.colision[0] + boss.colision[2] and boss.colision[1] < flecha.y < boss.colision[1] + boss.colision[3]:
                    boss.hp -= 10
                    self.flechas.remove(flecha)

    def obtener_rectangulo_colision(self):
        return self.colision

    def sobre_plataforma(self, lista_plataformas):
        colision_plataforma = False
        for plataforma in lista_plataformas:
            if self.colision.colliderect(plataforma.obtener_rectangulo_colision()) and self.y + self.colision.height <= plataforma.rect.top + self.vely:
                self.y = plataforma.rect.top - self.colision.height
                colision_plataforma = True
                break
        return colision_plataforma

    def colision_con_enemigos(self, enemigos):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_golpe > self.COOLDOWN_DAÑO:
            for enemigo in enemigos:
                if self.colision.colliderect(enemigo.obtener_rectangulo_colision()):
                    self.hp -= 1
                    self.tiempo_ultimo_golpe = ahora
                    if self.hp <= 0:
                        self.vivo = False 
                    break

    
