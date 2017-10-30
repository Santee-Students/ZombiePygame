import unittest
from manager import ImageManager
import pygame
import os
from errors import *

class ImageManagerTestCaseA(unittest.TestCase):

    def test_try_making_imagemanager(self):
        """ImageManager should raise an error if the screen surface has not been initialised yet"""

        with self.assertRaises(ScreenNotInitialized):
            imagemanager = ImageManager()

class ImageManagerTestCaseB(unittest.TestCase):

    def setUp(self):
        # Initialise required stuff
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))

        self.path = 'data/images/'
        self.imagedude = ImageManager(self.path)   # Load images from data/images/

        self.bg = pygame.image.load(os.path.join(self.path, 'backgroundA.jpg')).convert()   # Load image
        self.bg_width, self.bg_height = self.bg.get_size()
        self.imagedude['backgroundB.jpg'] = self.bg # Add image

    def test_try_making_imagemanager(self):
        """ImageManager should raise an error if the screen surface has not been initialised yet"""
        pygame.quit()
        pygame.init()
        with self.assertRaises(ScreenNotInitialized):
            imagemanager = ImageManager()

    def test_add_image_invalid_value(self):
        with self.assertRaises(TypeError):
            self.imagedude['abc'] = '123'
            self.imagedude['edf'] = 123

    def test_add_images(self):
        # Add image
        image_name = 'bg'
        self.imagedude[image_name] = self.bg
        self.assertEqual(self.imagedude[image_name], self.bg)

    def test_get_image(self):
        bg = self.imagedude['backgroundB.jpg']
        self.assertEqual(bg, self.bg)

    @unittest.skip
    def test_get_image_invalid_type(self):
        with self.assertRaises(TypeError):
            surf = self.imagedude[123123]

    def test_get_image_not_found(self):
        with self.assertRaises(FileNotFoundError):
            surf = self.imagedude['filenotfoundimage.png']


    def test_automatic_load_image(self):
        """Load an image that has not been loaded before"""

        # Make sure that the requested surface is not none
        background = self.imagedude['backgroundA.jpg']
        self.assertIsNotNone(background)

        # Test that the image was actually stored into the dictionary
        self.assertEqual(background, self.imagedude['backgroundA.jpg'])

        # Compare the dimensions of the loaded images
        bgB = pygame.image.load(os.path.join(self.path, 'backgroundA.jpg')).convert()
        background_size = background.get_size()
        bgB_size = bgB.get_size()

        self.assertEqual(background_size, bgB_size)

        # Test loading image that doesn't exist.
        with self.assertRaises(FileNotFoundError):
            image = self.imagedude['asdflkjoiuqeioqwe.jog']

        # Make sure that loading images with invalid image filename types is illegal
        with self.assertRaises(TypeError):
            invalid = self.imagedude[123456]
            invalid = self.imagedude[123456.3]

    def test_transparent_image(self):
        # Test loading an image with alpha
        transparent_image = self.imagedude['transparent.png']
        pixel = transparent_image.get_at((10, 10))
        self.assertNotEqual(pixel, (0, 0, 0))
        self.assertNotEqual(pixel, (255, 255, 255))
        self.assertEqual(transparent_image.get_at((70, 70)), (0, 0, 0)) # BLACK
        self.assertEqual(transparent_image.get_at((35, 70)), (149, 0, 186))  # Arbitrary purple

    def test_pre_cache_all(self):
        pass

    def test_directory(self):
        imagedude_path = self.imagedude.image_directory
        #print(imagedude_path)
        self.assertEqual(imagedude_path, os.path.abspath(self.path))

        all_filesA = tuple((entry.name for entry in os.scandir(imagedude_path)))
        all_filesB = tuple((entry.name for entry in os.scandir(self.path)))
        self.assertTupleEqual(all_filesA, all_filesB)


if __name__ == '__main__':
    unittest.main()