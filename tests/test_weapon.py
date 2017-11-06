import unittest
import utilities
from weapon import *
from game import *


@unittest.skip
class WeaponTestCase(unittest.TestCase):

    def setUp(self):
        self.world = World()

        self.weap_damage = 10        # per shot
        self.weap_clip = 5
        self.weap_reload_rate = 3    # per second
        self.weap_reload_full_clip = True   # If false, reload the amount by reload_rate
        self.weap_fire_rate = 2      # per second
        self.weap_spread = 1         # 0 is perfect accuracy; value is degrees.
        self.weap_rounds_per_shot = 1     # how much to decrease clip per shot
        self.weap_projectile_type = None      # None is instant
        self.weap_num_projectiles = 1  # Number of projectiles coming out of barrel when fired
        self.weap_projectile_speed = 100
        self.weap_warhead = None
        # Instant projectiles should be handled by the entity holding the weapon when firing.
        # They are still projectiles, but they just instantly the target if there are any in front of the entity.
        #self.wep_max_range = don't bother...
        self.weap_ammo_count = 10
        self.pistol = Weapon(self.weap_damage,
                             self.weap_clip,
                             self.weap_reload_rate,
                             self.weap_fire_rate,
                             self.weap_spread,
                             self.weap_rounds_per_shot,
                             self.weap_projectile_type,
                             self.weap_num_projectiles,
                             self.weap_projectile_speed,
                             self.weap_warhead,
                             reload_entire_clip=self.weap_reload_full_clip)

    def test_instantiate(self):
        pass

    @unittest.expectedFailure
    def test_shoot_at_angle(self):
        angle = utilities.unit_angle(math.radians(280))
        old_entity_count = self.world.entity_count()
        projectiles = self.pistol.shoot_at_angle(self.world, angle)
        self.assertGreater(self.world.entity_count(), old_entity_count)
        self.assertEqual(self.world.entity_count(), self.pistol.NUM_PROJECTILES)
        self.assertEqual(self.world.entity_count(), old_entity_count + self.pistol.NUM_PROJECTILES)

    @unittest.expectedFailure
    def test_shoot_at_destination(self):
        destination = Vector2(SCREEN_WIDTH, SCREEN_WIDTH)
        self.pistol.shoot_at_destination(self.world, destination)


    def test_process(self):
        """Weapons are affected by ticks, because of reload and fire rates"""
        self.pistol.clip = 0
        projectiles = self.pistol.shoot_angled(self.world, utilities.unit_angle(math.radians(100)))
        self.assertIsNone(projectiles)  # No projectiles shot since clip is empty

        self.pistol.process(TICK_SECOND)    # Calls reload
        projectiles = self.pistol.shoot_angled(self.world, utilities.unit_angle(math.radians(100)))
        self.assertIsNone(projectiles)  # No projectiles shot since clip is still empty

        self.pistol.process(self.weap_clip / self.weap_reload_rate + TICK_SECOND)
        projectiles = self.pistol.shoot_angled(self.world, utilities.unit_angle(math.radians(100)))
        self.assertIsNotNone(projectiles)

    def test_factory(self):
        pass


class ProjectileFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.warhead = None
        self.speed = 200
        self.angle = utilities.unit_angle(math.radians(45))
        self.projectile_type = Projectile
        self.factory = ProjectileFactory(self.projectile_type, self.location, self.speed, self.angle, None, self.warhead)


class WeaponSimplifiedTestCase(unittest.TestCase):
    def setUp(self):
        self.fire_rate = 3  # bullets per second
        self.world = World()
        self.owner_location = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.owner = GameEntity(self.world, 'dummy', None, self.owner_location)
        self.ammo = 9999
        self.damage = 10
        self.weapon = WeaponSimplified(self.world, self.owner, self.fire_rate, self.damage, self.ammo)

    def test_ammunition_decrease_on_fire(self):
        self.weapon.fire(1) # fire for 1 second
        self.assertEqual(self.weapon.ammo, self.ammo - self.fire_rate)

    def test_ammunition_decrease_1tick(self):
        self.weapon.fire(TICK_SECOND)
        self.assertEqual(self.weapon.ammo, self.ammo)
        self.assertEqual(self.weapon.accumulator, self.fire_rate * TICK_SECOND)

    def test_ammunition_decrease_2sec(self):
        seconds = 2
        self.weapon.fire(seconds)
        self.assertEqual(self.weapon.ammo, self.ammo - self.fire_rate * seconds)

    def test_bullets_spawned_on_fire(self):
        self.weapon.fire(1)
        self.assertEqual(self.world.entity_count(), self.fire_rate)

    def test_bullets_damage(self):
        self.weapon.fire(1)
        bullets = (e for e in self.world.entities.values() if e.name == 'bullet')
        for b in bullets:
            with self.subTest(bullet=b):
                self.assertEqual(b.damage, self.weapon.damage)

    def test_no_ammo(self):
        self.weapon.ammo = 0
        self.weapon.fire(TICK_SECOND)
        self.assertEqual(self.weapon.ammo, 0)
        self.assertEqual(self.weapon.accumulator, 0)    # accumulator = 0, since there is no more ammo
        