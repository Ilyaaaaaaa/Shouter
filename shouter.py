from pygame import *
from random import randint, choice

class SpaceObject(sprite.Sprite):
    def __init__(self, img_file, pos_x, pos_y, obj_width, obj_height, obj_speed):
        super().__init__()
        self.image = transform.scale(image.load(img_file), (obj_width, obj_height))
        self.speed = obj_speed
        self.rect = (self.image.get_rect())
        self.rect.x = pos_x
        self.rect.y = pos_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Spaceship(SpaceObject):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 10 or keys[K_a] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < screen_width - 80 or keys[K_d] and self.rect.x < screen_width - 80:
            self.rect.x += self.speed

    def shoot(self):
        global ability_type, shot_count, is_ability_active
        if not is_ability_active:
            if ability_type == 3 and shot_count < 120:
                projectile = Projectile("bullet.png", self.rect.centerx - 4, self.rect.top - 15, 8, 15, 3)
                projectiles.add(projectile)
                shoot_sound.play()
            elif ability_type == 6 and shot_count < 120:
                projectile = Projectile("bullet.png", self.rect.centerx - 12, self.rect.top - 45, 24, 45, 30)
                projectiles.add(projectile)
                shoot_sound.play()
            elif ability_type == 8 and shot_count < 120:
                projectile1, projectile2, projectile3 = Projectile("bullet.png", self.rect.centerx - 35, self.rect.top - 15, 8, 15, 30), Projectile("bullet.png", self.rect.centerx - 4, self.rect.top - 15, 8, 15, 30), Projectile("bullet.png", self.rect.centerx + 31, self.rect.top - 15, 8, 15, 30)
                projectiles.add(projectile1, projectile2, projectile3)
                shoot_sound.play()
            elif ability_type == 700:
                projectile1, projectile2, projectile3 = Projectile("bullet.png", self.rect.centerx - 35, self.rect.top - 45, 24, 45, 3), Projectile("bullet.png", self.rect.centerx - 12, self.rect.top - 45, 24, 45, 3), Projectile("bullet.png", self.rect.centerx + 11, self.rect.top - 45, 24, 45, 3)
                projectiles.add(projectile1, projectile2, projectile3)
                shoot_sound.play()
            elif shot_count < 120:
                projectile = Projectile("bullet.png", self.rect.centerx - 4, self.rect.top - 15, 8, 15, 30)
                projectiles.add(projectile)
                shoot_sound.play()
            if ability_type == 7 or ability_type == 700:
                shot_count = 0
            elif shot_count < 120:
                shot_count += 1
            

class Projectile(SpaceObject):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -15:
            self.kill()

class Alien(SpaceObject):
    def update(self):
        global missed_count, ability_type
        self.rect.y += self.speed
        if self.rect.y >= screen_height:
            self.rect.y = -80
            self.speed = choice([1, 1.5, 2, 2.5])
            self.rect.x = randint(0, screen_width - 80)
            if ability_type != 2:
                missed_count += 1

class SpaceRock(SpaceObject):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x <= -2500:
            self.rect.x = screen_width + 1500

game_over = False
is_game_active = True
is_ability_active = False
is_paused = False
is_resetting = False
ability_duration = 0
ability_type = 0
shot_count = 0
temp_var = 0
score = 0
missed_count = 0
high_score = 0
initial_x = 0
alien_list = []
projectile_list = []
rock_list = []
projectile_list = []
health = 3
window = display.set_mode((1736, 1072))
screen_width, screen_height = window.get_size()
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (screen_width, screen_height))
player_spaceship = Spaceship("rocket.png", screen_width / 2 - 35, screen_height - 90, 70, 90, 10)
projectiles = sprite.Group()
aliens = sprite.Group()

for i in range(8):
    alien = Alien("ufo.png", initial_x, -80, 80, 50, choice([1, 1.5, 2, 2.5]))
    aliens.add(alien)
    initial_x += (screen_width - 80 * 6) / 5 + 80

space_rock = SpaceRock("asteroid.png", screen_width + 1500, 20, 65, 65, 3)

clock = time.Clock()
FPS = 60

mixer.init()

