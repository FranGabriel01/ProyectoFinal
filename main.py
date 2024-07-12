import pygame
import sys
import json
import csv
from contantes import *
from personaje import Personaje
from enemigo import Enemy
from plataforma import Plataforma
from utilidades import *
from Monedas import Moneda

pygame.init()

def inicializar():
    '''
    Inicializa la pantalla, el fondo y la musica del juego.

    Returns:
        pantalla (pygame.Surface): La superficie de la ventana del juego.
        fondo_pantalla (pygame.Surface): La imagen de fondo del juego.
        volumen_musica (float): El volumen inicial de la musica.
    '''
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    fondo_pantalla = pygame.image.load(r'Imagenes\escenario\terror.png')
    pygame.display.set_caption("Mostrar Coordenadas del Mouse")
    pygame.mixer.music.load(r'Sonidos\Game of Thrones.mp3')
    pygame.mixer.music.play(-1)
    volumen_musica = 0.5
    return pantalla, fondo_pantalla, volumen_musica

def cargar_plataformas(archivo):
    '''
    Carga las plataformas desde un archivo JSON.

    Args:
        archivo (str): La ruta del archivo JSON que contiene los datos de las plataformas.

    Returns:
        list: Una lista de objetos Plataforma.
    '''
    with open(archivo, 'r') as file:
        plataformas_data = json.load(file)
    plataformas = [Plataforma(data['x'], data['y'], data['ancho'], data['alto'], imagen_plataforma) for data in plataformas_data]
    return plataformas

def cargar_enemigos(archivo):
    '''
    Carga los enemigos desde un archivo CSV.

    Args:
        archivo (str): La ruta del archivo CSV que contiene los datos de los enemigos.

    Returns:
        list: Una lista de objetos Enemy.
    '''
    enemigos = []
    with open(archivo, newline='') as file:
        reader = csv.DictReader(file)
        for linea in reader:
            enemigo = Enemy(int(linea['x']), int(linea['y']), int(linea['start_x']), int(linea['end_x']), int(linea['speed']), int(linea['direccion']))
            enemigos.append(enemigo)
    return enemigos

def cargar_monedas(archivo):
    '''
    Carga las monedas desde un archivo JSON.

    Args:
        archivo (str): La ruta del archivo JSON que contiene los datos de las monedas.

    Returns:
        list: Una lista de objetos Moneda.
    '''
    with open(archivo, 'r') as file:
        monedas_data = json.load(file)
    monedas = [Moneda(data['x'], data['y']) for data in monedas_data]
    return monedas

def mostrar_texto(texto, fuente, color, superficie, x, y):
    '''
    Muestra un texto en la superficie especificada.

    Args:
        texto (str): El texto a mostrar.
        fuente (pygame.font.Font): La fuente del texto.
        color (tuple): El color del texto.
        superficie (pygame.Surface): La superficie donde se dibujara el texto.
        x (int): La coordenada x de la posicion del texto.
        y (int): La coordenada y de la posicion del texto.
    '''
    texto_surface = fuente.render(texto, True, color)
    texto_rect = texto_surface.get_rect()
    texto_rect.topleft = (x, y)
    superficie.blit(texto_surface, texto_rect)

