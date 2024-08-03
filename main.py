# arcade side-scrolling shooter

import pygame
import random

# initialization of all pygame modules
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
# font for arrows
arrow_font = pygame.font.SysFont('Calibri', 35)
# creating variables with keyboard arrows
up = '\u2191'
down = '\u2193'
left = '\u2190'
right = '\u2192'
# creating text surfaces for arrows
text_up = arrow_font.render(up, True, (160, 156, 156))
text_down = arrow_font.render(down, True, (160, 156, 156))
text_left = arrow_font.render(left, True, (160, 156, 156))
text_right = arrow_font.render(right, True, (160, 156, 156))
# text creation
move = prompt.render(' - move', True, (160, 156, 156))
shoot = prompt.render('SPACE - shoot', True, (160, 156, 156))
description = prompt.render('- after three hits, the game will be over', True, (160, 156, 156))

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
best_result = 0
highscore = points.render(f"Best result: {best_result}", True, (175, 175, 175))


def render_score(score):
    # сounts points and displays them on the screen during the game for meteors and enemy ships shot down
    return points.render(f"Score: {score}", True, (175, 175, 175))


def show_score(score):
    # showing all earned points on gameover screen
    return label.render(f'Your score: {score}', False, (109, 108, 108))


# flag indicating that the main menu is active
main_menu = True
# flag indicating that the gameplay is active
gameplay = False
# flag indicating that the game window is running
running = True

