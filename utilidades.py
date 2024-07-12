import pygame

pygame.mixer.init()

# Intentar cargar el sonido y manejar excepciones
try:
    golpe_sonido = pygame.mixer.Sound(r'Sonidos\RPGSFX - 64 hit 1.ogg')
except pygame.error as e:
    print(f"Error al cargar el sonido: {e}")
    golpe_sonido = None

