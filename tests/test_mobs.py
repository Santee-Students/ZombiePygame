import unittest

from manager import ImageManager
import time
from mobs import *
from game import *
from pygame.math import Vector2

class SentryGunTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.image_manager = ImageManager('../data/images/')
        self.sentry_gun_image = self.image_manager['sentrygun.png']
        self.world = World()
        self.TICK_SECOND = 33 / 1000

        # Create the sentry gun
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2
        self.sentry_gun = SentryGun(self.world, self.sentry_gun_image, (x, y))
        self.world.add_entity(self.sentry_gun)

        # Add a couple of zombies
        '''
        for i in range(10):
            zombie_image = self.image_manager['zombie.png']
            zombie = Zombie(self.world, zombie_image, (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))
            self.world.add_entity(zombie)
        '''

        # Main zombie
        self.zombie = Zombie(self.world, self.image_manager['zombie.png'], (100, 100))
        self.world.add_entity(self.zombie)

        self.world.render(self.screen)
        pygame.display.update()

    def test_turret_face_target(self):
        self.sentry_gun.turret_face_entity(self.zombie)
        self.sentry_gun.brain.think()
        self.assertEqual(self.sentry_gun.target, self.zombie)

    def test_target_acquire(self):
        # Make the turret face the zombie
        angle = SentientEntity.get_angle(self.sentry_gun.location, self.zombie.location)
        self.sentry_gun.turret_angle = angle
        self.sentry_gun.brain.think()   # Switch states from scan to face
        print(self.sentry_gun.brain.active_state.name)
        self.assertEqual(self.sentry_gun.target, self.zombie)

    @unittest.skip
    def test_rotate_to_target(self):
        self.sentry_gun.target = self.zombie
        self.sentry_gun.brain.set_state('face')
        # Do a loop that will repeatedly call think

        '''
        prev_angle = self.sentry_gun.turret_angle
        for i in range(100):
            self.screen.fill((0, 0, 0))
            #with self.subTest(i=i):
            self.sentry_gun.process(self.TICK_SECOND)
            #self.assertNotEqual(self.sentry_gun.turret_angle, prev_angle)
            print('angle:',self.sentry_gun.turret_angle)

            #angle_diff = self.sentry_gun.turret_angle - prev_angle
            #self.assertAlmostEqual(angle_diff, self.sentry_gun.turret_rotation_rate * self.TICK_SECOND, 4)

            prev_angle = self.sentry_gun.turret_angle
            self.world.render(self.screen)
            pygame.display.update()
        '''

    def test_turret_angle(self):
        self.assertAlmostEqual(self.sentry_gun.turret_angle,utilities.unit_angle(self.sentry_gun.turret_angle))
        new_angle = 100
        self.sentry_gun.turret_angle = new_angle
        angle = self.sentry_gun.turret_angle
        self.assertEqual(angle, utilities.unit_angle(new_angle))

    def test_entity_angle(self):
        self.assertAlmostEqual(self.sentry_gun.angle, utilities.unit_angle(self.sentry_gun.angle))
        new_angle = 100
        self.sentry_gun.angle = new_angle
        angle = self.sentry_gun.angle
        self.assertEqual(angle, utilities.unit_angle(new_angle))

    def test_attack_target(self):
        #self.sentry_gun.face_entity(self.zombie)
        self.sentry_gun.turret_angle = SentientEntity.get_angle(self.sentry_gun.location, self.zombie.location)
        for i in range(10):
            self.sentry_gun.brain.think()
        current_state_name = self.sentry_gun.brain.active_state.name
        #self.assertEqual(current_state_name, 'attack')
        self.assertEqual(self.sentry_gun.target, self.zombie)

        # Kill target and check if it returns to scan mode
        self.zombie.hp -= 10000
        self.sentry_gun.brain.think()
        current_state_name = self.sentry_gun.brain.active_state.name
        self.assertEqual(current_state_name, 'scan')
        self.assertIsNone(self.sentry_gun.target)   # it should no longer target dead zombie

        self.sentry_gun.target = None

        # Move the zombie somewhere it cannot be seen by the turret
        self.zombie.hp = 10
        x = self.sentry_gun.location.x + 100
        y = self.sentry_gun.location.y + 100
        self.zombie.location = Vector2(x, y)
        for i in range(10):
            self.sentry_gun.brain.think()
        self.assertIsNone(self.sentry_gun.target)  # No target since zombie is behind turret
        current_state_name = self.sentry_gun.brain.active_state.name
        self.assertEqual(current_state_name, 'scan')