# main loop
while running:

    # moving background screen
    bg_x -= 2
    if bg_x == -1024:
        bg_x = 0

    # background design
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1024, 0))
    # displaying the control description in the main menu
    screen.blit(text_up, (65, 460))
    screen.blit(text_down, (65, 510))
    screen.blit(text_left, (30, 500))
    screen.blit(text_right, (100, 500))
    screen.blit(move, (130, 500))
    screen.blit(shoot, (700, 500))
    # displaying a description of enemy bullet hits
    screen.blit(description, (200, 650))
    screen.blit(enemy_bullet, (180, 660))

    # event processing
    for event in pygame.event.get():
        # pygame.QUIT means the user clicked X to close window
        if event.type == pygame.QUIT:
            running = False

        # gameplay flag active
        if gameplay:
            # enemy spawn event
            if event.type == enemy_timer:
                # generating random Y coordinate
                enemy_y = random.randint(0, height - enemy.get_height())
                # creating a rectangle around an enemy
                enemy_list.append(enemy.get_rect(topleft=(1026, enemy_y)))
                # giving new enemy 2 health with spawn
                enemy_health_list.append(2)

            # enemy bullet spawn event
            if event.type == enemy_bullet_timer:
                # if no enemies, no shooting
                if enemy_list:
                    # choosing a random enemy who's going to shoot
                    shooting_enemy = random.choice(enemy_list)
                    # making enemy bullet as an object and placing it on enemy position
                    enemy_bullet_list.append(enemy_bullet.get_rect(topleft=
                                                                   (shooting_enemy.x,
                                                                    shooting_enemy.y + enemy.get_height() //
                                                                    2)))
                    # creating three lives for the player
                    player_health_list.append(3)

            # meteor spawn event
            if event.type == meteor_timer:
                # generating random Y coordinate for spawn
                meteor_y = random.randint(0, height - meteor.get_height())
                # creating a rectangle around the meteor
                new_meteor = meteor.get_rect(topleft=(1025, meteor_y))
                meteor_list.append(new_meteor)
                meteor_angles.append(0)  # Initialize rotation angle for new meteor

        # creating a lazer shot event
        # if player press SPACE button laser will be fired
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            lazer_sound.play()  # when pressing SPACE button, laser sound play
            lazers.append(lazer.get_rect(topleft=(x + 40, y + 30)))  # rectangle around laser

    if main_menu:
        # displaying interactive buttons for starting and exit the game in the main menu
        screen.blit(game_start, game_start_rect)
        screen.blit(exit_game, exit_game_rect)

        mouse = pygame.mouse.get_pos()  # current position of the mouse

        # if player press with mouse on Start the Game button
        if game_start_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            main_menu = False
            gameplay = True
            # timers for enemy spawning, bullets and meteorites are set when game starts
            pygame.time.set_timer(enemy_timer, 2000)
            pygame.time.set_timer(enemy_bullet_timer, 1650)
            pygame.time.set_timer(meteor_timer, 1500)

        # if player press with mouse on Exit button
        elif exit_game_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            running = False

    elif gameplay:
        # definition of font and its color for player lives
        life_label = prompt.render(str(player_life), False, (109, 108, 108))

        # displaying background
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 1024, 0))
        # displaying player
        screen.blit(player, (x, y))
        # displaying players current score
        screen.blit(render_score(score), (0, 850))
        # displaying players lives
        screen.blit(life_label, (30, 0))
        screen.blit(player_health, (0, 0))

        # drawing around player rectangle
        player_rect = player.get_rect(topleft=(x, y))

        # if enemy spawned
        if enemy_list:
            for (i, el) in enumerate(enemy_list):
                # displaying enemy
                screen.blit(enemy, el)
                # enemy speed
                el.x -= 7

                # condition when enemy flies off the screen
                if el.x < -10:
                    # deleting enemy from the playing screen
                    enemy_list.pop(i)
                    enemy_health_list.pop(i)

                # condition, when player interacts with enemy
                if player_rect.colliderect(el):
                    # collision sound play
                    collision.play()
                    # game ends
                    gameplay = False

        # if meteor spawned
        if meteor_list:
            for (i, el) in enumerate(meteor_list):
                # value to control rotation speed
                meteor_angles[i] += 2
                # rotating meteor image by an angle of meteor_angles[i]
                rotated_meteor = pygame.transform.rotate(meteor, meteor_angles[i])
                # creates a rectangle around meteor
                rotated_meteor_rect = rotated_meteor.get_rect(center=el.center)
                # displaying rotation of the meteor
                screen.blit(rotated_meteor, rotated_meteor_rect.topleft)

                el.x -= 10  # meteor speed

                # condition when meteor flies off the screen
                if el.x < -10:
                    # deleting meteor from the playing screen
                    meteor_list.pop(i)
                    meteor_angles.pop(i)

                # when player collides with meteor
                if player_rect.colliderect(rotated_meteor_rect):
                    # collision sound play
                    collision.play()
                    # game ends
                    gameplay = False

        # moving background
        bg_x -= 2
        if bg_x == -1024:
            bg_x = 0

        # key binding
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y -= speed
        if keys[pygame.K_DOWN]:
            y += speed
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed

        # limiting player movement within the window
        x = max(0, min(x, width - player.get_width()))
        y = max(0, min(y, height - player.get_height()))

        # lazer launch
        if lazers:
            for (i, el) in enumerate(lazers):
                # displaying laser
                screen.blit(lazer, (el.x, el.y))
                el.x += 10  # laser speed

                # deleting lazer if it goes of the screen
                if el.x > 1030:
                    lazers.pop(i)

                # condition of interaction lasers with enemies
                if enemy_list:
                    for (j, enemy_el) in enumerate(enemy_list):
                        # if laser collides with enemy
                        if el.colliderect(enemy_el):
                            hit_enemy.play()   # hit sound play
                            enemy_health_list[j] -= 1  # enemy have 2 health
                            lazers.pop(i)   # deleting laser from the game
                            # if laser hits enemy 2 times
                            if enemy_health_list[j] <= 0:
                                hit_enemy.play()    # hit sound play
                                enemy_list.pop(j)   # deleting enemy
                                enemy_health_list.pop(j)
                                score += 300    # adding points
                                # score_label = render_score(score)   # and displaying them on the screen
                            break

                # condition of interaction lasers with meteors
                if meteor_list:
                    for (m, meteor_el) in enumerate(meteor_list):
                        # if laser collides with meteor
                        if el.colliderect(meteor_el):
                            meteor_list.pop(m)  # deleting meteor from the game
                            lazers.pop(i)   # deleting laser from the game
                            score += 200    # adding points
                            break

        # enemy bullet launch
        if enemy_bullet_list:
            for (f, el) in enumerate(enemy_bullet_list):
                # displaying enemy bullet
                screen.blit(enemy_bullet, (el.x, el.y))
                el.x -= 12  # bullet speed

                if el.x < -10:  # deleting bullet if it goes off the screen
                    enemy_bullet_list.pop(f)

                if player_rect.colliderect(el):  # if bullet interacts with player, -health
                    enemy_bullet_list.pop(f)    # deleting bullet from the game
                    player_health_list[f] -= 1  # subtraction of 1 life from list
                    player_life -= 1    # subtraction of 1 life from screen

                    if player_health_list[f] <= 0:  # if player lives has gone
                        collision.play()    # collision sound play
                        gameplay = False    # game ends

    else:
        # game over screen
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 1024, 0))
        screen.blit(game_over, (360, 50))
        # total score for played game
        screen.blit(show_score(score), (300, 240))
        # interaction buttons to play again and to go back to main menu
        screen.blit(play_again, (play_again_rect))
        screen.blit(menu, (menu_rect))

        # binding mouse key to restart the game
        mouse = pygame.mouse.get_pos()
        # when pressing the button (with LMB) new game starts
        if play_again_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            # deleting objects from the last game and resetting the player's location and scores to default
            x, y = 50, 300
            player = pygame.image.load('images/ship.png').convert_alpha()
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

        # when pressing the button (with LMB) going back to main menu
        elif menu_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            main_menu = True
            gameplay = False
            # deleting objects from the last game and resetting the player's location and scores to default
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
    dt = clock.tick(60) / 1000

# shutting down pygame
pygame.quit()
