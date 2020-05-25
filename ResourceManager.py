import os

import pygame as pygame

class ResourceManager:
    def __init__(self):
        self.root_path = os.getcwd()
        self.images = {}
        self.audio = {}

        self.missing_surface = None

    '''
    Loads image from cache or disk based on filepath and returns image data back
    :param file_path: image file path
    :returns: pygame image
    '''
    def get_image(file_path):
        if file_path in self.images:
            return self.images[file_path]
        else:
            full_path = os.path.join(self.root_path, file_path)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                surface = pg.image.load(file).convert()
                self.images[file_path] = surface
                return surface
            else:
                print('[-] Could not load image: {}'.format(full_path))
                return self.missing_surface

    '''
    Loads audio from cache or disk based on filepath and returns audio data back
    :param file_path: audio file path
    :returns: pygame audio
    '''
    def get_audio(file_path):
        if not pg.mixer:
            return None

        if file_path in self.audio:
            return self.audio[file_path]
        else:
            full_path = os.path.join(self.root_path, file_path)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                sound = pg.mixer.Sound(file)
                self.audio[file_path] = sound
                return sound
            else:
                print('[-] Could not load audio: {}'.format(full_path))
                return None