import pygame
import random

WIDTH = 600
HEIGHT = 1040
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()


def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player1.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, - 100)
            self.speedy = random.randrange(1, 10)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/blackHoleVideoGame.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def show_go_screen():
    screen.blit(background_level1, [0, 0])
    draw_text(screen, "TO THE STARS", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "A super advanced spaceship that shoots black holes", 27, WIDTH // 2, HEIGHT // 2.6)
    draw_text(screen, "must destroy all the planets, stars and comets", 27, WIDTH // 2, HEIGHT // 2.3)
    draw_text(screen, "that come close to it to stay alive!", 27, WIDTH // 2, HEIGHT // 2.05)
    draw_text(screen, "Press Space", 30, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def show_end_screen():
    screen.blit(background_level3, [0, 0])
    draw_text(screen, "GAME OVER", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, f"Score: {score}", 30, WIDTH // 2, HEIGHT // 2)

    restart_button = pygame.Rect(WIDTH // 5, HEIGHT * 3/5, 150, 50)
    pygame.draw.rect(screen, BLACK, restart_button)
    draw_text(screen, "Reiniciar", 30, WIDTH / 3.1, HEIGHT * 3/4.99)


    quit_button = pygame.Rect(WIDTH //2, HEIGHT * 3 / 5, 150, 50)
    pygame.draw.rect(screen, BLACK, quit_button)
    draw_text(screen, "Salir", 28, quit_button.centerx, HEIGHT * 3/4.99)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_x, mouse_y):
                    # Reiniciar el juego
                    return True
                elif quit_button.collidepoint(mouse_x, mouse_y):
                    # Salir del juego
                    pygame.quit()
        clock.tick(60)


meteor_images = []
meteor_list = ["assets/SaturnoVideoGame.png", "assets/SunVideoGame.png", "assets/bluePlanetVideoGame.png",
               "assets/bluePlanetVideoGame.png",
               "assets/CometVideoGame.png", "assets/SaturnoVideoGame.png", "assets/CometVideoGame.png",
               "assets/CometVideoGame.png",
               "assets/SunVideoGame.png", "assets/CometVideoGame.png", "assets/bluePlanetVideoGame.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())


explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)


background_level1 = pygame.image.load("assets/back1.jpg").convert()
background_level2 = pygame.image.load("assets/back2.jpg").convert()
background_level3 = pygame.image.load("assets/back3.jpg").convert()

background_level1 = pygame.transform.scale(background_level1, (WIDTH, HEIGHT))
background_level2 = pygame.transform.scale(background_level2, (WIDTH, HEIGHT))
background_level3 = pygame.transform.scale(background_level3, (WIDTH, HEIGHT))

player_images = [pygame.image.load("assets/player1.png").convert(),
                 pygame.image.load("assets/player1.png").convert(),
                 pygame.image.load("assets/player1.png").convert()]

bullet_images = [pygame.image.load("assets/blackHoleVideoGame.png").convert(),
                 pygame.image.load("assets/blackHoleVideoGame.png").convert(),
                 pygame.image.load("assets/blackHoleVideoGame.png").convert()]


game_over = True
running = True
score = 0
level = 1
num_meteors = 15
restart_game = False

while running:
    if score >= 3000:
        restart_game = show_end_screen()
        if restart_game:
            game_over = True
            score = 0

    if game_over:

            show_go_screen()
            game_over = False
            all_sprites = pygame.sprite.Group()
            meteor_list = pygame.sprite.Group()
            bullets = pygame.sprite.Group()

            player = Player()
            all_sprites.add(player)

            for i in range(num_meteors):
                meteor = Meteor()
                all_sprites.add(meteor)
                meteor_list.add(meteor)

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10

        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 25
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True
            score = 0
            level = 1

    if score >= 1000 and level < 3:
        level = 2

    if score >= 2000:
        level = 3

    if level == 1:
        screen.blit(background_level1, [0, 0])
        player.image = player_images[level - 1]
        player.image.set_colorkey(BLACK)
        bullets.image = bullet_images[level - 1]
        bullets.image.set_colorkey(BLACK)

    elif level == 2:
        screen.blit(background_level2, [0, 0])
        player.image = player_images[level - 1]
        player.image.set_colorkey(BLACK)
        bullets.image = bullet_images[level - 1]
        bullets.image.set_colorkey(BLACK)
    elif level == 3:
        screen.blit(background_level3, [0, 0])
        player.image = player_images[level - 1]
        player.image.set_colorkey(BLACK)
        bullets.image = bullet_images[level - 1]
        bullets.image.set_colorkey(BLACK)

    all_sprites.draw(screen)

    # Marcador
    draw_text(screen, f"Level: {level}", 25, 70, 10)
    draw_text(screen, f"Score: {score}", 25, WIDTH // 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()

pygame.quit()


