from pygame.math import Vector2
import math
import pygame
import utilities


class GameEntity:
    def __init__(self, world, name, image, location=None):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(location) if location is not None else Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0.0
        self.brain = StateMachine()
        self.id = 0
        self.__angle = 0.0

    @property
    def angle(self):
        return utilities.unit_angle(self.__angle)

    @angle.setter
    def angle(self, angle):
        self.__angle = utilities.unit_angle(angle)

    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x - w / 2, y - h / 2))

    def process(self, seconds_passed):
        self.brain.think()
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


