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
        self.entityA = SentientEntity(self.world, 'dummy', self.entity_image, location=Vector2(x, y))

        x = SCREEN_WIDTH * 3 / 4
        y = SCREEN_HEIGHT * 3 / 4
        self.entityB = SentientEntity(self.world, 'dummy', self.entity_image, location=Vector2(x, y))

    def test_face_entity(self):
        rotation_a = self.entityA.face_entity(self.entityB)

        # Manually calculate rotation
        vec_diff = self.entityB.location - self.entityA.location
        angle = utilities.unit_angle(-math.atan2(vec_diff.y, vec_diff.x))

        self.assertAlmostEqual(angle, rotation_a, 4)
        self.assertAlmostEqual(angle, self.entityA.angle, 4)

    def test_face_vector(self):
        # Do face_vector version:
        rotation_a = self.entityA.face_vector(self.entityB.location)

        # Manually calculate rotation
        vec_diff = self.entityB.location - self.entityA.location
        angle = utilities.unit_angle(-math.atan2(vec_diff.y, vec_diff.x))

        self.assertAlmostEqual(angle, rotation_a, 4)
        self.assertAlmostEqual(angle, self.entityA.angle, 4)

    def test_get_angle(self):
        angle = SentientEntity.get_angle(self.entityA.location, self.entityB.location)

        # Manually calculate angle
        vec_diff = self.entityB.location - self.entityA.location
        calc_angle = utilities.unit_angle(-math.atan2(vec_diff.y, vec_diff.x))

        self.assertAlmostEqual(calc_angle, angle, 4)


class GameEntityBoundaryRectTestCase(unittest.TestCase):
    def setUp(self):
        self.dummy_surf = pygame.Surface((32, 32))
        self.location = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.world = World()
        self.entity = GameEntity(self.world, 'dummy', self.dummy_surf, self.location)
        self.world.add_entity(self.entity)

        # What we're interested in:
        self.rect_width = 16  # surface may have 32px width, but entity should really be 16px when performing things
        self.rect_height = 32
        self.boundary_rect = pygame.Rect((0, 0), (self.rect_width, self.rect_height))  # note: x/y don't matter
        self.boundary_rect_offset = Vector2(-self.rect_width / 2, -self.rect_height)  # Offset from entity.location

    def test_set_boundary_rect(self):
        self.entity.set_rect(self.boundary_rect)  # Should ignore rect x and y...
        self.assertEqual(self.entity._GameEntity__rect.width, self.boundary_rect.width)
        self.assertEqual(self.entity._GameEntity__rect.height, self.boundary_rect.height)

    def test_set_boundary_rect_with_offset(self):
        self.entity.set_rect(self.boundary_rect, self.boundary_rect_offset)  # Should ignore rect x and y...
        self.assertEqual(self.entity._GameEntity__rect, self.boundary_rect)
        self.assertEqual(self.entity._GameEntity__rect_offset, self.boundary_rect_offset)

    def test_get_boundary_rect(self):
        self.entity.set_rect(self.boundary_rect)
        rect = self.entity.get_rect()

        self.assertEqual(self.entity._GameEntity__rect.width, rect.width)
        self.assertEqual(self.entity._GameEntity__rect.height, rect.height)
        # Because there is no offset, the rect will be centered to location
        self.assertEqual(rect.x, self.entity.location.x - rect.width / 2)
        self.assertEqual(rect.y, self.entity.location.y - rect.height / 2)

    def test_get_boundary_rect_with_offsets(self):
        self.entity.set_rect(self.boundary_rect, self.boundary_rect_offset)
        rect = self.entity.get_rect()
        loc = self.entity.location
        brect = self.boundary_rect

        self.assertEqual(rect.x, loc.x - brect.width / 2 + self.boundary_rect_offset.x)
        self.assertEqual(rect.y, loc.y - brect.height / 2 + self.boundary_rect_offset.y)

    def test_get_boundary_rect_no_rect_height_width_only(self):
        """Test the get_rect() method to return the entity's image rect instead of rect when there is none assigned.
        This test will not concern the entity's rectangle's X/Y coordinates."""
        rect = self.entity.get_rect()
        image_rect = self.entity.image.get_rect()

        self.assertEqual(rect.width, image_rect.width)
        self.assertEqual(rect.height, image_rect.height)

    def test_get_boundary_rect_no_rect(self):
        """Continuation of above, but considers x and y attributes"""
        rect = self.entity.get_rect()
        image_rect = self.entity.image.get_rect()

        self.assertEqual(rect.x, self.location.x - image_rect.width / 2)
        self.assertEqual(rect.y, self.location.y - image_rect.height / 2)


class SentientEntitySidesTestCase(unittest.TestCase):
    def setUp(self):
        self.world = World()
        self.good_guy_name = 'good_guy'
        self.bad_guy_name = 'bad_fuy'
        self.other_bad_guy_name = 'bad_man'

        self.good_guy = SentientEntity(self.world, self.good_guy_name, None, Vector2(100, 100), speed=0,
                                       enemies=[self.bad_guy_name, self.other_bad_guy_name])
        self.bad_guy = SentientEntity(self.world, self.bad_guy_name, None, Vector2(150, 140), speed=0,
                                      enemies=[self.good_guy_name])
        self.bad_guy2 = SentientEntity(self.world, self.other_bad_guy_name, None,
                                       Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), speed=0,
                                       enemies=[self.good_guy_name])
        self.world.add_entity(self.good_guy)
        self.world.add_entity(self.bad_guy)
        self.world.add_entity(self.bad_guy2)

    def test_get_enemy_entity(self):
        enemy = self.good_guy.get_close_enemy(radius=100)
        self.assertIsNotNone(enemy)
        self.assertIn(enemy.name, self.good_guy.enemies)

    def test_get_enemy_entity_other_bad_guy(self):

        # Replace other bad guy's location with first bad guys', and put the first far away
        temp_loc = self.bad_guy.location
        self.bad_guy.location = Vector2(*SCREEN_SIZE)
        self.bad_guy2.location = temp_loc

        enemy = self.good_guy.get_close_enemy(radius=100)
        self.assertIsNotNone(enemy)
        self.assertIn(enemy.name, self.good_guy.enemies)
        self.assertEqual(enemy.name, self.other_bad_guy_name)

    def test_get_enemy_entity_beyond_radius(self):
        self.good_guy.location = (0, 0)
        self.bad_guy.location = Vector2(*SCREEN_SIZE)
        self.bad_guy2.location = Vector2(*SCREEN_SIZE)

        enemy = self.good_guy.get_close_enemy(radius=100)
        self.assertIsNone(enemy)
