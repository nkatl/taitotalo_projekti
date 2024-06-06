# arcade side-scrolling shooter

import pygame
import random

# pygame setup
pygame.init()

width, height = 1024, 881
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
dt = 0

icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Cosmofight')

# making an object in the middle of the screen
# object_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

x, y = 50, 300
speed = 7
player = pygame.image.load('images/ship.png').convert_alpha()
player_health = pygame.image.load('images/health.png').convert_alpha()
player_life = 3
player_health_list = []
collision = pygame.mixer.Sound('sounds/explosion.mp3')

enemy = pygame.image.load('images/enemy.png').convert_alpha()
enemy_list = []
enemy_health_list = []
hit_enemy = pygame.mixer.Sound('sounds/kick.mp3')
enemy_timer = pygame.USEREVENT + 1
# pygame.time.set_timer(enemy_timer, 2000)

enemy_bullet = pygame.image.load('images/flake.png').convert_alpha()
enemy_bullet_list = []
enemy_bullet_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(enemy_bullet_timer, 1650)

meteor = pygame.image.load('images/meteor.png').convert_alpha()
meteor_list = []
meteor_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(meteor_timer, 1500)
meteor_angles = []  # list to store rotation angles for each enemy

bg = pygame.image.load('images/bg.png').convert()
bg_x = 0

lazer = pygame.image.load('images/lazer.png').convert_alpha()
lazers = []
lazer_sound = pygame.mixer.Sound('sounds/laser gun.mp3')

label = pygame.font.Font('fonts/Orbitron-VariableFont_wght.ttf', 50)

# start menu
game_start = label.render('Start the Game', True, (98, 221, 89))
game_start_rect = game_start.get_rect(topleft=(300, 250))
exit_game = label.render('Exit', True, (98, 221, 89))
exit_game_rect = exit_game.get_rect(topleft=(445, 420))
prompt = pygame.font.Font(None, 50)
move = prompt.render('WASD - move', True, (109, 108, 108))
shoot = prompt.render('SPACE - shoot', True, (109, 108, 108))
description = prompt.render('- after three hits, the game will be over', True, (109, 108, 108))
description_2 = prompt.render('on collision with -', True, (109, 108, 108))
description_3 = prompt.render('gameover', True, (109, 108, 108))


# text on screen in case of lose
game_over = label.render('Game Over', False, (220, 41, 13))
play_again = label.render('Play Again', True, (98, 221, 89))
play_again_rect = play_again.get_rect(topleft=(360, 430))
menu = label.render('Main Menu', True, (98, 221, 89))
menu_rect = menu.get_rect(topleft=(360, 560))
# your_score = label.render(f'Your score: {score}', False, ())

score = 0
points = pygame.font.Font('fonts/Orbitron-VariableFont_wght.ttf', 25)


def render_score(score):
    return points.render(f"Score: {score}", True, (175, 175, 175))


def show_score(score):
    return label.render(f'Your score: {score}', False, (109, 108, 108))


