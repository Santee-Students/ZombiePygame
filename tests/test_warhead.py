from weapon import Weapon, Projectile, Warhead
import unittest
from game import *


class WarheadTestCase(unittest.TestCase):

    """Warheads should be reusable for different projectiles of same type"""

    def setUp(self):
        """
        self.warhead = None
        self.speed = 100
        self.world = World()
        self.location = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.projectile = Projectile(self.world, None, self.location, self.destination, self.speed, self.warhead)
        self.world.add_entity(self.projectile)
        """

    def test_instance(self):
        pass


class WarheadTestCase(unittest.TestCase):

    def setUp(self):
        self.damage = 0
        self.vs_armor = 0.5
        self.vs_flesh = 1
        self.weapon = None  # If there is one, the weapon will fire too
        self.radius = 0
        self.attached_effect =  None