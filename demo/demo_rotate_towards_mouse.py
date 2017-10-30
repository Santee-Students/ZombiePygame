import pygame
from manager import ImageManager
from game import *
from pygame.locals import *
from pygame.math import Vector2

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    image_manager = ImageManager('../data/images')

    sprite_image = image_manager['sentrygun.png']
    sprite_location = Vector2(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0)
    circles = []
    print(sprite_location)

    time_passed = 0
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))

        mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()
        mouse_location = Vector2(mouse_pos)
        vec_diff = mouse_location - sprite_location
        angle = -math.atan2(vec_diff.y, vec_diff.x) # atan2's result is inverted controls, so * -1
        #print(angle)
        rotated_image = pygame.transform.rotate(sprite_image, math.degrees(angle))
        rotated_x = (SCREEN_WIDTH - rotated_image.get_width()) / 2.0
        rotated_y = (SCREEN_HEIGHT - rotated_image.get_height()) / 2.0

        # Draw center cross-hair lines:
        pygame.draw.line(screen, (255, 0, 0), (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))
        pygame.draw.line(screen, (255, 0, 0), (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

        if pygame.mouse.get_pressed()[0]:
            circles += [mouse_pos]

        for circle_pos in circles:
            pygame.draw.circle(screen, (0, 255, 0), circle_pos, 5)

        screen.blit(sprite_image, mouse_pos)
        screen.blit(rotated_image, (rotated_x, rotated_y))
        # Why is it the angle offset!?

        #pygame.display.update(pygame.Rect(rotated_x, rotated_y, rotated_image.get_width(), rotated_image.get_height()))
        pygame.display.update()
        time_passed = clock.tick(FPS)


if __name__ == '__main__':
    main()