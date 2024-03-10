import pygame

WIDTH, HEIGHT = 775, 775
FPS = 60
bg_y = 0
position_x = {
    "alien": WIDTH // 10,
    "shield": WIDTH // 10,
}
position_y = {
    "green": HEIGHT // 2.25,
    "yellow": HEIGHT // 4,
    "red": HEIGHT // 5.25,
}
font_consolas = pygame.font.match_font("consolas")
score = 0
lives = 3


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/player.png").convert()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.radius = 30
        self.rect.center = (WIDTH // 2, 750)
        self.speed_x = 0
        self.can_shoot = True

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.speed_x -= 10
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.speed_x += 10

        if keys[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speed_x

    def shoot(self):
        if self.can_shoot:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            shoot_sound.play()
            self.can_shoot = False


class Alien(pygame.sprite.Sprite):
    def __init__(self, color_alien: str, move_y=0):
        super().__init__()
        global position_x, position_y
        self.color = color_alien
        self.image = pygame.image.load(f"img/{color_alien}.png").convert()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.radius = 20

        position_x["alien"] += WIDTH // 10
        if position_x["alien"] > WIDTH - self.rect.width:
            position_x["alien"] = WIDTH // 10 + WIDTH // 10
            position_y[f"{color_alien}"] += HEIGHT // 15 + move_y

        self.rect.center = (position_x["alien"] - self.rect.width, position_y[f"{color_alien}"] - self.rect.height)
        self.speed_x = 1
        self.speed_y = 0
        self.can_shoot = False
        self.speed_bullet = 2

    def move_x(self):
        self.speed_x = abs(self.speed_x)
        self.rect.x += self.speed_x

    def move_y(self):
        self.speed_y = 3
        self.rect.y += self.speed_y

    def reverse_x(self):
        self.speed_x *= -1
        self.rect.x += self.speed_x

    def shoot(self):
        if self.can_shoot:
            if self.color == "yellow":
                self.speed_bullet = 4
            elif self.color == "red":
                self.speed_bullet = 6
            alien_bullet = AlienBullets(self.rect.centerx, self.rect.bottom, self.speed_bullet)
            alien_bullets.add(alien_bullet)
            shoot_sound.play()
            self.can_shoot = False

    def explosion(self):
        self.image = pygame.image.load("img/explosion.png")
        self.image.set_colorkey("black")
        return pygame.time.get_ticks()


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(f"img/bullet.png").convert(), (5, 30))
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.y -= 3
        if self.rect.bottom == 0:
            self.kill()


class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, speed: int):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(f"img/bullet.png").convert(), (5, 30))
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.top = y
        self.rect.centerx = x
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top == HEIGHT:
            self.kill()


