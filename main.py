# arcade side-scrolling shooter

import pygame
import random

# pygame setup
pygame.init()

# set the game screen size
width, height = 1024, 881
screen = pygame.display.set_mode((width, height))
# call the .time method to create the Clock() object, which helps to keep track of the time in the game
clock = pygame.time.Clock()
# 'delta time' - amount of time passed between the current and previous frame
dt = 0

# displaying the icon and game name in the upper left corner of the window
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Cosmofight')

# coordinates of the player's appearance on the screen
x, y = 50, 300
# player speed
speed = 7
# uploading an image of the player
player = pygame.image.load('images/ship.png').convert_alpha()
# uploading an image of the player to display health
player_health = pygame.image.load('images/health.png').convert_alpha()
player_life = 3
player_health_list = []
# uploading sound of explosion
collision = pygame.mixer.Sound('sounds/explosion.mp3')

# uploading an image of the enemy
enemy = pygame.image.load('images/enemy.png').convert_alpha()
# setting enemy list
enemy_list = []
# setting enemy health
enemy_health_list = []
# uploading hitting sound
hit_enemy = pygame.mixer.Sound('sounds/kick.mp3')
# user event creation to make enemies
enemy_timer = pygame.USEREVENT + 1

# uploading an image of the enemy bullet
enemy_bullet = pygame.image.load('images/flake.png').convert_alpha()
# setting enemy bullet list
enemy_bullet_list = []
# user event creation to make enemies shoot
enemy_bullet_timer = pygame.USEREVENT + 3

# uploading an image of the meteor
meteor = pygame.image.load('images/meteor.png').convert_alpha()
# setting meteor list
meteor_list = []
# user event creation to make meteors
meteor_timer = pygame.USEREVENT + 2
# list to store rotation angles of meteor
meteor_angles = []

# uploading an image of the background picture
bg = pygame.image.load('images/bg.png').convert()
# x-coordinates of the original background location
bg_x = 0

# uploading an image of the lazer(for player)
lazer = pygame.image.load('images/lazer.png').convert_alpha()
# setting lazer list
lazers = []
# uploading lazer sound
lazer_sound = pygame.mixer.Sound('sounds/laser gun.mp3')

# uploading font for start menu and gameover screen
label = pygame.font.Font('fonts/Orbitron-VariableFont_wght.ttf', 50)

# start menu
# text creation
game_start = label.render('Start the Game', True, (98, 221, 89))
# places a text in a rectangle to allow interaction
game_start_rect = game_start.get_rect(topleft=(300, 250))
# text creation
exit_game = label.render('Exit', True, (98, 221, 89))
# places a text in a rectangle to allow interaction
exit_game_rect = exit_game.get_rect(topleft=(445, 420))

# uploading default font to describe the rules on start menu
prompt = pygame.font.Font(None, 50)
# text creation
move = prompt.render('WASD - move', True, (109, 108, 108))
shoot = prompt.render('SPACE - shoot', True, (109, 108, 108))
description = prompt.render('- after three hits, the game will be over', True, (109, 108, 108))
description_2 = prompt.render('on collision with -', True, (109, 108, 108))
description_3 = prompt.render('gameover', True, (109, 108, 108))

# text on screen in case of lose
# text creation
game_over = label.render('Game Over', False, (220, 41, 13))
play_again = label.render('Play Again', True, (98, 221, 89))
# places a text in a rectangle to allow interaction
play_again_rect = play_again.get_rect(topleft=(360, 430))
# text creation
menu = label.render('Main Menu', True, (98, 221, 89))
# places a text in a rectangle to allow interaction
menu_rect = menu.get_rect(topleft=(360, 560))

# variable for storing earned points
score = 0
# uploading font for points
points = pygame.font.Font('fonts/Orbitron-VariableFont_wght.ttf', 25)


def render_score(score):
    # сounts points and displays them on the screen during the game for meteors and enemy ships shot down
    return points.render(f"Score: {score}", True, (175, 175, 175))


def show_score(score):
    # showing all earned points on gameover screen
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

        mouse = pygame.mouse.get_pos()  # current position of the mouse
        if game_start_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            main_menu = False
            gameplay = True
            # timers for enemy spawning, bullets and meteorites are set when game starts
            pygame.time.set_timer(enemy_timer, 2000)
            pygame.time.set_timer(enemy_bullet_timer, 1650)
            pygame.time.set_timer(meteor_timer, 1500)

        elif exit_game_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            running = False

    elif gameplay:
        life_label = prompt.render(str(player_life), False, (109, 108, 108))    # number of lives

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

        keys = pygame.key.get_pressed()  # key binding
        if keys[pygame.K_w]:
            y -= speed
        if keys[pygame.K_s]:
            y += speed
        if keys[pygame.K_a]:
            x -= speed
        if keys[pygame.K_d]:
            x += speed

        # limiting player movement within the window
        x = max(0, min(x, width - player.get_width()))
        y = max(0, min(y, height - player.get_height()))

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

        elif menu_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:   # back to Main Menu
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

    # screen update(smooth and correct display of all changes on the screen)
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60)

pygame.quit()
