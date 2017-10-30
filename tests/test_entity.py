import unittest
from pygame.math import Vector2
from game import *
from entity import *

class GameEntityTestCase(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.ENTITY_WIDTH, self.ENTITY_HEIGHT = self.ENTITY_SIZE = (32, 32)
        self.entity_image = pygame.Surface(self.ENTITY_SIZE)

        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2
        self.entityA = GameEntity(self.world, 'dummy', self.entity_image, location=Vector2(x, y))

        x = SCREEN_WIDTH * 3 / 4
        y = SCREEN_HEIGHT * 3 / 4
        self.entityB = GameEntity(self.world, 'dummy', self.entity_image, location=Vector2(x, y))

    def test_face_entity(self):
        rotation_a = self.entityA.face_entity(self.entityB)

        # Manually calculate rotation
        vec_diff = self.entityB.location - self.entityA.location
        angle = -math.atan2(vec_diff.y, vec_diff.x)

        self.assertAlmostEqual(angle, rotation_a, 4)
        self.assertAlmostEqual(angle, self.entityA.angle, 4)

    def test_face_vector(self):
        # Do face_vector version:
        rotation_a = self.entityA.face_vector(self.entityB.location)

        # Manually calculate rotation
        vec_diff = self.entityB.location - self.entityA.location
        angle = -math.atan2(vec_diff.y, vec_diff.x)

        self.assertAlmostEqual(angle, rotation_a, 4)
        self.assertAlmostEqual(angle, self.entityA.angle, 4)

    def test_get_angle(self):
        angle = GameEntity.get_angle(self.entityA.location, self.entityB.location)

        # Manually calculate angle
        vec_diff = self.entityB.location - self.entityA.location
        calc_angle = -math.atan2(vec_diff.y, vec_diff.x)

        self.assertAlmostEqual(calc_angle, angle, 4)