main_menu = True
gameplay = False
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close window
    screen.fill((68, 60, 109))
    screen.blit(move, (100, 500))
    screen.blit(shoot, (700, 500))
    screen.blit(description, (200, 650))
    screen.blit(enemy_bullet, (180, 660))
    # screen.blit(description_2, (200, 710))
    # screen.blit(enemy, ())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if gameplay:
            if event.type == enemy_timer:
                # genering random Y coordinate
                enemy_y = random.randint(0, height - enemy.get_height())
                enemy_list.append(enemy.get_rect(topleft=(1026, enemy_y)))
                enemy_health_list.append(2)  # giving new enemy 2 health with spawn

            if event.type == enemy_bullet_timer:
                if enemy_list:  # if no enemies, no shooting
                    shooting_enemy = random.choice(enemy_list)  # choosing a random enemy who's gonna shoot
                    enemy_bullet_list.append(enemy_bullet.get_rect(topleft=
                                                                   (shooting_enemy.x,
                                                                    shooting_enemy.y + enemy.get_height() //
                                                                    2)))  # making enemy bullet as an object and
                    # placing it on enemy position
                    player_health_list.append(3)

            if event.type == meteor_timer:
                meteor_y = random.randint(0, height - meteor.get_height())
                new_meteor = meteor.get_rect(topleft=(1025, meteor_y))
                meteor_list.append(new_meteor)
                meteor_angles.append(0)  # Initialize rotation angle for new meteor
        # creating a lazer shot
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            lazer_sound.play()
            lazers.append(lazer.get_rect(topleft=(x + 40, y + 30)))

    if main_menu:
        screen.blit(game_start, game_start_rect)
        screen.blit(exit_game, exit_game_rect)

        mouse = pygame.mouse.get_pos()
        if game_start_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            main_menu = False
            gameplay = True
            # timers for enemy spawning, bullets and meteorites are set when game starts
            pygame.time.set_timer(enemy_timer, 2000)
            pygame.time.set_timer(enemy_bullet_timer, 1650)
            pygame.time.set_timer(meteor_timer, 1500)

        elif exit_game_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            running = False
    # fill the screen with color
    # screen.fill('green')
    # display the player and the background pictures
    # screen.blit(bg, (bg_x, 0))
    # screen.blit(bg, (bg_x + 1024, 0))
    # screen.blit(player, (x, y))
    # screen.blit(render_score(score), (0, 850))
    # screen.blit(enemy, (enemy_x, 250))    # drawing just one enemy at the time

    elif gameplay:
        life_label = prompt.render(str(player_life), False, (109, 108, 108))

        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 1024, 0))
        screen.blit(player, (x, y))
        screen.blit(render_score(score), (0, 850))
        screen.blit(life_label, (30, 0))
        screen.blit(player_health, (0, 0))

        # drawing around player and enemy a rectangle
        player_rect = player.get_rect(topleft=(x, y))
        # enemy_rect = enemy.get_rect(topleft=(enemy_x, 250))
        if enemy_list:
            for (i, el) in enumerate(enemy_list):
                screen.blit(enemy, el)
                el.x -= 5

                if el.x < -10:
                    enemy_list.pop(i)
                    enemy_health_list.pop(i)

                # condition, when player interacts with enemy
                if player_rect.colliderect(el):
                    collision.play()
                    gameplay = False

        if meteor_list:
            for (i, el) in enumerate(meteor_list):
                # rotate the meteor
                meteor_angles[i] += 2  # adjust this value to control rotation speed
                rotated_meteor = pygame.transform.rotate(meteor, meteor_angles[i])  # rotating meteor image by an
                                                                                    # angle of meteor_angles[i]
                rotated_meteor_rect = rotated_meteor.get_rect(
                    center=el.center)  # creates a rectangle around meteor and places it in the center of meteor
                screen.blit(rotated_meteor, rotated_meteor_rect.topleft)  # topleft angle of rotated meteor rectangle

                el.x -= 10

                if el.x < -10:
                    meteor_list.pop(i)
                    meteor_angles.pop(i)  # Remove angle from list

                if player_rect.colliderect(rotated_meteor_rect):
                    collision.play()
                    gameplay = False

        # moving background
        bg_x -= 2
        if bg_x == -1024:
            bg_x = 0

        # render game here
        # pygame.draw.circle(screen, 'purple', object_pos, 40)    # drawing a circle

        keys = pygame.key.get_pressed()  # key binding
        if keys[pygame.K_w]:
            y -= speed
        if keys[pygame.K_s]:
            y += speed
        if keys[pygame.K_a]:
            x -= speed
        if keys[pygame.K_d]:
            x += speed

        # player can't go off-screen
        x = max(0, min(x, width - player.get_width()))
        y = max(0, min(y, height - player.get_height()))

        # enemy speed
        # enemy_x -= 5

        # lazer launch
        if lazers:
            for (i, el) in enumerate(lazers):
                screen.blit(lazer, (el.x, el.y))
                el.x += 10

                # deleting lazer if it goes of the screen
                if el.x > 1030:
                    lazers.pop(i)

                # if lazer interacts with enemy, deleting them from the game(lists)
                if enemy_list:
                    for (j, enemy_el) in enumerate(enemy_list):
                        if el.colliderect(enemy_el):
                            hit_enemy.play()
                            enemy_health_list[j] -= 1  # enemy have 2 health
                            lazers.pop(i)
                            if enemy_health_list[j] <= 0:
                                hit_enemy.play()
                                enemy_list.pop(j)
                                enemy_health_list.pop(j)
                                score += 300
                                score_label = render_score(score)
                            break

                if meteor_list:
                    for (m, meteor_el) in enumerate(meteor_list):
                        if el.colliderect(meteor_el):
                            meteor_list.pop(m)
                            lazers.pop(i)
                            score += 200
                            break

        # enemy bullet launch
        if enemy_bullet_list:
            for (f, el) in enumerate(enemy_bullet_list):
                screen.blit(enemy_bullet, (el.x, el.y))
                el.x -= 10  # bullet speed

                if el.x < -10:  # deleting bullet if it goes off the screen
                    enemy_bullet_list.pop(f)

                if player_rect.colliderect(el):  # if bullet interacts with player, -health
                    enemy_bullet_list.pop(f)
                    player_health_list[f] -= 1
                    player_life -= 1
                    if player_health_list[f] <= 0:
                        collision.play()
                        gameplay = False

    else:
        # gameover screen
        screen.fill((68, 60, 109))
        screen.blit(game_over, (360, 50))
        screen.blit(show_score(score), (300, 240))
        screen.blit(play_again, (play_again_rect))
        screen.blit(menu, (menu_rect))

        # binding mouse key to restart the game in case of loss
        mouse = pygame.mouse.get_pos()
        if play_again_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            x, y = 50, 300
            player = pygame.image.load('images/ship.png').convert_alpha()
            # next lines deleting all objects from game, to start a new one
            enemy_list.clear()
            lazers.clear()
            meteor_list.clear()
            enemy_bullet_list.clear()
            score = 0
            player_health_list.clear()
            pygame.time.set_timer(enemy_timer, 2000)
            pygame.time.set_timer(enemy_bullet_timer, 1650)
            pygame.time.set_timer(meteor_timer, 1500)
            player_life = 3

        elif menu_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            main_menu = True
            gameplay = False
            x, y = 50, 300
            player = pygame.image.load('images/ship.png').convert_alpha()
            enemy_list.clear()
            lazers.clear()
            meteor_list.clear()
            enemy_bullet_list.clear()
            score = 0
            player_health_list.clear()
            player_life = 3

    # flip() the display to put work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame,
    # used for framerate independent physics.
    dt = clock.tick(60)

pygame.quit()