class Shield(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global position_x, position_y
        self.life = 20
        self.image = pygame.image.load(f"img/shield-1.png").convert()
        self.rect = self.image.get_rect()
        self.radius = 50

        position_x["shield"] += WIDTH // 12 + self.rect.width

        self.rect.center = (position_x["shield"] - self.rect.width, 700 - self.rect.height)
        self.speed_x = 0
        self.speed_y = 0
        self.play_music = [True, True, True, True]

    def update(self):
        if self.life <= 14:
            if self.play_music[0]:
                kill_shield.play()
                self.play_music[0] = False
            self.image = pygame.image.load(f"img/shield-2.png").convert()

        if self.life <= 8:
            if self.play_music[1]:
                kill_shield.play()
                self.play_music[1] = False
            self.image = pygame.image.load(f"img/shield-3.png").convert()

        if self.life <= 2:
            if self.play_music[2]:
                kill_shield.play()
                self.play_music[2] = False
            self.image = pygame.image.load(f"img/shield-4.png").convert()

        if self.life <= 0:
            if self.play_music[3]:
                kill_shield.play()
                self.play_music[3] = False
            self.kill()


class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/extra.png").convert()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.center = WIDTH + self.rect.width, 100
        self.speed_x = 2

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right <= 0:
            self.kill()

    def shoot(self):
        if self.can_shoot:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            shoot_sound.play()
            self.can_shoot = False


def show_text(text: str, x: int, y: int):
    type_font = pygame.font.Font(font_consolas, 40)
    font = type_font.render(text, False, "white")
    rect = font.get_rect()
    rect[0], rect[1] = x, y
    screen.blit(font, rect)


pygame.init()

clock = pygame.time.Clock()

# Images
icon = pygame.image.load("img/icon.png")
bg = pygame.image.load("img/bg.png")

# Sounds
pygame.mixer.init()
bg_sound = pygame.mixer.Sound("audio/bg.mp3")
# bg_sound.play(-1)
extra_life = pygame.mixer.Sound("audio/extra-life.wav")
shoot_sound = pygame.mixer.Sound("audio/shoot.wav")
shoot_shield = pygame.mixer.Sound("audio/shoot-shield.wav")
kill_alien = pygame.mixer.Sound("audio/kill-alien.wav")
kill_shield = pygame.mixer.Sound("audio/kill-shield.wav")
kill_player = pygame.mixer.Sound("audio/kill-player.wav")
kill_extra = pygame.mixer.Sound("audio/kill-extra.wav")

# Screen
set_screen = pygame.display
set_screen.set_caption("Space Invaders")
set_screen.set_icon(icon)

screen = set_screen.set_mode((WIDTH, HEIGHT))

# Sprites
player = pygame.sprite.Group()
aliens = pygame.sprite.Group()
shields = pygame.sprite.Group()
bullets = pygame.sprite.Group()
alien_bullets = pygame.sprite.Group()
sprites = [player, aliens, shields, bullets, alien_bullets]

for green_alien in range(16):
    sprite_alien = Alien("green")
    aliens.add(sprite_alien)
for yellow_alien in range(16):
    sprite_alien = Alien("yellow")
    aliens.add(sprite_alien)
for red_alien in range(8):
    sprite_alien = Alien("red")
    aliens.add(sprite_alien)

for shield in range(4):
    sprite_shield = Shield()
    shields.add(sprite_shield)

ship = Player()
player.add(ship)

# Set Conditionals
move = False
move_y = 0

rise_life = True

run = True
exit_game = True
last_time_ufo = pygame.time.get_ticks()
last_time_green = pygame.time.get_ticks()
last_time_yellow = pygame.time.get_ticks()
last_time_red = pygame.time.get_ticks()
last_time_explosion = None

time_ufo_extra = 20000
bullet_green = 2000
bullet_yellow = 5000
bullet_red = 11000
explosion = 500

while run:
    clock.tick(FPS)

    time_ufo = pygame.time.get_ticks()
    time_green = pygame.time.get_ticks()
    time_yellow = pygame.time.get_ticks()
    time_red = pygame.time.get_ticks()
    time_explosion = pygame.time.get_ticks()

    if time_ufo - last_time_ufo >= time_ufo_extra:
        player.add(Ufo())
        last_time_ufo = time_ufo

    if time_green - last_time_green >= bullet_green:
        number = 0
        for alien in aliens:
            if alien.color == "green" and number % 3 == 0:
                alien.can_shoot = True
                alien.shoot()
                alien.can_shoot = False
            number += 1
        last_time_green = time_green

    if time_yellow - last_time_yellow >= bullet_yellow:
        number = 0
        for alien in aliens:
            if alien.color == "yellow" and number % 5 == 0:
                alien.can_shoot = True
                alien.shoot()
                alien.can_shoot = False
            number += 1
        last_time_yellow = time_yellow

    if time_red - last_time_red >= bullet_red:
        number = 0
        for alien in aliens:
            if alien.color == "red" and number % 6 == 0:
                alien.can_shoot = True
                alien.shoot()
                alien.can_shoot = False
            number += 1
        last_time_red = time_red

    # Exit Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            exit_game = True

    # Movement Aliens
    for alien in aliens:
        if alien.rect.x + alien.rect.width >= WIDTH:
            move = True
        elif alien.rect.x <= 0:
            move = False
            for sprite in aliens:
                sprite.move_y()
        if move:
            alien.reverse_x()
        if not move:
            alien.move_x()

    alien_speed = 1
    if 21 <= len(aliens) <= 30:
        alien_speed = 2
        bullet_green = 1500
        bullet_yellow = 4000
        bullet_red = 9000
    elif 11 <= len(aliens) <= 20:
        alien_speed = 3
        bullet_green = 1000
        bullet_yellow = 3000
        bullet_red = 7000
    elif 1 <= len(aliens) <= 10:
        alien_speed = 4
        bullet_green = 7500
        bullet_yellow = 2000
        bullet_red = 5000
    for alien in aliens:
        alien.speed_x = alien_speed

    # Movement Background
    height_bg = bg.get_rect().height
    relative_y = bg_y % height_bg
    screen.blit(bg, (0, relative_y - height_bg))
    if relative_y < HEIGHT:
        screen.blit(bg, (0, relative_y))
    bg_y += 1

    # Collision Objets
    collision_alien = pygame.sprite.groupcollide(bullets, aliens, True, False)
    collision_bullets_aliens_shields = pygame.sprite.groupcollide(alien_bullets, shields, True, False)
    collision_bullets = pygame.sprite.groupcollide(bullets, alien_bullets, True, True)
    collision_player = pygame.sprite.groupcollide(player, alien_bullets, True, True)
    collision_alien_to_player = pygame.sprite.groupcollide(player, aliens, True, True)
    collision_alien_to_shields = pygame.sprite.groupcollide(aliens, shields, True, True)

    try:
        bull = list(collision_alien_to_shields)[0]
        collision_alien_to_shields[bull][0].life -= 1
        kill_alien.play()
    except IndexError:
        pass

    if collision_alien_to_player:
        run = False

    try:
        bull = list(collision_bullets_aliens_shields)[0]
        collision_bullets_aliens_shields[bull][0].life -= 1
    except IndexError:
        pass

    if collision_player:
        lives -= 1
        kill_player.play()
        player.add(ship)

    if collision_bullets:
        ship.can_shoot = True

    for bullet in bullets:
        if bullet.rect.bottom <= 10:
            ship.can_shoot = True

    if collision_alien:
        ship.can_shoot = True
        grab_alien = collision_alien
        kill_alien.play()
    if last_time_explosion is not None:
        if time_explosion - last_time_explosion >= explosion:
            bull = list(grab_alien)[0]
            grab_alien[bull][0].kill()
            last_time_explosion = time_explosion
    collision_shields = pygame.sprite.groupcollide(bullets, shields, True, False)

    if collision_shields:
        ship.can_shoot = True
        shoot_shield.play()

    collision_ufo = pygame.sprite.groupcollide(bullets, player, True, True)

    if collision_ufo:
        kill_extra.play()
        score += 100

    # Handle Scoreboard
    try:
        bull = list(collision_alien)[0]
        last_time_explosion = collision_alien[bull][0].explosion()
        if collision_alien[bull][0].color == "green":
            score += 10
        if collision_alien[bull][0].color == "yellow":
            score += 20
        if collision_alien[bull][0].color == "red":
            score += 40
    except IndexError:
        pass

    if rise_life:
        if score >= 600:
            lives += 1
            rise_life = False
            extra_life.play()

    # Win - Lose Logic
    if len(aliens) == 0 or lives == 0:
        run = False

    # Update Scoreboard
    show_text(str(score).zfill(4), 40, 20)

    # Update Lives
    show_text(str(lives), 700, 20)

    # Update Group Sprites and Screen
    for sprite in sprites:
        sprite.update()
        sprite.draw(screen)

    set_screen.flip()

pygame.quit()
