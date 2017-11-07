from weapon import Weapon, Projectile, Warhead
from unittest import TestCase
from game import *
import utilities


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
        self.speed = 100
        self.world = World()
        self.location = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.angle = utilities.unit_angle(math.radians(300))
        self.direction = Vector2(1, 0).rotate(self.angle)
        self.max_distance = 200
        self.projectile = Projectile(self.world, 'bullet', None, self.location, self.direction, speed=self.speed, damage=0, max_distance=self.max_distance)
        self.world.add_entity(self.projectile)

    def test_instance(self):
        pass

    def test_max_distance_remove_from_world(self):
        seconds = self.max_distance / self.speed
        self.projectile.process(seconds)
        self.assertNotIn(self.projectile, self.world.entities.values())
