# --------------------- Controles ---------------------
"""

    W,A,S,D - move o personagem
    Espaço - Tp
    Mouse - mira
    M1/M2 - Ataque leve, Absorção
    
"""

# --------------------- Bibliotecas ---------------------

import sys
import pygame
import random
import math
from pygame.math import Vector2

# --------------------- Configurações ---------------------

resolucoes = { "1": { "width": 800, "height": 600}, "2": { "width": 1024, "height": 768, } }

# --------------------- Variaveis ---------------------


clock = pygame.time.Clock()
FPS = 60
TITULO = "Tpy"
COR_PLAYER = (0, 180, 180)
COR_FUNDO = (200, 200, 200)
COR_UI = (0, 120, 90)


# --------------------- Classes ---------------------

class main:
    def __init__(player):
        player.w = 20
        player.h = 20
        player.r = 5
        


# --------------------- Main ---------------------