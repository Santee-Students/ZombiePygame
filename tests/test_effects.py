import copy
from effects import BulletTravelEffect, ExplosionEffect
from game import World
import unittest
from pygame.math import Vector2
from game import *


TICK_SECOND = 1000 / 30 / 1000 # One tick represented by 30 frames per second; 33 milliseconds


class BulletTravelEffectTestCase(unittest.TestCase):
    def setUp(self):
        self.world = World()
        '''
        self.origin = Vector2(0, SCREEN_HEIGHT)
        self.destination = Vector2(SCREEN_WIDTH, 0)
        self.bullet_effect = BulletTravelEffect(self.world, self.origin, self.destination)
        '''
        self.origin = Vector2(0, SCREEN_HEIGHT)
        self.destination = Vector2(SCREEN_WIDTH, 0)
        self.color = YELLOW
        #self.duration = 1 / 10  # 1/10th of a second
        self.bullet = BulletTravelEffect(self.world, self.origin, self.destination, color=self.color)
        self.world.add_entity(self.bullet)

    def test_instance(self):
        origin = Vector2(0, SCREEN_HEIGHT)
        destination = Vector2(SCREEN_WIDTH, 0)
        color = YELLOW
        duration = 1/10   # 1/10th of a second

        bullet = BulletTravelEffect(self.world, origin, destination, color=color, duration=duration)
        self.assertEqual(bullet.location, origin)
        self.assertEqual(bullet.destination, destination)
        self.assertEqual(bullet.color, color)
        self.assertEqual(bullet.remaining_time, duration)

    def test_location_destination(self):
        pass

    def test_fade(self):
        d = 1
        self.bullet.DURATION = d
        self.bullet.remaining_time = d  # seconds

        # Test when the bullet trail/line starts to fade
        self.bullet.process(TICK_SECOND)
        self.assertLess(self.bullet.remaining_time, self.bullet.DURATION)
        self.assertEqual(self.bullet.remaining_time, self.bullet.DURATION - TICK_SECOND)

    def test_remaining_zero(self):
        # Kill the effect
        self.bullet.remaining_time = 0
        self.bullet.process(TICK_SECOND)
        self.assertNotIn(self.bullet, self.world.entities.values())

    def test_bullet_travel(self):
        """Test the bullet_head and bullet_tail vectors"""
        self.assertEqual(self.bullet.fx_head, self.bullet.location)
        self.assertEqual(self.bullet.fx_tail, self.bullet.location)
        #self.assertEqual(self.bullet.fx_length, 100)
        heading = (self.bullet.destination - self.bullet.location).normalize()
        self.assertEqual(self.bullet.fx_heading, heading)

        # Do one TICK; the head should start moving, while the tail remains the same
        self.bullet.process(TICK_SECOND)
        travelled = (TICK_SECOND * self.bullet.fx_speed)
        self.assertEqual(self.bullet.fx_head.distance_to(self.bullet.location), travelled)
        self.assertEqual(self.bullet.fx_tail, self.bullet.location)

    def test_process_head(self):
        num_ticks = 1000
        ticks = list((TICK_SECOND for i in range(num_ticks)))
        tick_accumulate = 0
        expected_head = {}
        b = self.bullet

        # build expected head; assumptions of fx_head's whereabouts relative to tick_accumulate
        for tick in ticks:
            heading = (b.destination - b.location).normalize()
            new_location = b.fx_head + (heading * (tick_accumulate + tick)* b.speed)
            # ^ accumulate current tick since it is leading tail
            expected_head[tick_accumulate] = new_location
            tick_accumulate += tick

        tick_accumulate = 0
        for i, tick in enumerate(ticks):
            if b not in self.world.entities.values():
                # bullet is no longer in this world... but still exists as object;
                # eg. b's fx_head == fx_tail == fx_destination
                break
            with self.subTest(tick_accumulate=tick_accumulate, i=i):
                b.process(tick)
                expected = expected_head[tick_accumulate]
                if b.fx_head != b.destination:
                    self.assertEqual(expected, b.fx_head)
            tick_accumulate += tick

    def test_location(self):
        b = self.bullet
        self.assertEqual(b.fx_tail, b.location)
        self.assertEqual(b.fx_head, b.location)
        self.assertNotEqual(b.fx_head, b.destination)
        self.assertNotEqual(b.fx_tail, b.destination)
        self.assertIn(b, self.world.entities.values())

    def test_process_tail(self):
        self.assertIsNotNone(self.bullet)

        num_ticks = 1000
        ticks = list((TICK_SECOND for i in range(num_ticks)))
        tick_accumulate = 0
        expected_head = {}
        expected_tail = {}
        b = self.bullet
        self.assertIn(TICK_SECOND, ticks)
        self.assertEqual(num_ticks, len(ticks))

        # build expected tail; assumptions of fx_tail's whereabouts relative to tick_accumulate
        for tick in ticks:
            tail_heading = (b.destination - b.fx_tail).normalize()
            new_tail_location = b.fx_tail + (tail_heading * tick_accumulate * b.speed)
            expected_tail[tick_accumulate] = new_tail_location
            tick_accumulate += tick

        self.assertNotEqual(id(b.fx_tail), id(b.fx_head))

        tick_accumulate = 0
        for i, tick in enumerate(ticks):
            if b not in self.world.entities.values():
                break
            with self.subTest(tick_accumulate=tick_accumulate, i=i):
                b.process(tick)
                #print(expected_tail[tick_accumulate], b.fx_tail, sep='=')
                self.assertEqual(expected_tail[tick_accumulate], b.fx_tail)
            tick_accumulate += tick

    @unittest.skip
    def test_each_tick(self):
        # There's a bug here, where the length is far less than fx_length,
        # relative to a single tick and its speed... But visually, it's not a big problem.\

        num_ticks = 100
        ticks = list((TICK_SECOND for i in range(num_ticks)))
        b = self.bullet

        tick_accumulate = 0
        for tick in ticks:
            b.process(tick)
            with self.subTest(tick_accumulate=tick_accumulate):
                if b.fx_head != b.destination and b.fx_tail != b.destination and \
                                b.fx_tail != b.location and b.fx_head != b.location:
                    self.assertAlmostEqual(b.fx_head.distance_to(b.fx_tail), b.fx_length, 1)
            tick_accumulate += tick

    def test_die(self):
        """Effect should die when both fx_head/tail reaches destination"""
        self.bullet.fx_head = self.bullet.destination
        self.bullet.fx_tail = self.bullet.fx_head
        self.bullet.process(TICK_SECOND)
        self.assertNotIn(self.bullet, self.world.entities.values())


