from random import *
from entity import *
from game import *

'''
self.pistol = Weapon(self.weap_damage, \
                     self.weap_clip, \
                     self.weap_reload_rate, \
                     self.weap_fire_rate, \
                     self.weap_spread, \
                     self.weap_rounds_per_shot, \
                     self.weap_projectile_type, \
                     self.weap_projectile_count)
'''


class Weapon:
    def __init__(self,
                 damage=1,
                 clip=1,
                 max_ammo=90,
                 reload_rate=1,
                 fire_rate=1,
                 spread=0,
                 rounds_per_shot=1,
                 proj_type=None,
                 num_proj=1,
                 proj_speed=100,
                 warhead=None,
                 factory=None,
                 reload_entire_clip=True,
                 projectile_factory=None):

        if factory is not None:
            factory(self)

        self.DAMAGE = damage
        self.clip = clip
        self.MAX_CLIP = clip
        self.MAX_AMMO = max_ammo
        self.RELOAD_RATE = reload_rate
        self.FIRE_RATE = fire_rate
        self.SPREAD = spread
        self.ROUNDS_PER_SHOT = rounds_per_shot
        self.PROJECTILE_TYPE = proj_type
        self.NUM_PROJECTILES = num_proj
        self.PROJECTILE_SPEED = proj_speed
        self.WARHEAD=warhead
        self.ready = True
        self.reload_entire_clip = reload_entire_clip

    def shoot_angled(self, world, angle):
        """Shoot the projectiles at an angle, and add them into the world"""
        pass

    def process(self, seconds_passed):
        if self.clip == 0:
            # reload
            self.reload(seconds_passed)

        if self.is_ready():
            pass

    def reload(self, seconds_passed):
        self.clip += self.RELOAD_RATE * seconds_passed
        # if self.clip > self.MAX_CLIP:


class ProjectileFactory:
    """Class that gives a new projectile object each time it is called.
    An instance of it will reside in a weapon object."""
    def __init__(self, ptype, speed, image, warhead):
        pass


class Projectile(GameEntity):

    def __init__(self, world, name, image, location, direction_vec, speed=200, damage=0, max_distance=300, owner=None):
        super().__init__(world, name, image, location, None, speed)
        self.direction = direction_vec
        self.damage = damage
        self.origin = location
        self.max_distance = max_distance
        self.owner = owner

    def process(self, seconds_passed):
        if self.location.distance_to(self.origin) >= self.max_distance:
            self.world.remove_entity(self)
            return
        self.location += self.direction * self.speed * seconds_passed

    def render(self, surface):
        if self.image is not None:
            super().render(surface)
            return
        pygame.draw.circle(surface, YELLOW, (int(self.location.x), int(self.location.y)), 1)

    @staticmethod
    def factory(type_name, world, owner, weapon):
        angle = owner.angle if not hasattr(owner, 'turret_angle') else owner.turret_angle
        angle *= -1 # Multiply by -1 to fix direction vector
        direction = Vector2(1, 0).rotate(math.degrees(angle) + uniform(-weapon.spread/2, weapon.spread/2))

        if type_name == 'bullet':
            return Projectile(world, 'bullet', None, owner.location, direction, speed=500, damage=weapon.damage, owner=owner)
        raise ValueError('Unknown projectile type name {}'.format(type_name))


class Warhead:
    pass


class WeaponSimplified(SentientEntity):
    """A simple weapon that fires without reload; just a delay in between."""

    def __init__(self, world, owner, fire_rate, damage, ammo, spread=0):
        self.world = world
        self.owner = owner
        self.fire_rate = fire_rate
        self.damage = damage
        self.ammo = ammo
        self.accumulator = 0
        self.spread = spread
        self.ready_to_fire = True

    def render(self, surface):
        return

    def process(self, seconds_passed):
        if self.ammo <= 0:
            self.accumulator = 0
            return
        if self.ready_to_fire:
            return

        if self.accumulator >= 1 / self.fire_rate:
            self.accumulator = 0
            self.ready_to_fire = True
        self.accumulator += seconds_passed

    def fire(self):
        if not self.ready_to_fire or self.ammo <= 0:
            return

        self.ready_to_fire = False
        bullet = Projectile.factory('bullet', self.world, self.owner, self)
        self.world.add_entity(bullet)
        self.ammo -= 1