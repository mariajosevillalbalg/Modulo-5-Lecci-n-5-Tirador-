from pygame import *
from random import randint
from time import time as timer  # Para manejar la recarga

# Inicialización de fuente
font.init()
font1 = font.Font(None, 36)

# Carga de imágenes
img_ast    = "asteroid.png"  # Obstáculos
img_back   = "galaxy.jpg"    # Fondo del juego
img_hero   = "rocket.png"    # Jugador
img_enemy  = "ufo.png"       # Enemigos
img_bullet = "bullet.png"    # Balas

# Variables del juego
score     = 0       # Puntos por enemigos destruidos
lost      = 0       # Enemigos que pasan
goal      = 10      # Puntos necesarios para ganar
max_lost  = 3       # Caídas permitidas antes de perder
life      = 3       # Vidas del jugador

num_fire  = 0       # Contador de disparos consecutivos
rel_time  = False   # Bandera de recarga activa
last_time = 0       # Marca de tiempo cuando inicia recarga

# Configuración de la ventana
win_width  = 700
win_height = 500
window     = display.set_mode((win_width, win_height))
display.set_caption("Tirador")
background = transform.scale(image.load(img_back), (win_width, win_height))

# Clase base para todos los sprites
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.speed = speed
        self.rect  = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Clase del jugador
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        global num_fire, rel_time, last_time
        # Corrección: limitar a 5 disparos antes de recargar
        if num_fire < 5 and not rel_time:
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
            fire_sound.play()
            num_fire += 1
        # Cuando alcanza 5 disparos, inicia recarga de 3 segundos
        if num_fire >= 5 and not rel_time:
            rel_time  = True
            last_time = timer()

# Clase para enemigos y asteroides (misma lógica de movimiento)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1  # Conteo de enemigos fallados

# Clase de balas
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()  # Elimina la bala fuera de pantalla

# Grupos de sprites
monsters  = sprite.Group()
for i in range(5):
    m = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(m)

asteroids = sprite.Group()
for i in range(3):
    a = Enemy(img_ast, randint(30, win_width), -40, 80, 50, randint(1, 7))
    asteroids.add(a)

bullets   = sprite.Group()
ship      = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# Sonido
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")  # Uso correcto de Sound

# Bucle principal
run   = True
finish = False
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            ship.fire()  # Disparo encapsulado en el método fire()

    if not finish:
        window.blit(background, (0, 0))

        # Actualiza y dibuja jugador
        ship.update()
        ship.reset()

        # Actualiza y dibuja enemigos y asteroides
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)

        # Actualiza y dibuja balas
        bullets.update()
        bullets.draw(window)

        # Lógica de recarga
        if rel_time:
            now = timer()
            if now - last_time < 3:
                text = font1.render("Espera, recargando...", True, (255, 0, 0))
                window.blit(text, (250, 460))
            else:
                num_fire = 0
                rel_time  = False

        # Colisiones bala-enemigo
        hits = sprite.groupcollide(monsters, bullets, True, True)
        for _ in hits:
            score += 1
            new = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(new)

        # Colisiones jugador-enemigo/asteroide
        if sprite.spritecollide(ship, monsters, True) or sprite.spritecollide(ship, asteroids, True):
            life -= 1  # Disminuye vida al colisionar

        # Condición de derrota
        if life <= 0 or lost >= max_lost:
            finish = True
            text = font1.render("¡PERDISTE!", True, (255, 0, 0))
            window.blit(text, (250, 250))

        # Condición de victoria
        if score >= goal:
            finish = True
            text = font1.render("¡GANASTE!", True, (0, 255, 0))
            window.blit(text, (250, 250))

        # HUD: puntaje, fallados y vidas
        txt_score = font1.render(f"Puntaje: {score}", True, (255, 255, 255))
        txt_lost  = font1.render(f"Fallados: {lost}", True, (255, 255, 255))
        txt_life  = font1.render(f"Vidas: {life}", True, (0, 255, 0))
        window.blit(txt_score, (10, 20))
        window.blit(txt_lost, (10, 50))
        window.blit(txt_life, (10, 80))

        display.update()
        clock.tick(60)
