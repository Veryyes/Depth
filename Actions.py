import pygame
import pygame.locals

class Actions:
    @staticmethod
    def on_click(component, game_ctxt):
        return component.is_clicked(game_ctxt)

    @staticmethod
    def on_right_click(component, game_ctxt):
        return component.is_right_clicked(game_ctxt)

    @staticmethod
    def on_left_click(component, game_ctxt):
        return component.is_left_clicked(game_ctxt)

    @staticmethod
    def on_mouse_move(component, game_ctxt):
        return component.mouse_is_moving(game_ctxt)

    @staticmethod
    def on_mouse_exit(component, game_ctxt):
        return component.mouse_exited(game_ctxt)

    @staticmethod
    def on_mouse_enter(component, game_ctxt):
        return component.mouse_entered(game_ctxt)

'''
what the <strong>fuk</strong> is going on here?

To avoid typing out an event function for every key that pygame supports, I dynamically load them into Event
pygame.locals.__dict__ return all the constants pygame has, so I filter out only those with the prefix "K_" which represent each key. 
I create a function for each key and make that function a member of Event

BUT, this creates an issue with symbols that cannot be used in python variables such as all the operators (+=-!|&/%)
These Events currently can only be reached with the getattr python build in function. e.g. getattr(Event, "on_key_+_pressed")

This is probably considered awful, but someone pls make a PR with a better idea
'''
keys = [getattr(pygame.locals,k) for k in pygame.locals.__dict__ if k.startswith('K_')]
for key in keys:
    key_name = pygame.key.name(key)
    setattr(Actions, 
            "on_key_{}_pressed".format(key_name),  
            lambda component, game_ctxt, key=key_name: component.key_pressed(key, game_ctxt))
            
    setattr(Actions,
            "on_key_{}_down".format(key_name),
            lambda component, game_ctxt, key=key_name: component.key_down(key, game_ctxt))

    setattr(Actions,
            "on_key_{}_up".format(key_name),
            lambda component, game_ctxt, key=key_name: component.key_up(key, game_ctxt))
            
