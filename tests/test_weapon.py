import unittest
import utilities
from weapon import *
from game import *


class WeaponSimplifiedTestCase(unittest.TestCase):
    def setUp(self):
        self.fire_rate = 3  # bullets per second
        self.world = World()
        self.owner_location = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.owner = GameEntity(self.world, 'dummy', None, self.owner_location)
        self.ammo = 9999
        self.damage = 10
        self.weapon = WeaponSimplified(self.world, self.owner, self.fire_rate, self.damage, self.ammo)

    def test_ammunition_decrease_1tick(self):
        self.weapon.process(TICK_SECOND)
        self.weapon.fire()
        self.assertEqual(self.weapon.ammo, self.ammo - 1)

    # def test_ammunition_decrease_2sec(self):
    #     seconds = 2
    #     self.weapon.process(seconds)
    #     self.assertEqual(self.weapon.ammo, self.ammo - self.fire_rate * seconds)
    def test_after_2seconds_ready_to_fire(self):
        self.weapon.fire()
        self.assertFalse(self.weapon.ready_to_fire)
        self.weapon.process(2)
        self.weapon.ready_to_fire = True
        pass

    def test_bullets_spawned_on_fire(self):
        self.weapon.process(1)
        self.weapon.fire()
        self.assertGreater(self.world.entity_count(), 0)

    def test_bullets_damage(self):
        self.weapon.process(1)
        bullets = (e for e in self.world.entities.values() if e.name == 'bullet')
        for b in bullets:
            with self.subTest(bullet=b):
                self.assertEqual(b.damage, self.weapon.damage)

    def test_no_ammo(self):
        self.weapon.ammo = 0
        self.weapon.process(TICK_SECOND)
        self.weapon.fire()
        self.assertEqual(self.weapon.ammo, 0)
        self.assertEqual(self.weapon.accumulator, 0)    # accumulator = 0, since there is no more ammo
