import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Game.py/assets").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.botton = HEIGHT - 10
        self.seepd_x = 0

    def update(self):
        self.seepd_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.seepd_x = -5
        if keystate[pygame.K_RIGHT]:
            self.seepd_x = 5
        self.rect.x += self.seepd_x


all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.quit():
            running = False
    all_sprites.update()
    screen.fill(BLACK)
    pygame.display.flip()

pygame.quit()
