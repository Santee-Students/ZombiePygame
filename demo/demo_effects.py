import sys
import pygame
from game import *
from effects import *
from pygame.locals import *


GREEN = (0, 255, 0)

"""
bullet_travel = BulletTravelEffect(world, Vector2(0, 0), Vector2(320, 240))
world.add_entity(bullet_travel)
"""

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((640, 480))
    world = World()

    time_passed = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                print(event)
                if event.button is not 1:
                    continue
                spawn_effect(world)
                print('fx added')


        if pygame.mouse.get_pressed()[0]:
            spawn_effect(world)
        if pygame.mouse.get_pressed()[2]:
            print('world entities:')
            print(world.entities.values())


        world.process(time_passed)

        screen.fill((0, 0, 0))
        world.render(screen)

        pygame.display.update()
        time_passed = clock.tick(FPS)


def spawn_effect(world):
    bullet_fx = BulletTravelEffect(world, Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
                                   Vector2(*pygame.mouse.get_pos()), GREEN)
    world.add_entity(bullet_fx)


if __name__ == '__main__':
    main()