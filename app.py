import pygame
import sys
import random



WIDTH, HEIGHT = 800, 800
FPS = 60
PLAYER_SPEED = 5
ENEMY_SPEED = 1
BULLET_SPEED = 5
ENEMY_FIRE_RATE = 3000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Battle")
clock = pygame.time.Clock()

player_explosion_sound = pygame.mixer.Sound("sounds/explode.wav")


def show_intro_screen(screen):
    intro_background = pygame.image.load("images/intro_bg.png").convert()
    intro_background = pygame.transform.scale(intro_background, (WIDTH, HEIGHT))

    font_instructions = pygame.font.Font(None, 36)

    instruction_text2 = font_instructions.render("Press any key to start", True, BLACK)

    text_rect_instruction2 = instruction_text2.get_rect(midbottom=(WIDTH // 2, HEIGHT - 150))

    screen.blit(intro_background, (0, 0))
    screen.blit(instruction_text2, text_rect_instruction2)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return




class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, initial_pos, controls):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = initial_pos
        self.speed = PLAYER_SPEED
        self.controls = controls
        self.lives = 3
        self.exploded = False
        self.explosion_sound = pygame.mixer.Sound("sounds/explode.wav")  # Initialize explosion sound


    def update(self):
        if not self.exploded:
            keys = pygame.key.get_pressed()

            if keys[self.controls[0]] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[self.controls[1]] and self.rect.right < WIDTH:
                self.rect.x += self.speed
            if keys[self.controls[2]] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[self.controls[3]] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed

    def shoot(self):
        if not self.exploded:
            bullet = Bullet(self.rect.centerx, self.rect.top, -BULLET_SPEED)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    def explode(self):
        self.exploded = True
        self.explosion_sound.set_volume(0.3)  # Set volume level (0.0 to 1.0)
        self.explosion_sound.play()
        self.image = pygame.Surface((0, 0))
        self.kill()

    def is_exploded(self):
        return self.exploded


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/enemy.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-HEIGHT, -self.rect.height)
        self.speed = ENEMY_SPEED
        self.last_fire = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-HEIGHT, -self.rect.height)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)

        now = pygame.time.get_ticks()
        if now - self.last_fire > ENEMY_FIRE_RATE:
            self.last_fire = now
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/enemy_bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.explosion_images = []
        for i in range(9):
            img = pygame.image.load(f"images/explosion{str(i)}.png").convert_alpha()
            img = pygame.transform.scale(img, (100, 100))
            self.explosion_images.append(img)
        self.image = self.explosion_images[0]
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
            if self.frame == len(self.explosion_images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Score:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.high_score = 0
        self.load_high_score()

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (600, 10))

    def update(self, value):
        self.score += value
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def reset(self):
        self.score = 0

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))


scoreboard = Score()

