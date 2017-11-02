import copy
from effects import BulletTravelEffect
from game import World
import unittest
from pygame.math import Vector2
from game import *


TICK_SECONDS = 1000 / 30 / 1000 # One tick represented by 30 frames per second; 33 milliseconds


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
        self.bullet.process(TICK_SECONDS)
        self.assertLess(self.bullet.remaining_time, self.bullet.DURATION)
        self.assertEqual(self.bullet.remaining_time, self.bullet.DURATION - TICK_SECONDS)

    def test_remaining_zero(self):
        # Kill the effect
        self.bullet.remaining_time = 0
        self.bullet.process(TICK_SECONDS)
        self.assertNotIn(self.bullet, self.world.entities.values())

    def test_bullet_travel(self):
        """Test the bullet_head and bullet_tail vectors"""
        self.assertEqual(self.bullet.fx_head, self.bullet.location)
        self.assertEqual(self.bullet.fx_tail, self.bullet.location)
        #self.assertEqual(self.bullet.fx_length, 100)
        heading = (self.bullet.destination - self.bullet.location).normalize()
        self.assertEqual(self.bullet.fx_heading, heading)

        # Do one TICK; the head should start moving, while the tail remains the same
        self.bullet.process(TICK_SECONDS)
        travelled = (TICK_SECONDS * self.bullet.fx_speed)
        self.assertEqual(self.bullet.fx_head.distance_to(self.bullet.location), travelled)
        self.assertEqual(self.bullet.fx_tail, self.bullet.location)

        # Another;

    def test_process(self):
        num_ticks = 1000
        ticks = list((TICK_SECONDS for i in range(num_ticks)))
        tick_accumulate = 0
        expected_head = {}
        b = self.bullet

        # build expected head; assumptions of fx_head's whereabouts relative to tick_accumulate
        for tick in ticks:
            heading = (b.destination - b.location).normalize()
            new_location = b.fx_head + (heading * tick_accumulate * b.speed)
            expected_head[tick_accumulate] = new_location
            tick_accumulate += tick

        tick_accumulate = 0
        for tick in ticks:
            if b not in self.world.entities.keys():
                # bullet is no longer in this world... but still exists as object;
                # eg. b's fx_head == fx_tail == fx_destination
                break
            with self.subTest(tick=tick):
                b.process(tick)
                self.assertEqual(expected_head[tick_accumulate], b.location)
            tick_accumulate += tick

    @unittest.skip
    def test_bullet_travel_part2(self):
        # Fast forward.... The tail should start moving once it reaches the desired fx_length

        self.bullet.speed = 10
        dt = (self.bullet.fx_length / self.bullet.fx_speed) + 5 * TICK_SECONDS    # +TICK is extra
        self.bullet.process(dt)
        self.bullet.process(TICK_SECONDS)

        # generate tic seconds to simulate flow and do asserts within...

        #self.assertIn(self.bullet, self.world.entities.values())
        self.assertAlmostEqual(self.bullet.fx_length, self.bullet.fx_head.distance_to(self.bullet.fx_tail))
        self.assertAlmostEqual(self.bullet.fx_head.distance_to(self.bullet.fx_tail), self.bullet.fx_length, 1)

    @unittest.expectedFailure
    def test_bullet_travel_part3(self):
        """This is when fx_head has reached the destination, and fx_tail is still catching up"""
        self.bullet.fx_head = Vector2(self.bullet.destination) - Vector2(self.bullet.fx_heading)
        self.bullet.process(TICK_SECONDS)
        self.assertGreater(self.bullet.fx_head.distance_to(self.bullet.fx_tail))
        #print(self.bullet.fx_head == self.bullet.destination)

        tail = Vector2(self.bullet.fx_tail)
        self.bullet.process(TICK_SECONDS)
        print('tail', self.bullet.fx_tail)
        print('head', self.bullet.fx_head)
        print('tail to head', self.bullet.fx_tail.distance_to(self.bullet.fx_head))
        self.assertNotEqual(self.bullet.fx_tail, tail)

        self.assertLess(self.bullet.fx_tail.distance_to(self.bullet.fx_head), self.bullet.fx_length)

    def test_die(self):
        """Effect should die when both fx_head/tail reaches destination"""
        self.bullet.fx_head = self.bullet.destination
        self.bullet.fx_tail = self.bullet.fx_head
        self.bullet.process(TICK_SECONDS)
        self.assertNotIn(self.bullet, self.world.entities.values())