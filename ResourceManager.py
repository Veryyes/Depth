import os

import pygame as pygame

class ResourceManager:
    root_path = os.getcwd()
    images = {}
    audio = {}
    missing_surface = None

    
'''
Loads image from cache or disk based on filepath and returns image data back
:param file_path: image file path
:returns: pygame image
'''
def get_image(file_path):
    if file_path.startswith(os.sep):
        file_path = file_path[1:]

    if not file_path.startswith("resources" + os.sep + "images"):
        file_path = os.path.join('resources', 'images', file_path)

    if file_path in ResourceManager.images:
        return ResourceManager.images[file_path]
    else:
        full_path = os.path.join(ResourceManager.root_path, file_path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            surface = pygame.image.load(full_path).convert_alpha()
            ResourceManager.images[file_path] = surface
            return surface
        else:
            print('[-] Could not load image: {}'.format(full_path))
            return ResourceManager.missing_surface

'''
Loads audio from cache or disk based on filepath and returns audio data back.
This is for loading Sound FFX, not music to stream
:param file_path: audio file path
:returns: pygame audio
'''
def get_audio(file_path):
    if not pygame.mixer:
        return None

    if file_path.startswith(os.sep):
        file_path = file_path[1:]

    if not file_path.startswith("resources" + os.sep + "audio"):
        file_path = os.path.join('resources', 'audio', file_path)

    if file_path in ResourceManager.audio:
        return ResourceManager.audio[file_path]
    else:
        full_path = os.path.join(ResourceManager.root_path, file_path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            sound = pygame.mixer.Sound(full_path)
            ResourceManager.audio[file_path] = sound
            return sound
        else:
            print('[-] Could not load audio: {}'.format(full_path))
            return None

def get_music_path(filename):
    path = os.path.join(ResourceManager.root_path, "library", filename)
    if os.path.exists:
        return path
    else:
        print("Does not exists")
        return None