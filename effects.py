"""This is where effects go. eg. Explosions, bullet effects, etc. that disappear in time"""

from entity import GameEntity
from game import *
import math


class BulletTravelEffect(GameEntity):

    def __init__(self, world, origin, destination, color=YELLOW, speed=1000, length=50, duration=math.inf):
        super().__init__(world, 'bullet_travel', None, origin, destination)
        self.color = color
        self.DURATION = duration
        self.remaining_time = self.DURATION
        self.fx_head = Vector2(self.location)
        self.fx_tail = Vector2(self.location)
        self.fx_length = length
        self.fx_heading = (self.destination - self.location).normalize()
        self.fx_speed = speed
        self.stop_fx_head = False

    @property
    def fx_speed(self):
        return self.speed

    @fx_speed.setter
    def fx_speed(self, new_value):
        self.speed = new_value

    def process(self, seconds_passed):
        if self.fx_head != self.destination:
            head_to_destination_vec = self.destination - self.fx_head
            head_heading = head_to_destination_vec.normalize()
            distance = min(self.speed * seconds_passed, head_to_destination_vec.length())
            self.fx_head += head_heading * distance

        if self.fx_tail != self.destination and (self.fx_head.distance_to(self.location) >= self.fx_length or self.fx_head == self.destination):
            tail_to_destination_vec = self.destination - self.fx_tail
            tail_heading = tail_to_destination_vec.normalize()
            distance = min(tail_to_destination_vec.length(), self.speed * seconds_passed)
            self.fx_tail += tail_heading * distance

        self.remaining_time -= seconds_passed
        if self.remaining_time <= 0 or (self.fx_tail == self.fx_head == self.destination):
            self.world.remove_entity(self)
            print('dead')


    def render(self, surface):
        pygame.draw.aaline(surface, self.color, self.fx_tail, self.fx_head)
