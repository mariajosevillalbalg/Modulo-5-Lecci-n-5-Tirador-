from pygame import *

# música de fondo
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# necesitamos estas imágenes:
img_back = "galaxy.jpg"  # fondo de juego
img_hero = "rocket.png"  # personaje


# clase padre para otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # llamamos al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)

        # cada objeto debe almacenar una propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # cada objeto debe almacenar la propiedad rect en la cual está inscrito
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método que dibuja al personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# clase del jugador principal
class Player(GameSprite):
    # método para controlar el objeto con las flechas del teclado
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # el método “fire” (usa la posición del jugador para crear una bala)
    def fire(self):
        pass


# Crea la ventana
win_width = 700
win_height = 500
display.set_caption("Tirador")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# crea objetos
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# la variable de “juego terminado”: cuando es True, los objetos dejan de funcionar en el ciclo principal
finish = False
# Ciclo de juego principal:
run = True  # la bandera es limpiada con el botón de cerrar ventana
while run:
    # el evento de pulsación del botón Cerrar
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        # actualizar fondo
        window.blit(background, (0, 0))

        # produciendo los movimientos del objeto
        ship.update()

        # los actualiza en una nueva ubicación en cada iteración del ciclo
        ship.reset()

        display.update()
    # el ciclo se ejecuta cada 0.05 segundos
    time.delay(50)
