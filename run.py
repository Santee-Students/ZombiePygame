import pygame
from pygame.locals import *
from game import *
import sys
import mobs
from manager import ImageManager
from random import randint

image_dude = None

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Zombie Defence v0.0.0')
    clock = pygame.time.Clock()
    world = World()
    global image_dude
    image_dude = ImageManager('data/images/')
    setup_world(world)

    time_passed = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()

        # Dirty way of attacking the enemy
        lmb, mmb, rmb = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if lmb:
            e = world.get_close_entity('zombie', Vector2(mouse_x, mouse_y), radius=32)
            if e is not None:
                print('zombie found @ {}; state: {}'.format(e.location, e.brain.active_state.name))
                e.hp -= 1

        world.process(time_passed)

        screen.fill(BLACK)
        world.render(screen)

        pygame.display.update()
        time_passed = clock.tick(FPS)

def quit_game():
    pygame.quit()
    sys.exit()

def setup_world(world):
    # Create RED sprite for zombie
    zombie_surf = pygame.Surface((32, 32)).convert()
    zombie_surf.fill(RED)

    for i in range(10):
        z_width, z_height = zombie_surf.get_size()
        randx = randint(z_width / 2, SCREEN_WIDTH - z_width / 2)
        randy = randint(z_height / 2, SCREEN_HEIGHT - z_height / 2)
        z_location = Vector2(randx, randy)
        zombie = mobs.Zombie(world, zombie_surf, z_location)
        world.add_entity(zombie)

    survivor_surf = pygame.Surface((32, 32)).convert()
    survivor_surf.fill(GREEN)
    for i in range(5):
        s_width, s_height = survivor_surf.get_size()
        randx = randint(s_width / 2, SCREEN_WIDTH - s_width / 2)
        randy = randint(s_height / 2, SCREEN_HEIGHT - s_height / 2)
        s_location = Vector2(randx, randy)
        survivor = mobs.Survivor(world, survivor_surf, s_location)
        world.add_entity(survivor)

    sentry_gun_surf = image_dude['sentrygun.png']
    w, h = sentry_gun_surf.get_size()
    x, y = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    sentry_gun = mobs.SentryGun(world, sentry_gun_surf, Vector2(x, y))
    world.add_entity(sentry_gun)

    for e in world.entities.values():
        print(e)


if __name__ == '__main__':
    main()