def pantalla_inicio():
    '''
    Muestra la pantalla de inicio con las opciones para comenzar el juego, configurarlo o salir.
    '''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return
                elif event.key == pygame.K_2:  
                    pantalla_configuracion()
                elif event.key == pygame.K_3: 
                    pygame.quit()
                    sys.exit()

        pantalla.fill((0, 0, 0))
        fuente = pygame.font.Font(None, 36)
        texto_empezar = fuente.render("1. Empezar juego", True, (255, 255, 255))
        texto_configuracion = fuente.render("2. Configuración", True, (255, 255, 255))
        texto_salir = fuente.render("3. Salir", True, (255, 255, 255))
        pantalla.blit(texto_empezar, (ANCHO // 2 - texto_empezar.get_width() // 2, ALTO // 2 - 50))
        pantalla.blit(texto_configuracion, (ANCHO // 2 - texto_configuracion.get_width() // 2, ALTO // 2))
        pantalla.blit(texto_salir, (ANCHO // 2 - texto_salir.get_width() // 2, ALTO // 2 + 50))
        pygame.display.update()

def pantalla_configuracion():
    '''
    Muestra la pantalla de configuracion para ajustar el volumen de la musica.
    '''
    global volumen_musica
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    return
                elif event.key == pygame.K_UP: 
                    volumen_musica = min(1.0, volumen_musica + 0.1)
                    pygame.mixer.music.set_volume(volumen_musica)
                elif event.key == pygame.K_DOWN:  
                    volumen_musica = max(0.0, volumen_musica - 0.1)
                    pygame.mixer.music.set_volume(volumen_musica)

        pantalla.fill((0, 0, 0))
        fuente = pygame.font.Font(None, 36)
        texto_volumen = fuente.render(f'Volumen de Música: {int(volumen_musica * 100)}%', True, (255, 255, 255))
        texto_instrucciones = fuente.render('UP - Subir Volumen | DOWN - Bajar Volumen | ESC - Salir', True, (255, 255, 255))
        pantalla.blit(texto_volumen, (ANCHO // 2 - texto_volumen.get_width() // 2, ALTO // 2 - 50))
        pantalla.blit(texto_instrucciones, (ANCHO // 2 - texto_instrucciones.get_width() // 2, ALTO // 2))
        pygame.display.update()

def reiniciar_juego():
    '''
    Reinicia el juego cargando nuevamente el personaje, enemigos, plataformas y monedas.
    '''
    global arquero, enemigos, plataformas, monedas, jugando
    arquero = Personaje(40, 400)
    enemigos = cargar_enemigos('enemigos.csv')
    plataformas = cargar_plataformas('plataformas.json')
    monedas = cargar_monedas('Coin.json')
    jugando = True

def pantalla_pausa():
    '''
    Muestra la pantalla de pausa con opciones para reanudar o reiniciar el juego.
    '''
    pausado = True
    while pausado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pausado = False
                elif event.key == pygame.K_e:
                    reiniciar_juego()
                    pausado = False
                    return  

        pantalla.fill((0, 0, 0))
        fuente_titulo = pygame.font.Font(None, 74)
        texto_pausa = fuente_titulo.render("Pausa", True, (255, 255, 255))
        pantalla.blit(texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, ALTO // 4 - texto_pausa.get_height() // 2))

        fuente_instrucciones = pygame.font.Font(None, 36)
        texto_reanudar = fuente_instrucciones.render("P - Reanudar juego", True, (255, 255, 255))
        texto_reiniciar = fuente_instrucciones.render("E - Reiniciar juego", True, (255, 255, 255))
        pantalla.blit(texto_reanudar, (ANCHO // 2 - texto_reanudar.get_width() // 2, ALTO // 2))
        pantalla.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 50))

        pygame.display.update()

def mostrar_hud(pantalla):
    '''
    Muestra el HUD del juego, incluyendo el volumen de la música y el puntaje.

    Args:
        pantalla (pygame.Surface): La superficie de la ventana del juego.
    '''
    fuente_hud = pygame.font.Font(None, 36)
    mostrar_texto(f'Volumen: {int(volumen_musica * 100)}%', fuente_hud, (255, 255, 255), pantalla, 10, 50)
    font = pygame.font.SysFont(None, 36)
    score_text = font.render("Score: " + str(score), True, BLANCO)
    pantalla.blit(score_text, (500, 20))

def verificar_victoria(enemigos):
    '''
    Verifica si todos los enemigos han sido derrotados.

    Args:
        enemigos (list): Lista de objetos Enemy.

    Returns:
        bool: True si todos los enemigos estan derrotados, False en caso contrario.
    '''
    for enemigo in enemigos:
        if enemigo.esta_vivo():
            return False
    return True


pantalla, fondo_pantalla, volumen_musica = inicializar()
clock = pygame.time.Clock()
score = 0


arquero = Personaje(40, 400)
imagen_plataforma = pygame.image.load(r'Imagenes\Plataformas\NonSLiced.png')
plataformas = cargar_plataformas('plataformas.json')
enemigos = cargar_enemigos('enemigos.csv')
monedas = cargar_monedas('Coin.json')


pantalla_inicio()


jugando = True
while jugando:
    clock.tick(FPS)
    userInput = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pantalla_pausa()
            elif event.key == pygame.K_F1:
                volumen_musica = min(1.0, volumen_musica + 0.1)
                pygame.mixer.music.set_volume(volumen_musica)
            elif event.key == pygame.K_F2:
                volumen_musica = max(0.0, volumen_musica - 0.1)
                pygame.mixer.music.set_volume(volumen_musica)

    if arquero.hp <= 0:
        pygame.time.delay(1000)
        pantalla.fill((0, 0, 0))
        fuente = pygame.font.Font(None, 74)
        texto_game_over = fuente.render(f"Game Over Score:{score} ", True, (255, 0, 0))
        pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - texto_game_over.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        jugando = False
        continue

    arquero.mover_personaje(userInput, plataformas)
    arquero.saltar(userInput)
    arquero.sobre_plataforma(plataformas)
    arquero.disparar(userInput, enemigos)
    arquero.colision_con_enemigos(enemigos)

    pantalla.blit(fondo_pantalla, (0, 0))
    arquero.draw(pantalla)

    for flecha in arquero.flechas:
        flecha.draw_flecha(pantalla)

    for plataforma in plataformas:
        plataforma.draw(pantalla)

    for enemigo in enemigos[:]:
        enemigo.move()
        enemigo.draw(pantalla)
        if enemigo.hp <= 0:
            enemigo.vivo = False
            score += 100

    enemigos = [enemigo for enemigo in enemigos if enemigo.esta_vivo()]

    for moneda in monedas[:]:
        moneda.draw(pantalla)
        if arquero.colision.colliderect(moneda.colision):
            score += 50
            monedas.remove(moneda)

    mostrar_hud(pantalla)
    if verificar_victoria(enemigos):
        pantalla.fill((0, 0, 0))
        fuente = pygame.font.Font(None, 74)
        texto_victoria = fuente.render(f"¡Victoria! Score: {score}", True, (0, 255, 0))
        pantalla.blit(texto_victoria, (ANCHO // 2 - texto_victoria.get_width() // 2, ALTO // 2 - texto_victoria.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        jugando = False

    pygame.display.update()

pygame.quit()
