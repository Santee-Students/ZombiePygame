from mobs import *
from random import randint, random
import unittest
from game import *
import pygame

NUM_ZOMBIES = 10
NUM_SURVIVORS = 5
NUM_SENTRY_GUNS = 2

class WorldTestCase(unittest.TestCase):

    def setUp(self):
        self.world = World()
        dummy_surface = pygame.Surface((16, 16))
        w, h = dummy_surface.get_size()

        # Add zombies
        for i in range(NUM_ZOMBIES):
            x = random() * SCREEN_WIDTH
            y = random() * SCREEN_HEIGHT
            zombie = Zombie(self.world, dummy_surface, Vector2(x, y))
            self.world.add_entity(zombie)

        # Add survivors
        for i in range(NUM_SURVIVORS):
            x = random() * SCREEN_WIDTH
            y = random() * SCREEN_HEIGHT
            survivor = Survivor(self.world, dummy_surface, Vector2(x, y))
            self.world.add_entity(survivor)

        # Add sentry guns
        for i in range(NUM_SENTRY_GUNS):
            x = random() * SCREEN_WIDTH
            y = random() * SCREEN_HEIGHT
            self.sentry_gun = SentryGun(self.world, dummy_surface, Vector2(x, y))
            self.world.add_entity(self.sentry_gun)

    def test_list_all_entities_with_name(self):
        zombies = tuple(self.world.entities_with_name('zombie'))
        survivors = tuple(self.world.entities_with_name('survivor'))
        sentry_guns = tuple(self.world.entities_with_name('sentry_gun'))
        self.assertEqual(len(zombies), NUM_ZOMBIES)
        self.assertEqual(len(survivors), NUM_SURVIVORS)
        self.assertEqual(len(sentry_guns), NUM_SENTRY_GUNS)

    def test_get_close_entity_type_zombie(self):
        z = self.world.get_close_entity('zombie', SCREEN_CENTER)
        self.assertEqual(z.name, 'zombie')