import time
import sys
import pygame
from game import *
from effects import *
from pygame.locals import *
from manager import ImageManager

GREEN = (0, 255, 0)
FPS = 30

"""
bullet_travel = BulletTravelEffect(world, Vector2(0, 0), Vector2(320, 240))
world.add_entity(bullet_travel)
"""

image_dude = None

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((640, 480))
    world = World()

    global image_dude
    image_dude = ImageManager('../data/images')

    time_passed = 0
    while True:
        #print(time_passed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                print(event)
                if event.button is 1:
                    spawn_effect(world)
                    print('fx added')
            elif event.type == KEYDOWN:
                if event.key == K_e:
                    spawn_explosion_effect(world)
                elif event.key == K_i:
                    # Show entities
                    print(world.entities.values())


        if pygame.mouse.get_pressed()[2]:
            spawn_effect(world)

        # if pygame.mouse.get_pressed()[3]:
        #     print('world entities:')
        #     print(world.entities.values())

        world.process(time_passed)

        screen.fill((0, 0, 0))
        world.render(screen)
        # pygame.draw.circle(screen, RED, pygame.mouse.get_pos(), 5)

        pygame.display.update()

        # simulate FPS drop
        #time.sleep(0.2)

        time_passed = clock.tick(FPS)


def spawn_effect(world):
    bullet_fx = BulletTravelEffect(world, Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
                                   Vector2(*pygame.mouse.get_pos()), GREEN, speed=500)
    world.add_entity(bullet_fx)


def spawn_explosion_effect(world):
    explosion = ExplosionEffect(world, Vector2(*pygame.mouse.get_pos()), 50, color=VIOLET)
    world.add_entity(explosion)


if __name__ == '__main__':
    main()