class ExplosionEffectTestCase(unittest.TestCase):
    def setUp(self):
        self.exp_radius = 50
        self.exp_duration = 1   # second
        self.world = World()
        self.exp_location = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        #self.exp_image = pygame.Surface((32, 32)).fill(RED)
        self.exp_color = RED
        self.explosion = ExplosionEffect(self.world, self.exp_location, self.exp_radius, self.exp_color)
        self.world.add_entity(self.explosion)

    def test_instantiate_radius(self):
        # Negative radius
        with self.assertRaises(ValueError):
            ExplosionEffect(self.world, self.exp_location, -1)

    def test_instantiate_color(self):
        # Color argument type
        with self.assertRaises(TypeError):
            ExplosionEffect(self.world, self.exp_location, self.exp_radius, color=1)
        # Color argument length
        with self.assertRaises(ValueError):
            ExplosionEffect(self.world, self.exp_location, self.exp_radius, color=(100,200))

    def test_die_radius_zero(self):
        self.explosion.radius = 0
        self.explosion.process(TICK_SECOND)
        self.assertNotIn(self.explosion, self.world.entities.values())

    def test_radius_shrink(self):
        """Explosion should shrink based on TICK"""
        old_radius = self.explosion.radius
        self.explosion.process(TICK_SECOND)
        self.assertLess(self.explosion.radius, old_radius)

        # num_ticks  = 0
        # while self.explosion.radius >= 0:
        #     self.explosion.process(TICK_SECOND)
        #     print('radius:', self.explosion.radius)
        #     num_ticks += 1
        # print(num_ticks)
