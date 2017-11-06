from weapon import Weapon, Projectile, Warhead
from unittest import TestCase
from game import *


class DestinationProjectileTestCase(TestCase):

    def setUp(self):
        self.warhead = None
        self.speed = 100
        self.world = World()
        self.location = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.destination = Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.projectile = Projectile(self.world, None, self.location, self.destination, self.speed, self.warhead)
        self.world.add_entity(self.projectile)

    def test_instance(self):
        pass


class AngledProjectileTestCase(TestCase):

    def setUp(self):
        self.warhead = None
        self.speed = 100
        self.world = World()
        self.location = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.angle = math.radians(300)
        self.projectile = Projectile(self.world, None, self.location, self.destination, self.speed, self.warhead)
        self.world.add_entity(self.projectile)

    def test_instance(self):
        pass