player1 = Player("images/player.png", (WIDTH // 2, HEIGHT - 20), [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s])
player2 = Player("images/player2.png", (WIDTH // 2, HEIGHT - 100),
                 [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN])

all_sprites = pygame.sprite.Group(player1, player2)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
enemy_hit_sound = pygame.mixer.Sound("sounds/enemyhit.wav")
game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")


def reset_game():
    global all_sprites, enemies, bullets, enemy_bullets, scoreboard, player1, player2

    scoreboard.reset()

    player1 = Player("images/player.png", (WIDTH // 2, HEIGHT - 20), [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s])
    player2 = Player("images/player2.png", (WIDTH // 2, HEIGHT - 100),
                     [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN])
    player1.lives = 3
    player2.lives = 3

    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    enemy_bullets.empty()

    all_sprites.add(player1, player2)
    for _ in range(10):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)


def game_over_screen(screen, scoreboard):
    game_over_sound.set_volume(0.6)  # Adjust volume level for game over sound
    game_over_sound.play()

    background_image = pygame.image.load("images/gamebg.png").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    font_game_over = pygame.font.Font(None, 80)
    font_instruction = pygame.font.Font(None, 30)

    text_game_over = font_game_over.render("Game Over", True, (255, 0, 0))
    text_instruction = font_instruction.render("Press Enter to play again", True, (255, 255, 255))
    text_quit = font_instruction.render("Press Escape to quit", True, (255, 255, 255))
    text_score = font_instruction.render(f"Score: {scoreboard.score}", True, (255, 255, 255))
    text_high_score = font_instruction.render(f"High Score: {scoreboard.high_score}", True, (255, 255, 255))

    text_rect_game_over = text_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    text_rect_instruction = text_instruction.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_rect_quit = text_quit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    text_rect_score = text_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    text_rect_high_score = text_high_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

    screen.blit(background_image, (0, 0))

    screen.blit(text_game_over, text_rect_game_over)
    screen.blit(text_instruction, text_rect_instruction)
    screen.blit(text_quit, text_rect_quit)
    screen.blit(text_score, text_rect_score)
    screen.blit(text_high_score, text_rect_high_score)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False



def collide_mask(sprite1, sprite2):
    return pygame.sprite.collide_mask(sprite1, sprite2) is not None


player1_life_img = pygame.image.load("images/live_icon.png").convert_alpha()
player2_life_img = pygame.image.load("images/live_icon.png").convert_alpha()


def draw_lives_indicators(screen, player1, player2):
    for i in range(player1.lives):
        x_pos = WIDTH // 10 - 40 * i
        y_pos = 70
        screen.blit(player1_life_img, (x_pos, y_pos))

    for i in range(player2.lives):
        x_pos = WIDTH * 9.5 // 10 - 40 * i
        y_pos = 70
        screen.blit(player2_life_img, (x_pos, y_pos))

    scoreboard.draw(screen)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.explosion_images = []
        for i in range(9):
            img = pygame.image.load(f"explosion/regularExplosion{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (100, 100))
            self.explosion_images.append(img)
        self.image = self.explosion_images[0]
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
            if self.frame == len(self.explosion_images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AirCraft War")

    show_intro_screen(screen)

    background_image1 = pygame.image.load("images/bg.png").convert()
    background_image1 = pygame.transform.scale(background_image1, (WIDTH, HEIGHT))

    background_image2 = pygame.image.load("images/bg.png").convert()
    background_image2 = pygame.transform.scale(background_image2, (WIDTH, HEIGHT))
    background_y2 = -HEIGHT

    background_y = 0

    for _ in range(10):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    explosions = pygame.sprite.Group()

    running = True
    while running:
        clock.tick(FPS)

        background_y += 1
        background_y2 += 1

        screen.blit(background_image1, (0, background_y))
        screen.blit(background_image2, (0, background_y2))

        if background_y >= HEIGHT:
            background_y = -HEIGHT

        if background_y2 >= HEIGHT:
            background_y2 = -HEIGHT

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.shoot()
                elif event.key == pygame.K_RETURN:
                    if player1.lives <= 0 and player2.lives <= 0:
                        reset_game()
                        main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player2.shoot()

        all_sprites.update()
        explosions.update()

        hits_player1_bullet = pygame.sprite.groupcollide(bullets, enemies, True, True, collide_mask)
        for hit in hits_player1_bullet:
            enemy_hit_sound.play()
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            explosions.add(explosion)
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            scoreboard.update(10)

        if player1.alive and not player1.is_exploded():
            player_hit_by_enemy_bullet = pygame.sprite.spritecollide(player1, enemy_bullets, True, collide_mask)
            if player_hit_by_enemy_bullet:
                player1.lives -= 1
                if player1.lives <= 0:
                    explosion = Explosion(player1.rect.center)
                    all_sprites.add(explosion)
                    explosions.add(explosion)
                    player1.explode()

        if player2.alive and not player2.is_exploded():
            player2_hit_by_enemy_bullet = pygame.sprite.spritecollide(player2, enemy_bullets, True, collide_mask)
            if player2_hit_by_enemy_bullet:
                player2.lives -= 1
                if player2.lives <= 0:
                    explosion = Explosion(player2.rect.center)
                    all_sprites.add(explosion)
                    explosions.add(explosion)
                    player2.explode()

        if player1.lives <= 0 and player2.lives <= 0:
            if not any(explosion.alive() for explosion in explosions):
                running = game_over_screen(screen, scoreboard)

        # Remove screen.fill((0, 0, 0)) to keep the background images
        all_sprites.draw(screen)
        draw_lives_indicators(screen, player1, player2)
        pygame.display.flip()

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()
