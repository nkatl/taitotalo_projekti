import unittest     # module for writing and executing tests
import pygame
import random

# importing variables and objects from the main game file
from main import width, height, player, enemy, meteor, lazer, player_health_list, enemy_list, lazers


# creating a class for tests inheriting from unittest.TestCase
class GameTest(unittest.TestCase):

    # the setUp method is executed before each test to initialize common objects
    def setUp(self):
        pygame.init()   # pygame initialization
        self.screen = pygame.display.set_mode((width, height))  # creating a screen for tests
        self.clock = pygame.time.Clock()    # creating a Clock object for time management
        # next lines, creating rectangles for player, enemy, meteor and laser
        self.player_rect = pygame.Rect(50, 300, player.get_width(), player.get_height())
        self.enemy_rect = pygame.Rect(1024, random.randint(0, height - enemy.get_height()), enemy.get_width(), enemy.get_height())
        self.meteor_rect = pygame.Rect(1024, random.randint(0, height - meteor.get_height()), meteor.get_width(), meteor.get_height())
        self.lazer_rect = pygame.Rect(100, 100, lazer.get_width(), lazer.get_height())

    # the tearDown method is executed after each test to terminate pygame
    def tearDown(self):
        pygame.quit()   # shutting down pygame

    # testing player movement
    def test_player_movement(self):
        x, y = 50, 300  # initial coordinates of the player
        speed = 7   # speed of the player's movement
        # dictionary that simulates keystrokes
        keys = {pygame.K_UP: True, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}

        # logic of coordinates change depending on pressed keys
        if keys[pygame.K_UP]:
            y -= speed
        if keys[pygame.K_DOWN]:
            y += speed
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed

        # check that the y coordinate has changed correctly
        self.assertEqual(y, 293)

    # testing laser movement
    def test_lazer_movement(self):
        self.lazer_rect.x += 10     # changing the x-coordinate of the laser(speed)
        self.assertTrue(self.lazer_rect.x > 100)    # check that the x coordinate is greater than 100

    # testing player-enemy collision
    def test_enemy_collision(self):
        self.enemy_rect.topleft = (60, 300)     # changing the coordinates of the enemy to collide with the player
        self.assertTrue(self.player_rect.colliderect(self.enemy_rect))      # Checking that the rectangles intersect

    # testing game logic
    def test_gameplay_logic(self):
        self.assertEqual(len(player_health_list), 0)    # checking that the player's health list is empty
        self.assertEqual(len(enemy_list), 0)    # checking that the enemy list is empty
        self.assertEqual(len(lazers), 0)    # checking that the laser list is empty


# running tests
if __name__ == '__main__':
    unittest.main()    # run all tests in the class