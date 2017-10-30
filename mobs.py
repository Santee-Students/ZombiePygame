from random import randint
from entity import *
from game import *
from pygame.math import Vector2
import math
import utilities

class Zombie(GameEntity):
    """A Zombie wandering aimlessly"""

    def __init__(self, world, image, location):
        super().__init__(world, 'zombie', image, location)
        self.brain.add_state(ZombieExploreState(self))
        self.brain.add_state(ZombieAttackState(self))
        self.brain.set_state('explore')
        self.MAX_HP = 10
        self.hp = self.MAX_HP
        self.speed = 50

    def process(self, seconds_passed):
        super().process(seconds_passed)
        if self.hp <= 0:
            self.world.remove_entity(self)

    def shot(self):
        pass


class ZombieExploreState(State):
    def __init__(self, zombie):
        super().__init__('explore')
        self.entity = zombie

    def do_actions(self):
        # Change directions at least every 10th frame
        if randint(0, 100) == 1:
            self.random_destination()

    def check_conditions(self):
        if self.entity.hp < self.entity.MAX_HP:
            return 'attack'
        return None

    def random_destination(self):
        lower_x_boundary = int(self.entity.image.get_width() / 2)
        lower_y_boundary = int(self.entity.image.get_height() / 2)
        upper_x_boundary = int(SCREEN_WIDTH - lower_x_boundary)
        upper_y_boundary = int(SCREEN_HEIGHT - lower_y_boundary)
        x = randint(lower_x_boundary, upper_x_boundary)
        y = randint(lower_y_boundary, upper_y_boundary)
        self.entity.destination = Vector2(x, y)


class ZombieAttackState(ZombieExploreState):
    """Select a random survivor to attack until either is dead."""

    def __init__(self, zombie):
        super().__init__(zombie)
        self.name = 'attack'
        self.zombie = zombie
        self.has_killed = False
        self.target = None
        self.original_speed = -1
        self.reset_state()

    def entry_actions(self):
        #print('entering attack state...')
        self.original_speed = self.zombie.speed
        self.zombie.speed = 200
        self.acquire_target()

    def acquire_target(self):
        if self.target is not None:
            return
        target = self.zombie.world.get_close_entity('survivor', self.zombie.location, radius=50)
        if target is not None:
            self.target = target

    def do_actions(self):
        if self.target is None:
            if randint(1, 10) == 1:
                self.random_destination()
            self.acquire_target()
            return
        self.zombie.destination = self.target.location
        if self.zombie.location.distance_to(self.target.location) < 5:
            self.target.hp -= 1
            if self.target.hp <= 0:
                self.has_killed = True

    def check_conditions(self):
        if self.has_killed:
            return 'explore'
        return None

    def exit_actions(self):
        self.zombie.hp = self.zombie.MAX_HP # replenish zombie health
        self.reset_state()

    def reset_state(self):
        self.zombie.speed = self.original_speed
        self.has_killed = False
        self.target = None


class Survivor(GameEntity):
    """A survivor shooting at zombies"""

    def __init__(self, world, image, location):
        super().__init__(world, 'survivor', image, location)
        self.brain.add_state(SurvivorExploreState(self))
        self.brain.add_state(SurvivorPanicState(self))
        self.brain.set_state('explore')
        self.MAX_HP = 20
        self.hp = self.MAX_HP
        self.speed = 50

    def process(self, seconds_passed):
        super().process(seconds_passed)
        if self.hp <= 0:
            self.world.remove_entity(self)

    def shot(self):
        pass


class SurvivorExploreState(ZombieExploreState):
    def __init__(self, survivor):
        super().__init__(survivor)

    def do_actions(self):
        # Change directions at least every 100th frame
        if randint(0, 100) == 1:
            self.random_destination()

    def check_conditions(self):
        zombies = tuple(self.entity.world.entities_with_name('zombie'))
        if self.entity.hp < self.entity.MAX_HP and len(zombies) > 0:
            return 'panic'
        return None


class SurvivorPanicState(SurvivorExploreState):
    def __init__(self, survivor):
        super().__init__(survivor)
        self.name = 'panic'
        self.original_speed = self.entity.speed

    def entry_actions(self):
        self.original_speed = self.entity.speed
        self.entity.speed = 300

    def do_actions(self):
        # Change directions frequently
        if randint(0, 10) == 1:
            self.random_destination()

    def check_conditions(self):
        # Survivor should stop panicking once there are no more zombies...
        zombies = tuple(self.entity.world.entities_with_name('zombie'))

        #if not any(zombies):
        if len(zombies) <= 0:
            return 'explore'
        return None

    def exit_actions(self):
        self.entity.speed = self.original_speed


class SentryGun(GameEntity):
    def __init__(self, world, image, location):
        super().__init__(world, 'sentry_gun', image, location)
        self.TURRET_ROTATION_RATE_DEGREES = 180
        self.turret_rotation_rate = math.radians(self.TURRET_ROTATION_RATE_DEGREES) # radians per second
        self.__turret_angle = 0
        self.speed = 0
        self.target = None
        self.CONE_OF_VISION_DEGREES = 60
        self.cone_of_vision = math.radians(self.CONE_OF_VISION_DEGREES)    # radians

        self.brain.add_state(self.ScanEnvironment(self))
        self.brain.add_state(self.AttackTargetState(self))
        self.brain.set_state('scan')

    def process(self, seconds_passed):
        super().process(seconds_passed)
        if self.target is None:
            self.turret_angle += self.turret_rotation_rate * seconds_passed
            return

        # Rotate towards the target
        angle = GameEntity.get_angle(self.location, self.target.location)
        self.turret_angle = angle
        # attack target
        self.target.hp -= 1

    def render(self, surface):
        rotated_image = pygame.transform.rotate(self.image, math.degrees(self.turret_angle))
        x, y = self.location
        w, h = rotated_image.get_size()
        surface.blit(rotated_image, (x - w / 2, y - h / 2))

    def turret_face_entity(self, entity):
        angle = GameEntity.get_angle(self.location, entity.location)
        self.turret_angle = angle

    @property
    def turret_angle(self):
        return utilities.unit_angle(self.__turret_angle)

    @turret_angle.setter
    def turret_angle(self, angle):
        self.__turret_angle = utilities.unit_angle(angle)

    class ScanEnvironment(State):
        def __init__(self, turret):
            super().__init__('scan')
            self.turret = turret

        def entry_actions(self):
            #self.turret.target = None
            pass

        def check_conditions(self):
            """Scan surroundings by scanning all enemies around"""
            half_cone = self.turret.cone_of_vision / 2
            turret_angle = utilities.unit_angle(self.turret.turret_angle)

            def is_zombie(entity):
                return entity.name == 'zombie'
            zombies = filter(is_zombie, self.turret.world.entities.values())

            for zombie in zombies:
                angle = GameEntity.get_angle(self.turret.location, zombie.location)
                if turret_angle - half_cone < angle <= turret_angle + half_cone:
                    self.turret.target = zombie
                    #print('New target:', zombie)
                    return 'attack'

    '''
    class FaceTargetState(State):
        def __init__(self, turret):
            super().__init__('facing')
            self.turret = turret
    '''

    class AttackTargetState(State):
        def __init__(self, turret):
            super().__init__('attack')
            self.turret = turret

        def check_conditions(self):
            if self.turret.target.hp > 0 and self.turret.target is not None:
                return
            return 'scan'

        def exit_actions(self):
            self.turret.target = None
