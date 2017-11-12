import sys
import pygame
from pygame.math import Vector2
from game import *
from pygame.locals import *
from weapon import Projectile, WeaponSimplified
from entity import GameEntity
import utilities

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Projectile object demonstration')
clock = pygame.time.Clock()
world = World()
CENTER_VEC = Vector2(SCREEN_CENTER)
AMMO = 10000
SPREAD = 10
FIRE_RATE = 10

def main():
    time_passed = 0
    player = GameEntity(world, 'player', None, CENTER_VEC)
    world.add_entity(player)

    weapon = WeaponSimplified(world, player, FIRE_RATE, 0, AMMO, spread=SPREAD)

    ready2fire_surf = pygame.Surface((32, 32))
    #font_obj = pygame.SysFont()
    #print('\n'.join(pygame.font.get_fonts()))
    font_obj = pygame.font.SysFont('freesans', 32)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONDOWN:
                pass
                #print(world.entity_count())
            elif event.type == MOUSEMOTION:
                angle = GameEntity.get_angle(player.location, Vector2(event.pos))
                player.angle = angle
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    weapon.ammo = AMMO

        seconds_passed = time_passed / 1000

        lmb, mmb, rmb = pygame.mouse.get_pressed()
        if any((lmb, mmb, rmb)):
            weapon.fire()

        world.process(time_passed)
        weapon.process(seconds_passed)

        screen.fill(BLACK)
        world.render(screen)
        ready2fire_surf.fill(GREEN if weapon.ready_to_fire else RED)
        screen.blit(ready2fire_surf, (0, 0))
        ready2fire_text = font_obj.render('ready' if weapon.ready_to_fire else 'loading',
                        True,
                        WHITE)
        screen.blit(ready2fire_text, (32, 0))

        pygame.display.set_caption('Weapon demo; Ammo: {ammo}'.format(ammo=weapon.ammo))

        pygame.display.update()
        time_passed = clock.tick(FPS)
    pass


# def spawn_projectile(from_pos, to_pos):
#     direction = (Vector2(to_pos) - Vector2(from_pos)).normalize()
#     proj = Projectile(world, 'bullet', None, CENTER_VEC, direction, max_distance=100)
#     world.add_entity(proj)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()