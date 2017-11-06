import copy
import math
import pygame
from pygame.math import Vector2

FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = (640, 480)
TICK_SECOND = 1000 / FPS / 1000

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
VIOLET = (128, 0, 255)


class World:
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
        self.background = pygame.Surface(SCREEN_SIZE) #.convert()
        self.background.fill(BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def add_entity(self, entity):
        """Store an entity, give it an id and advance the current entity_id"""
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        if entity.id in self.entities.keys():
            del self.entities[entity.id]

    def get(self, entity_id):
        """Retrieve an entity by id"""
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def process(self, time_passed):
        """Update every entity in the world"""
        seconds_passed = time_passed / 1000.0
        entities_copy = copy.copy(self.entities)
        for entity in entities_copy.values():
            entity.process(seconds_passed)

    def render(self, surface):
        """Draw the background and all the entities"""
        surface.blit(self.background, (0, 0))
        for entity in self.entities.values():
            entity.render(surface)

    def get_close_entity(self, name, location, radius=100):
        """Find an entity within the radius of a location"""
        location = Vector2(*location)
        for entity in self.entities.values():
            if not entity.name == name:
                continue
            distance = location.distance_to(entity.location)
            if distance < radius:
                return entity
        return None

    def entities_with_name(self, name):
        def is_entity(entity):
            return entity.name == name
        return filter(is_entity, self.entities.values())

    def entity_count(self):
        return len(self.entities.values())