import uuid
import math

import pygame as pg

from Actions import Actions

class Component:
    TOP = 0
    CENTER = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4

    '''
    Creates a new component
    :param x: the x coordinate relative to the parent
    :param y: the y coordinate relative to the parent
    :param w: the width
    :param h: the height
    '''
    def __init__(self, x=0,y=0,w=0,h=0, parent=None):
        self.uuid = uuid.uuid4()

        self.parent = parent
        if self.parent:
            self.rect = pg.Rect(x+self.parent.rect.x,y+self.parent.rect.y,w,h)
            self.parent.add_child(self)
        else:
            self.rect = pg.Rect(x,y,w,h)
            
        self.visible = True
        self.enabled = True

        self.text = ""
        self.text_font = self.parent.text_font if self.parent else ""
        self.text_align = (Component.CENTER, Component.CENTER)
        self.font_name = self.parent.font_name if self.parent else ""
        self.font_size = self.parent.font_size if self.parent else 48
        self.text_color = (0,0,0)

        self.image = None
        self.background = False
        self.background_color = self.parent.background_color if self.parent else (0, 0, 0)

        self.draw_outline = False
        self.outline_color = 0x0
        self.outline_thiccness = 2

        self.children = []

        # Mapping (funcA -> funcB) where if funcA is true, then call funcB
        self.registered_events = {}

    def get_diagonal(self):
        return math.sqrt(self.rect.w**2 + self.rect.h**2)

    '''
    Resize with width of the component relative to the parents or a components width
    '''
    def resize_width_ratio(self, ratio, component=None):
        if not component:
            self.rect.w = self.parent.rect.w * ratio
        else:
            self.rect.w = component.rect.w * ratio

    '''
    Resize with height of the component relative to the parents or a components height
    '''
    def resize_height_ratio(self, ratio, component=None):
        if not component:
            self.rect.h = self.parent.rect.h * ratio
        else:
            self.rect.h = component.rect.h * ratio

    '''
    Resize component based on larges child
    '''
    def resize_on_children(self):
        self.resize_width_on_children()
        self.resize_height_on_children()

    '''
    Resize width of component based on largest child
    '''
    def resize_width_on_children(self):
        if len(self.children) == 0:
            return
        max_w = max([child.rect.w for child in self.children])
        self.rect.w = max_w

    '''
    Resize height of component based on largest child
    '''
    def resize_height_on_children(self):
        if len(self.children) == 0:
            return
        max_h = max([child.rect.h for child in self.children])
        self.rect.h = max_h

    '''
    Centers this component to ratio * parent's width relative to the parents x position
    :param ratio: the percentage of the parent's width the component should be centered to
    '''
    def center_x_ratio(self, ratio, component=None):
        if not component:
            component = self.parent
        
        self.rect.x = component.rect.x + (component.rect.w*ratio) - (self.rect.w / 2)

    def left_align_ratio(self, ratio, component=None):
        if not component:
            component = self.parent

        self.rect.x = component.rect.x + component.rect.w*ratio

    def right_align_ratio(self, ratio, component=None):
        if not component:
            component = self.parent

        self.rect.x = component.rect.x + component.rect.w*ratio - self.rect.w

    '''
    Centers this component to ratio * parent's height relative to the parents y position
    :param ratio: the percentage of the parent's height the component should be centered to
    '''
    def center_y_ratio(self, ratio, component=None):
        if not component:
            component = self.parent
        
        self.rect.y = component.rect.y + (component.rect.h*ratio) - (self.rect.h / 2)

    def top_align_ratio(self, ratio, component=None):
        if not component:
            component = self.parent

        self.rect.y = component.rect.y + component.rect.h*ratio

    def bottom_align_ratio(self, ratio, component=None):
        if not component:
            component = self.parent

        self.rect.y = component.rect.y + component.rect.h*ratio - self.rect.h

    '''
    Flushes component to the left side of the parent, or to the other component specified
    :param component: (Optional) Component to do operation relative to
    '''
    def flush_left(self, component=None):
        if not component:
            self.rect.x = self.parent.rect.x
        else:
            self.rect.x = component.rect.x

    '''
    Flushes component to the right side of the parent, or to the other component specified
    :param component: (Optional) Component to do operation relative to
    '''
    def flush_right(self, component=None):
        if not component:
            self.rect.x = self.parent.rect.x + self.parent.rect.w - self.rect.w 
        else:
            self.rect.x = component.rect.x + component.rect.w - self.rect.w 
    
    '''
    Flushes component to the top side of the parent, or to the other component specified
    :param component: (Optional) Component to do operation relative to
    '''
    def flush_top(self, component=None):
        if not component:
            self.rect.y = self.parent.rect.y
        else:
            self.rect.y = component.rect.y

    
    '''
    Flushes component to the bottom side of the parent, or to the other component specified
    :param component: (Optional) Component to do operation relative to
    '''
    def flush_bottom(self, component=None):
        if not component:
            self.rect.y = self.parent.rect.y + self.parent.rect.h - self.rect.h
        else:
            self.rect.y = component.rect.y + component.rect.h - self.rect.h
    
    '''
    Get the relative x position based on a ratio of the width of this component
    '''
    def get_width_ratio(self, ratio):
        return (self.rect.w * ratio) + self.rect.x

    '''
    Get the relative y position based on a ratio of the height of this component
    '''
    def get_height_ratio(self, ratio):
        return (self.rect.h * ratio) + self.rect.y

    def update(self, game_ctxt):
        if not self.enabled:
            return

        for reg_events in self.registered_events:
            # reg_event is the key and also a function that evauluates true if the event should be fired
            if reg_events(self, game_ctxt):
                for event in self.registered_events[reg_events]:
                    member_func, callback = event
                    if member_func:
                        callback(game_ctxt)
                    else:
                        callback(self, game_ctxt)

        for child in self.children:
            child.update(game_ctxt)

    def render(self, game_ctxt):
        if not self.visible:
            return

        # If a solid background color has been specified, render it
        if self.background:
            background = pg.Surface((self.rect.w, self.rect.h))
            background.fill(self.background_color)
            game_ctxt.screen.blit(background, (self.rect.x, self.rect.y))

        # If an image has been given, render it
        if self.image:
            game_ctxt.screen.blit(self.image, (self.rect.x, self.rect.y))
        
        # If theres text, render it
        if len(self.text) > 0:
            if self.text_align[0] == Component.LEFT:
                text_x = self.rect.x
            elif self.text_align[0] == Component.CENTER:
                text_x = self.get_width_ratio(.5) - (self.text_w/2)
            elif self.text_align[0] == Component.RIGHT:
                text_x = self.get_width_ratio(1) - self.text_w
            else:
                text_x = self.get_width_ratio(.5) - (self.text_w/2)

            if self.text_align[1] == Component.TOP:
                text_y = self.rect.y
            elif self.text_align[1] == Component.CENTER:
                text_y = self.get_height_ratio(.5) - (self.text_h/2)
            elif self.text_align[1] == Component.BOTTOM:
                text_y = self.get_height_ratio(1) - self.text_h
            else:
                text_y = self.get_height_ratio(.5) - (self.text_h/2)

            text_pos = (text_x, text_y)
            
            game_ctxt.screen.blit(self.text_img, text_pos)

        # If you wanna draw the outline, draw it
        if self.draw_outline:
            outline_rect = pg.Rect(self.rect.x-1, self.rect.y-1, self.rect.w+2, self.rect.h+2)
            pg.draw.rect(game_ctxt.screen, self.outline_color, outline_rect, self.outline_thiccness)

        for child in self.children:
            child.render(game_ctxt)        

    def strech_image(self, dims=None):
        image_copy = self.image.copy()
        if dims:
            target_w, target_h = dims
        else:
            target_w, target_h = self.rect.size
    
        self.image = pg.transform.scale(image_copy, (target_w, target_h))

    def fit_image(self, dims=None):
        image_copy = self.image.copy()
        img_w, img_h = image_copy.get_size()

        img_rect = pg.Rect(0,0, img_w, img_h)

        if dims:
            target_w, target_h = dims
        else:
            target_w, target_h = self.rect.size

        target_rect = pg.Rect(0,0,target_w, target_h)

        self.image = pg.transform.scale(image_copy, (img_rect.fit(target_rect).size))
        
    def tile_image(self):
        pass

    '''
    Sets the background color of the component to a solid color
    :param color: pygame color
    '''
    def set_background_color(self, color):
        self.background = True
        self.background_color = color

    '''
    Disables all children.
    :param recursive: (Optional) apply to all descendants
    '''
    def disable_children(self, recursive=False): # LOL
        for child in self.children:
            child.enabled = False
            if recursive:
                child.disable_children(recursive=recursive)

    '''
    Sets all children to be not visible.
    :param recursive: (Optional) apply to all descendants
    '''
    def hide_children(self, recursive=False): #Hide yo kids
        for child in self.children:
            child.visible = False
            if recursive:
                child.hide_children(recursive=recursive)

    
    '''
    Enables all children
    :param recursive: (Optional) apply to all descendants
    '''
    def enable_children(self, recursive=False):
        for child in self.children:
            child.enabled = True
            if recursive:
                child.enable_children(recursive=recursive)

    '''
    Shows all children
    :param recursive: (Optional) apply to all descendants
    '''
    def show_children(self, recursive=False):
        for child in self.children:
            child.visible = True
            if recursive:
                child.show_children(recursive=recursive)

    '''
    Shows and Enables all children
    :param recursive: (Optional) apply to all descendants
    '''
    def enable_and_show_children(self, recursive=False):
        self.enable_children(recursive=recursive)
        self.show_children(recursive=recursive)

    '''
    Hide and disable all children
    :param recursive: (Optional) apply to all descendants
    '''
    def disable_and_hide_children(self, recursive=False):
        self.disable_children(recursive=recursive)
        self.hide_children(recursive=recursive)

    '''
    Set the font style and size
    :param font_name: name of the font style (a system default one will be picked if no match)
    :param size: (Optional) The size of the font
    '''
    def set_font(self, font_name, size=48):
        if type(size) == float:
            size = int(size)

        self.text_font = pg.font.SysFont(font_name, size)
        self.font_name = font_name
        self.font_size = size

    '''
    Returns the font size. Only mutate self.font_size via self.set_font
    :returns: font size
    '''
    def get_font_size(self):
        return self.font_size

    '''
    Returns the font style. Only mutate self.font_style via self.set_font
    :returns: font style
    '''
    def get_font_name(self):
        return self.font_name

    '''
    Set the text to render in the center of the component. Rebuilds rendered text image
    :param text: The text to render
    :param allow_resize: (Optional) If true, increase the component's dimensions to fit the text
    :param color: (Optional) the color to set the text to
    '''
    def set_text(self, text, allow_resize=False, color=None):
        if not text:
            self.text = ""
        else:
            self.text = text

        if color:
            self.text_color = color

        self.text_img = self.text_font.render(self.text, True, self.text_color)
        self.text_w, self.text_h = self.text_font.size(self.text)
        if allow_resize:
            if self.text_w > self.rect.w:
                self.rect.w = self.text_w
            if self.text_h > self.rect.h:
                self.rect.h = self.text_h


    '''
    Sets the text color
    :param color: The color to set the text to
    '''
    def set_text_color(self, color):
        self.set_text(self.text, color=color)

    '''
    Returns the X coordinate of the right edge
    :returns: X coordinate of right edge
    '''
    def get_right_edge(self):
        return self.rect.x + self.rect.w

    '''
    Returns the Y coordinate of the bottom edge
    :returns: Y coordinate of bottom edge
    '''
    def get_bottom_edge(self):
        return self.rect.y + self.rect.h

    def highlight_on_hover(self, factor=1.25):
        self.register_event(
            Actions.on_mouse_enter,
            lambda c, gctxt: c.set_background_color(tuple(map(lambda color: min(int(color*factor), 255) , c.parent.background_color)))
        )
        self.register_event(
            Actions.on_mouse_exit,
            lambda c, gctxt: c.set_background_color(c.parent.background_color)
        )

    '''
    Adds a child component
    :param child_component: The child component to add
    '''
    def add_child(self, child_component):
        if not child_component in self.children:
            self.children.append(child_component)
        child_component.parent = self

    '''
    BFS-style apply a function to each child.
    :param recursive: if True, apply function to children recursively
    :param func: function to apply on children
    :param kwargs: kwgars to func
    '''
    def apply_to_children(self, recursive, func, **kwarg):
        for child in self.children:
            func(child, kwarg)

        if recursive:
            for child in self.children:
                child.apply_to_children(func, recursive, kwarg)

    '''
    Registers callbacks based on an event

    The callback function will be run with self and game_ctxt as the parameters
    Thus, the callback function given should only take two parameters, Although member functions of a class insert a reference
    to themselves as the first parameter.
                
    :param event: Function that if it evaluates to true, then callback will be called like so: event(self, game_ctxt). see Actions class
    :param callback: The callback function to associate with the given event. Is called like so: callback(self, game_ctxt)
    :param member_func: (Optional) Set to True if the callback is a member_function. If True, the callback function will be called like so instead: callback(game_ctxt)
    :returns: True if successful
    '''
    def register_event(self, event, callback, member_func=False):
        if not callable(event):
            print('[-] Event is not a function. Must be a function that evalutes to a boolean value')
            return False

        if not callable(callback):
            print('[-] Callback registered for {} is not callable'.format(event))
            return False

        if not self.registered_events.get(event, None):
            self.registered_events[event] = [(member_func, callback)]
        else:
            self.registered_events[event].append((member_func, callback))

        return True
    
    '''
    Evalutes whether or not the mouse is clicked inside the component
    :returns: True if the left or right mouse button has been clicked inside the component
    '''
    def is_clicked(self, game_ctxt):
        return self.is_left_clicked(game_ctxt) or self.is_right_clicked(game_ctxt)

    def clicked_outside(self, game_ctxt):
        if not self.rect.collidepoint(pg.mouse.get_pos()):
            for event in game_ctxt.events:
                if event.type == pg.MOUSEBUTTONDOWN and (event.button == 3 or event.button == 1):
                    return True
        return False

    '''
    Evalutes whether or not the mouse button has been released inside the component
    :returns: True if the left or right mouse button has been released inside the component
    '''
    def is_mouse_released(self, game_ctxt):
        return self.is_left_released(game_ctxt) or self.is_right_released(game_ctxt)

    '''
    Evalutes whether or not the mouse is held down inside the component
    :returns: True if the left or right mouse button is being held down inside the component
    '''
    def is_mouse_pressed(self, game_ctxt):
        return self.is_left_pressed(game_ctxt) or self.is_right_pressed(game_ctxt)

    '''
    Evalutes whether or not the right mouse button is clicked inside the component
    :returns: True if the right mouse button has been clicked inside the component
    '''
    def is_right_clicked(self, game_ctxt):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            for event in game_ctxt.events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                    return True
        return False

    '''
    Evalutes whether or not the right mouse button has been released inside the component
    :returns: True if the right mouse button has been released inside the component
    '''
    def is_right_released(self, game_ctxt):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            for event in game_ctxt.events:
                if event.type == pg.MOUSEBUTTONUP and event.button == 3:
                    return True
        return False

    '''
    Evalutes whether or not the right mouse button has been released inside the component
    :returns: True if the right mouse button has been released inside the component
    '''
    def is_right_pressed(self, game_ctxt):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            click = pg.mouse.get_pressed()[2] == 1
            inside = self.rect.collidepoint(pg.mouse.get_pos())
            return click and inside
        return False

    '''
    Evalutes whether or not the left mouse button is clicked inside the component
    :returns: True if the left mouse button has been clicked inside the component
    '''
    def is_left_clicked(self, game_ctxt):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            for event in game_ctxt.events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    return True
        return False

    '''
    Evalutes whether or not the left mouse button has been released inside the component
    :returns: True if the left mouse button has been released inside the component
    '''
    def is_left_released(self, game_ctxt):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            for event in game_ctxt.events:
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    return True
        return False

    '''
    Evalutes whether or not the left mouse button has been released inside the component
    :returns: True if the left mouse button has been released inside the component
    '''
    def is_left_pressed(self, game_ctxt):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            click =  pg.mouse.get_pressed()[0] == 1
            inside = self.rect.collidepoint(pg.mouse.get_pos())
            return click and inside
        return False

    def is_scrolling_up(self, game_ctxt):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            for event in game_ctxt.events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 4:
                    return True
        return False


    def is_scrolling_down(self, game_ctxt):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            for event in game_ctxt.events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 5:
                    return True
        return False

    '''
    Evalutes whether or not the mouse is moving inside the component
    :returns: True if the mouse is moving inside the component
    '''
    def mouse_is_moving(self, game_ctxt):
        inside = self.rect.collidepoint(pg.mouse.get_pos())
        x_vel, y_vel = game_ctxt.mouse_rel
        moved = x_vel != 0 and y_vel != 0
        return inside and moved

    '''
    Evalutes whether or not the mouse has just left the component
    :returns: True if the mouse has just left the component
    '''
    def mouse_exited(self, game_ctxt):
        x, y = pg.mouse.get_pos()
        x_vel, y_vel = game_ctxt.mouse_rel
        inside_before = self.rect.collidepoint(x-x_vel,y-y_vel) == 1
        outside_after = not self.rect.collidepoint(x,y)
        return inside_before and outside_after

    '''
    Evalutes whether or not the mouse has just entered the component
    :returns: True if the mouse has just entered the component
    '''
    def mouse_entered(self, game_ctxt):
        x, y = pg.mouse.get_pos()
        x_vel, y_vel = game_ctxt.mouse_rel

        outside_before = not self.rect.collidepoint(x-x_vel, y-y_vel)
        inside_after = self.rect.collidepoint(x,y) == 1
        return outside_before and inside_after

    def mouse_exited_family(self, game_ctxt):
        x, y = pg.mouse.get_pos()
        x_vel, y_vel = game_ctxt.mouse_rel

        prev_x = x-x_vel
        prev_y = y-y_vel

        family = [child for child in self.children]
        family.append(self)

        one_inside_before = any([member.rect.collidepoint(prev_x, prev_y)==1 for member in family])
        all_outside_after = all([not member.rect.collidepoint(x, y) for member in family])

        return one_inside_before and all_outside_after

    def mouse_entered_family(self, game_ctxt):
        x, y = pg.mouse.get_pos()
        x_vel, y_vel = game_ctxt.mouse_rel

        prev_x = x-x_vel
        prev_y = y-y_vel

        family = [child for child in self.children]
        family.append(self)

        all_outside_before = all([not member.rect.collidepoint(prev_x, prev_y) for member in family])
        one_inside_after = any([member.rect.collidepoint(x, y)==1 for member in family])

        return all_outside_before and one_inside_after

    '''
    Evalutes whether or not keyboard button key is pressed
    :param key: a string representing the keyboard button
    :returns: True if key is pressed
    '''
    def key_pressed(self, key, game_ctxt):
        keystate = pg.key.get_pressed()
        return keystate[pg.key.key_code(key)] == 1
        
    '''
    Evalutes whether or not keyboard button key has been pushed down
    :param key: a string representing the keyboard button
    :returns: True if key was pressed
    '''
    def key_down(self, key, game_ctxt):
        for event in game_ctxt.events:
            if event.type == pg.KEYDOWN and event.key == ord(key):
                return True

    '''
    Evalutes whether or not keyboard button key is released
    :param key: a string representing the keyboard button
    :returns: True if key was released
    '''
    def key_up(self, key, game_ctxt):
        for event in game_ctxt.events:
            if event.type == pg.KEYUP and event.key == ord(key):
                return True