mixer.music.load("space.ogg")
mixer.music.play(-1)
shoot_sound = mixer.Sound("fire.ogg")
reset_sound = mixer.Sound("reset.wav")

font.init()

font_small = font.Font(None, 36)
score_display = font_small.render("Счёт: " + str(score), True, (255, 255, 255))
missed_display = font_small.render("Пропущено: " + str(missed_count), True, (255, 255, 255))
high_score_display = font_small.render("Рекорд: " + str(high_score), True, (255, 255, 255))
ability_display = font_small.render("Способность: нет", True, (255, 255, 255))
ability_time_display = font_small.render("До конца способности: " + str(ability_duration), True, (255, 255, 255))
reload_display = font_small.render("Пуль в магазине: " + str(60 - shot_count), True, (215, 255, 0))
health_text = font_small.render("Жизни: " + str(health), True, (255, 215, 0))

font_large = font.Font(None, 54)
game_over_display = font_large.render("ВЫ ПРОИГРАЛИ!", True, (200, 0, 0))
victory_display = font_large.render("ВЫ ПОБЕДИЛИ!", True, (255, 215, 0))
pause_display = font_large.render("ПРИОСТАНОВЛЕНО", True, (255, 255, 255))

font_tiny = font.Font(None, 18)
reload_message = font_tiny.render("Пожалуйста, подождите, идет перезарядка...", True, (200, 0, 0))

