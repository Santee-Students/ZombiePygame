import sys
import pygame
from pygame.math import Vector2
from game import *
from pygame.locals import *
from weapon import Projectile

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Projectile object demonstration')
clock = pygame.time.Clock()
world = World()
CENTER_VEC = Vector2(SCREEN_CENTER)


def main():
    time_passed = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONDOWN:
                spawn_projectile(CENTER_VEC, event.pos)
                print(world.entity_count())

        lmb, mmb, rmb = pygame.mouse.get_pressed()
        if lmb:
            spawn_projectile(CENTER_VEC, event.pos)

        world.process(time_passed)

        screen.fill(BLACK)
        world.render(screen)

        pygame.display.update()
        time_passed = clock.tick(FPS)
    pass


def spawn_projectile(from_pos, to_pos):
    direction = (Vector2(to_pos) - Vector2(from_pos)).normalize()
    print('dir', direction)
    proj = Projectile(world, 'bullet', None, CENTER_VEC, direction, max_distance=100)
    world.add_entity(proj)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()