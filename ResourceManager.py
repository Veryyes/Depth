import os

import pygame as pygame

class ResourceManager:
    def __init__(self, root_path=None):
        if not root_path:
            self.root_path = os.getcwd()
        else:
            self.root_path = root_path
        self.images = {}
        self.audio = {}

        self.missing_surface = None

    '''
    Loads image from cache or disk based on filepath and returns image data back
    :param file_path: image file path
    :returns: pygame image
    '''
    def get_image(self, file_path):
        if file_path.startswith(os.sep):
            file_path = file_path[1:]

        if not file_path.startswith("resources" + os.sep + "images"):
            file_path = os.path.join('resources', 'images', file_path)

        if file_path in self.images:
            return self.images[file_path]
        else:
            full_path = os.path.join(self.root_path, file_path)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                surface = pygame.image.load(full_path).convert()
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
    def get_audio(self, file_path):
        if not pygame.mixer:
            return None

        if file_path.startswith(os.sep):
            file_path = file_path[1:]

        if not file_path.startswith("resources" + os.sep + "audio"):
            file_path = os.path.join('resources', 'audio', file_path)

        if file_path in self.audio:
            return self.audio[file_path]
        else:
            full_path = os.path.join(self.root_path, file_path)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                sound = pygame.mixer.Sound(full_path)
                self.audio[file_path] = sound
                return sound
            else:
                print('[-] Could not load audio: {}'.format(full_path))
                return None