while is_game_active:
    keys = key.get_pressed()
    if keys[K_SPACE] and ability_type == 9 or keys[K_SPACE] and ability_type == 700:
        player_spaceship.shoot()
    for e in event.get():
        if e.type == QUIT:
            is_game_active = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not game_over and not is_paused:
                player_spaceship.shoot()
            if e.key == K_ESCAPE and not game_over and not is_paused:
                mixer.music.pause()
                window.blit(pause_display, (screen_width / 2 - pause_display.get_width() / 2, screen_height / 2 - pause_display.get_height() / 2))
                is_paused = True
                game_over = True
            elif e.key == K_ESCAPE and is_paused:
                game_over = False
                is_paused = False
                mixer.music.unpause()
            if e.key == K_r:
                if is_paused:
                    reset_sound.play()
                    game_over = False
                    is_game_active = True
                    is_ability_active = False
                    is_resetting = False
                    is_paused = False
                    ability_duration = 0
                    ability_type = 0
                    shot_count = 0
                    temp_var = 0
                    score = 0
                    missed_count = 0
                    initial_x = 0
                    alien_list = []
                    projectile_list = []
                    rock_list = []
                    health = 3
                    player_spaceship.rect.x = screen_width / 2 - 35
                    player_spaceship.rect.y = screen_height - 90
                    for proj in projectiles:
                        proj.kill()
                    for alien in aliens:
                        alien.kill()
                    for i in range(8):
                        alien = Alien("ufo.png", initial_x, -80, 80, 50, choice([1, 1.5, 2, 2.5]))
                        aliens.add(alien)
                        initial_x += (screen_width - 80 * 6) / 5 + 80
                    space_rock = SpaceRock("asteroid.png", screen_width + 1500, 20, 65, 65, 3)
                    window.blit(background, (0, 0))
                    player_spaceship.reset()
                    projectiles.draw(window)
                    aliens.draw(window)
                    score_display = font_small.render("Счёт: " + str(score), True, (255, 255, 255))
                    missed_display = font_small.render("Пропущенно: " + str(missed_count), True, (255, 215, 0))
                    high_score_display = font_small.render("Рекорд: " + str(high_score), True, (255, 255, 255))
                    ability_display = font_small.render("Способность: нет", True, (255, 255, 255))
                    reload_display = font_small.render("Пуль в магазине: " + str(60 - shot_count), True, (255, 215, 0))
                    health_text = font_small.render("Жизни: " + str(health), True, (255, 215, 0))
                    window.blit(score_display, (10, 10))
                    window.blit(missed_display, (10, 50))
                    window.blit(high_score_display, (10, 90))
                    window.blit(ability_display, (10, 130))
                    window.blit(reload_display, (10, 210))
                    window.blit(health_text, (screen_width - (health_text.get_width() + 10), 10))
                    window.blit(pause_display, (screen_width / 2 - pause_display.get_width() / 2, screen_height / 2 - pause_display.get_height() / 2))
                    is_paused = True
                else:
                    reset_sound.play()
                    mixer.music.unpause()
                    game_over = False
                    is_game_active = True
                    is_ability_active = False
                    is_resetting = False
                    is_paused = False
                    ability_duration = 0
                    ability_type = 0
                    shot_count = 0
                    temp_var = 0
                    score = 0
                    missed_count = 0
                    initial_x = 0
                    alien_list = []
                    projectile_list = []
                    rock_list = []
                    health = 3
                    player_spaceship.rect.x = screen_width / 2 - 35
                    player_spaceship.rect.y = screen_height - 90
                    for proj in projectiles:
                        proj.kill()
                    for alien in aliens:
                        alien.kill()
                    for i in range(8):
                        alien = Alien("ufo.png", initial_x, -80, 80, 50, choice([1, 1.5, 2, 2.5]))
                        aliens.add(alien)
                        initial_x += (screen_width - 80 * 6) / 5 + 80
                    space_rock = SpaceRock("asteroid.png", screen_width + 1500, 20, 65, 65, 3)
            if e.key == K_p and not game_over and not is_paused and 120 - shot_count != 120 and ability_type != 7:
                shot_count = 0
                temp_var = 90
                is_ability_active = True

    if not game_over and not is_paused:
        window.blit(background, (0, 0))
        player_spaceship.update()
        player_spaceship.reset()
        projectiles.update()
        projectiles.draw(window)
        aliens.update()
        aliens.draw(window)

        if ability_type == 5 or ability_type == 700:
            alien_list = sprite.groupcollide(aliens, projectiles, False, False)
        else:
            alien_list = sprite.groupcollide(aliens, projectiles, False, True)

        for alien in alien_list:
            alien.rect.y = -80
            alien.speed = choice([1, 1.5, 2, 2.5])
            alien.rect.x = randint(0, screen_width - 80)
            score += 1
            if ability_type == 1 or ability_type == 700:
                score += 2

        score_display = font_small.render("Счёт: " + str(score), True, (255, 255, 255))
        window.blit(score_display, (10, 10))
        if missed_count == 0:
            missed_display = font_small.render("Пропущенно: " + str(missed_count), True, (255, 215, 0))
        elif missed_count > 0 and missed_count <= 4:
            missed_display = font_small.render("Пропущенно: " + str(missed_count), True, (255, 255, 255))
        else:
            missed_display = font_small.render("Пропущенно: " + str(missed_count), True, (200, 0, 0))
        window.blit(missed_display, (10, 50))

        if high_score <= score and score != 0:
            high_score = score
            high_score_display = font_small.render("Новый рекорд: " + str(high_score), True, (255, 215, 0))
            if not is_resetting and not is_ability_active:
                if health == 1:
                    ability_type = 10
                    health = 3
                else:
                    ability_type = randint(1, 700)
                    if ability_type != 700:
                        ability_type = randint(1, 9)
                        ability_duration = 1200
                    else:
                        ability_duration = 1200
                is_resetting = True
        else:
            high_score_display = font_small.render("Рекорд: " + str(high_score), True, (255, 255, 255))

        window.blit(high_score_display, (10, 90))

        space_rock.update()
        space_rock.reset()
        rock_list = sprite.spritecollide(space_rock, aliens, False)
        alien.speed = choice([1, 1.5, 2, 2.5])
        alien.rect.x = randint(0, screen_width - 80)
        alien.rect.y = -80

        projectile_list = sprite.spritecollide(space_rock, projectiles, True)
        if projectile_list:
            space_rock.rect.x = -80
            if health == 1:
                ability_type = 10
                health = 3
            elif not is_ability_active:
                ability_type = randint(1, 700)
                if ability_type != 700:
                    ability_type = randint(1, 9)
                    ability_duration = 1200
                else:
                    ability_duration = 1200

        if ability_duration != 0:
            space_rock.rect.x = -80

        if ability_type == 4:
            player_spaceship.speed = 17
        else:
            player_spaceship.speed = 10

        if ability_type == 1:
            ability_display = font_small.render("Способность: тройные очки", True, (255, 215, 0))
        elif ability_type == 2:
            ability_display = font_small.render("Способность: неуязвимость", True, (255, 215, 0))
        elif ability_type == 3:
            ability_display = font_small.render("Способность: медленные пули", True, (255, 215, 0))
        elif ability_type == 4:
            ability_display = font_small.render("Способность: ускорение ракеты", True, (255, 215, 0))
        elif ability_type == 5:
            ability_display = font_small.render("Способность: пробивные пули", True, (255, 215, 0))
        elif ability_type == 6:
            ability_display = font_small.render("Способность: ракеты вместо пуль", True, (255, 215, 0))
        elif ability_type == 7:
            ability_display = font_small.render("Способность: бесконечные пули", True, (255, 215, 0))
        elif ability_type == 8:
            ability_display = font_small.render("Способность: тройной выстрел", True, (255, 215, 0))
        elif ability_type == 9:
            ability_display = font_small.render("Способность: пулемёт", True, (255, 215, 0))
        elif ability_type == 700:
            ability_display = font_small.render("Способность: все способности", True, (200, 0, 0))
        else:
            ability_display = font_small.render("Способность: нет", True, (255, 255, 255))

        window.blit(ability_display, (10, 130))

        if ability_duration != 0:
            ability_time_display = font_small.render("До конца способности: " + str(round(ability_duration / 60, 1)) + " сек", True, (255, 215, 0))
            window.blit(ability_time_display, (10, 170))

        if ability_type == 7 or ability_type == 700:
            reload_display = font_small.render("Пуль в магазине: бесконечность", True, (255, 215, 0))
        elif not is_ability_active:
            if 120 - shot_count >= 90:
                reload_display = font_small.render("Пуль в магазине: " + str(120 - shot_count), True, (255, 215, 0))
            elif 120 - shot_count > 30 and 120 - shot_count < 90:
                reload_display = font_small.render("Пуль в магазине: " + str(120 - shot_count), True, (255, 255, 255))
            elif 120 - shot_count <= 30:
                reload_display = font_small.render("Пуль в магазине: " + str(120 - shot_count), True, (200, 0, 0))

        window.blit(reload_display, (10, 210))
 
        collision_list = sprite.spritecollide(player_spaceship, aliens, False)
        if missed_count >= 7 or collision_list:
            if ability_type != 2 and ability_type != 700:
                health -= 1
                if health == 0 or missed_count >= 7:
                    health_text = font_small.render("Жизни: " + str(health), True, (200, 0, 0))
                    window.blit(health_text, (screen_width - (health_text.get_width() + 10), 10))
                    window.blit(game_over_display, (screen_width / 2 - game_over_display.get_width() / 2, screen_height / 2 - game_over_display.get_height() / 2))
                    mixer.music.pause()
                    game_over = True
                else:
                    for alien in collision_list:
                        alien.rect.y = -80
                        alien.speed = choice([1, 1.5, 2, 2.5])
                        alien.rect.x = randint(0, screen_width - 80)
            else:
                for alien in collision_list:
                    alien.rect.y = -80
                    alien.speed = choice([1, 1.5, 2, 2.5])
                    alien.rect.x = randint(0, screen_width - 80)
        if score >= 500:
            window.blit(victory_display, (screen_width / 2 - victory_display.get_width() / 2, screen_height / 2 - victory_display.get_height() / 2))
            mixer.music.pause()
            game_over = True
        if health == 3:
            health_text = font_small.render("Жизни: " + str(health), True, (255, 215, 0))
        elif health < 3 and health > 1:
            health_text = font_small.render("Жизни: " + str(health), True, (255, 255, 255))
        else:
            health_text = font_small.render("Жизни: " + str(health), True, (200, 0, 0))
        window.blit(health_text, (screen_width - (health_text.get_width() + 10), 10))

        if ability_duration != 0:
            ability_duration -= 1
        else:
            ability_type = 0

        if temp_var < 0:
            is_ability_active = False
        else:
            temp_var -= 1

        if is_ability_active:
            window.blit(reload_message, (screen_width / 2 - reload_message.get_width() / 2, screen_height / 10 * 9 - reload_message.get_height() / 2))

    display.update()
    clock.tick(FPS)

# Завершение игры
quit()
