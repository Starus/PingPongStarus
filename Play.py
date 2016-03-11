#!/usr/bin/env python
# -*- coding: utf-8 -*-

#RETO Starus ent.

# Módulos
import sys, pygame, pygame.mixer
from pygame.locals import *
 
# Constantes
# ---------------------------------------------------------------------
WIDTH = 640
HEIGHT = 480
sonido_pared = "sonds/Ping_Pong_Ball_pared.mp2"
sonido_paleta = "sonds/Ping_Pong_Ball_paleta.mp2"
# ---------------------------------------------------------------------
# Clases
# ---------------------------------------------------------------------

class Bola(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/bola.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [0.35, -0.35]

    def actualizar(self, time, pala_jug1, pala_jug2, puntos):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0:
            puntos[1] += 1

        if self.rect.right >= WIDTH:
            puntos[0] += 1

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
            pygame.mixer.music.load(sonido_pared)
            pygame.mixer.music.play()

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
            pygame.mixer.music.load(sonido_pared)
            pygame.mixer.music.play()

        if pygame.sprite.collide_rect(self, pala_jug1):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
            pygame.mixer.music.load(sonido_paleta)
            pygame.mixer.music.play()

        if pygame.sprite.collide_rect(self, pala_jug2):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
            pygame.mixer.music.load(sonido_paleta)
            pygame.mixer.music.play()

        return puntos

class PalaP1(pygame.sprite.Sprite):

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/PaletaPj1.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.35

    def mover(self, time, keys):
        if self.rect.top >= 0:
            if keys[K_w]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_s]:
                self.rect.centery += self.speed * time

class PalaP2(pygame.sprite.Sprite):

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/PaletaPj2.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.35

    def mover(self, time, keys):
        if self.rect.top >= 0:
            if keys[K_w]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_s]:
                self.rect.centery += self.speed * time

    def ia(self, time, bola):
        if bola.speed[0] >= 0 and bola.rect.centerx >= WIDTH/2:
            if self.rect.centery < bola.rect.centery:
                self.rect.centery += self.speed * time
            if self.rect.centery > bola.rect.centery:
                self.rect.centery -= self.speed * time

# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------

def load_image(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image

def texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font("images/DroidSans.ttf", 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
 
# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PingPong - RETO starus")
    background_image = load_image('images/fondo.jpg')
    
    bola = Bola()
    pala_jug1 = PalaP1(20)
    pala_jug2 = PalaP2(WIDTH - 20)
    clock = pygame.time.Clock()
    puntos = [0, 0]

    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
 
        puntos = bola.actualizar(time,pala_jug1, pala_jug2, puntos)
        pala_jug1.mover(time, keys)
        pala_jug2.ia(time, bola)

        p_jug1, p_jug1_rect = texto(str(puntos[0]), WIDTH/4, 40)
        p_jug2, p_jug2_rect = texto(str(puntos[1]), WIDTH-WIDTH/4, 40)

        screen.blit(background_image, (0, 0))
        screen.blit(p_jug1, p_jug1_rect)
        screen.blit(p_jug2, p_jug2_rect)
        #screen.fill((255, 255 ,255)) ##blanco
        
        # Fonde de color
        screen.blit(bola.image, bola.rect)
        screen.blit(pala_jug1.image, pala_jug1.rect)
        screen.blit(pala_jug2.image, pala_jug2.rect)

        pygame.display.flip()

    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()
