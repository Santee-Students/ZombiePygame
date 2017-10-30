from manager import ImageManager
import sys
import os
import pygame
import time

# Add 1-dir-up to path (contains manager.py, and errors.py)
# sys.path += [os.path.join(os.getcwd(), '..')]
'''No need to do; just change the working directory of the file @ Run->Edit Configurations...
Don't forget to change relative paths of instances (eg. ImageManager('../data/images/')
to ImageManager('data/images/')'''


def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = (640, 480)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('[Demo] ImageManager image loading')
    imagedude = ImageManager('data/images')

    imagedude['backgroundB.jpg'] = pygame.transform.scale(imagedude['backgroundB.jpg'], SCREEN_SIZE)
    screen.blit(imagedude['backgroundB.jpg'], (0, 0))
    pygame.display.update()
    time.sleep(2)

    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    main()