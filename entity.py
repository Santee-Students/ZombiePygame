from pygame.math import Vector2
import math
import pygame
import utilities
#from mobs import *


class GameEntity:
    """GameEntity that has states"""
    def __init__(self, world, name, image, location=None, destination=None, speed=0):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(location) if location is not None else Vector2(0, 0)
        self.destination = Vector2(destination) if destination is not None else Vector2(0, 0)
        self.speed = speed
        self.id = 0
        self.__angle = 0.0
        self.__rect = None    # represents the boundary rectangle
        self.__rect_offset = None
        self.render_offset = None  # how much to offset the image by (relative to location) when rendering to a surface

    @property
    def angle(self):
        return utilities.unit_angle(self.__angle)

    @angle.setter
    def angle(self, angle):
        self.__angle = utilities.unit_angle(angle)

    def render(self, surface):
        if self.image is None:
            return

        x, y = 0, 0
        if self.render_offset is not None:
            x = self.location.x + self.render_offset.x
            y = self.location.y + self.render_offset.y
        else:
            x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x - w / 2, y - h / 2))

    def process(self, seconds_passed):
        if self.speed > 0 and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.length()
            heading = vec_to_destination.normalize()
            travel_distance = min(distance_to_destination, seconds_passed * self.speed)
            self.location += travel_distance * heading

    def face_vector(self, vector):
        """Face the entity towards the vector's location, set the new angle, and return it"""
        vec_diff = vector - self.location
        new_angle = self.get_angle(self.location, vector)
        self.angle = new_angle
        return new_angle

    def face_entity(self, entity):
        """Face the entity towards the other entity's location, set the new angle, and return it"""
        return self.face_vector(entity.location)

    @staticmethod
    def get_angle(vectora, vectorb):
        """Retrieve the angle (radians) between vectora and vectorb, where vectorb is the end point, and
        vectora, the starting point"""
        vec_diff = vectorb - vectora
        #return -math.atan2(vec_diff.y, vec_diff.x)
        return utilities.unit_angle(-math.atan2(vec_diff.y, vec_diff.x))

    def set_rect(self, rect, vec_offset=None):
        self.__rect = rect
        if vec_offset is not None:
            self.__rect_offset = vec_offset

    def get_rect(self):
        if self.__rect is not None:
            new_rect = pygame.Rect(self.__rect)
            new_rect.center = self.location
            if self.__rect_offset is not None:
                new_rect.x += self.__rect_offset.x
                new_rect.y += self.__rect_offset.y
            return new_rect

        img_rect = self.image.get_rect()
        img_rect.center = self.location
        return img_rect

    @property
    def rect(self):
        return self.get_rect()


class SentientEntity(GameEntity):
    """GameEntity that has states, and is able to think..."""

    def __init__(self, world, name, image, location=None, destination=None, speed=0, friends=None, enemies=None):
        super().__init__(world, name, image, location, destination, speed)
        self.friends = friends
        self.enemies = enemies
        self.brain = StateMachine()

    def process(self, seconds_passed):
        self.brain.think()
        super().process(seconds_passed)

    def get_close_enemy(self, radius=100):
        for enemy in self.enemies:
            e = self.world.get_close_entity(enemy, self.location, radius)
            if e is not None:
                return e
        return None


class State:

    def __init__(self, name):
        self.name = name

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateMachine:

    def __init__(self):
        self.states = {}
        self.active_state = None

    def add_state(self, state):
        """Add a state to the internal dictionary"""
        self.states[state.name] = state

    def think(self):
        """Let the current state do it's thing"""

        # Only continue if there is an
        if self.active_state is None:
            return

        # Perform the actions of the active state and check conditions
        self.active_state.do_actions()

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):
        """Change state machine's active state"""

        # perform any exit actions of the current state
        if self.active_state is not None:
            self.active_state.exit_actions()

        if new_state_name not in self.states.keys():
            print('Warning! "{}" not in self.states...'.format(new_state_name))
            return

        # Switch state and perform entry actions of new state
        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()


