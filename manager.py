import os
import pygame

from errors import *


class ImageManager:
    """The thing that manages images"""

    def __init__(self, dir='.'):
        self.image_directory = os.path.abspath(dir)
        self.surf_dict = {}

        if pygame.display.get_surface() is None:
            raise ScreenNotInitialized('ImageManager instances require a screen to be already initialised!')

    def __getitem__(self, item):
        """Load the image even though it has not bee loaded before"""

        surface = None
        try:
            surface = self.surf_dict[item]
        except KeyError:
            # Image has not been loaded before
            if not isinstance(item, str):
                raise TypeError('argument item ({}) must be str!'.format(type(item)))

            image_path = self.__get_image_path(item)
            if not os.path.exists(image_path):
                raise FileNotFoundError('Path: {}'.format(image_path))

            # Load the image and store into dictionary
            surface = pygame.image.load(image_path).convert_alpha()
            self.surf_dict[item] = surface

        return surface

    def __get_image_path(self, image_name):
        return os.path.join(self.image_directory, image_name)

    def __setitem__(self, image_name, surface):
        """Manually name an image surface (key-value pair)"""
        if not isinstance(surface, pygame.Surface):
            raise TypeError('surface argument ({}) must be a pygame.Surface type!'.format(surface))

        self.surf_dict[image_name] = surface
        return surface


