from encodings.punycode import selective_find

import pygame
from manager import ImageManager
from game import *
from pygame.locals import *
from pygame.math import Vector2
from mobs import *

image_manager = None

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    global image_manager
    image_manager = ImageManager('../data/images')

    world = World()
    sentry_gun = SentryGun(world, image_manager['sentrygun.png'], Vector2(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0))
    '''
    zombie = Zombie(world, image_manager['zombie.png'], Vector2(*pygame.mouse.get_pos()))
    zombie.hp = math.inf
    zombie.brain = StateMachine() # Reset brain to 0
    '''
    world.add_entity(sentry_gun)
    #world.add_entity(zombie)
    #sentry_gun.target = zombie

    time_passed = 0
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))
        world.process(time_passed)

        mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()
        mouse_location = Vector2(mouse_pos)
        #zombie.location = mouse_location
        if any(pygame.mouse.get_pressed()):
            spawn_zombie(world, mouse_location)

        # Draw center cross-hair lines:
        pygame.draw.line(screen, (255, 0, 0), (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))
        pygame.draw.line(screen, (255, 0, 0), (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

        world.render(screen)
        #print(sentry_gun.brain.active_state.name)
        #print('Entity count:', len(world.entities.keys()))
        #print(sentry_gun.turret_angle)
        #print(GameEntity.get_angle(sentry_gun.location, zombie.location))
        pygame.display.update()
        time_passed = clock.tick(FPS)

def spawn_zombie(world, mouse_location):
    zombie = Zombie(world, image_manager['zombie.png'], mouse_location)
    world.add_entity(zombie)
    print('There are {} entities in this world.'.format(len(world.entities.keys())))

if __name__ == '__main__':
    main()