import pygame as pg

class Component:
    
    '''
    Creates a new component
    :param x: the x coordinate relative to the parent
    :param y: the y coordinate relative to the parent
    :param w: the width
    :param h: the height
    '''
    def __init__(self, x,y,w,h, parent=None):

        self.parent = parent
        if self.parent:
            self.rect = pg.Rect(x+self.parent.rect.x,y+self.parent.rect.y,w,h)
            self.parent.add_child(self)
        else:
            self.rect = pg.Rect(x,y,w,h)
            
        self.visible = True
        self.enabled = True

        self.text = ""
        self.text_font = None
        self.font_name = ""
        self.font_size = 48

        self.image = None
        self.draw_outline = False
        self.text_color = 0x0

        self.children = []

        # Mapping (funcA -> funcB) where if funcA is true, then call funcB
        self.registered_events = {}

    '''
    Resize with width of the component relative to the parents width
    '''
    def resize_width_ratio(self, ratio):
        self.rect.w = self.parent.rect.w * ratio

    '''
    Resize with height of the component relative to the parents height
    '''
    def resize_height_ratio(self, ratio):
        self.rect.h = self.parent.rect.h * ratio

    '''
    Centers this component to ratio * parent's width relative to the parents x position
    :param ratio: the percentage of the parent's width the component should be centered to
    '''
    def center_x_ratio(self, ratio):
        self.rect.x = self.parent.rect.x + (self.parent.rect.w*ratio) - (self.rect.w / 2)
                
    '''
    Centers this component to ratio * parent's height relative to the parents y position
    :param ratio: the percentage of the parent's height the component should be centered to
    '''
    def center_y_ratio(self, ratio):
        self.rect.y = self.parent.rect.y + (self.parent.rect.h*ratio) - (self.rect.h / 2)

    '''
    Flushes component to the left side of the parent
    '''
    def flush_left(self):
        self.rect.x = self.parent.rect.x

    '''
    Flushes component to the right side of the parent
    '''
    def flush_right(self):
        self.rect.x = self.parent.rect.x + self.parent.rect.w - self.rect.w 
    
    '''
    Flushes component to the top side of the parent
    '''
    def flush_top(self):
        self.rect.y = self.parent.rect.y
    
    '''
    Flushes component to the bottom side of the parent
    '''
    def flush_bottom(self):
        self.rect.y = self.parent.rect.y + self.parent.rect.h - self.rect.h
    
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
                member_func, callback = self.registered_events[reg_events]
                if member_func:
                    callback(game_ctxt)
                else:
                    callback(self, game_ctxt)

        for child in self.children:
            child.update(game_ctxt)

    def render(self, game_ctxt):
        if not self.visible:
            return

        if self.image:
            game_ctxt.screen.blit(self.image, (self.rect.x, self.rect.y))
        
        if len(self.text) > 0:
            text_pos = (self.get_width_ratio(.5) - (self.text_w/2), self.get_height_ratio(.5) - (self.text_h/2))
            game_ctxt.screen.blit(self.text_img, text_pos)

        if self.draw_outline:
            pg.draw.rect(game_ctxt.screen, 0x0, self.rect, 2)

        for child in self.children:
            child.render(game_ctxt)

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
    '''
    def set_text(self, text, allow_resize=False):
        self.text = text
        self.text_img = self.text_font.render(self.text, True, self.text_color)
        self.text_w, self.text_h = self.text_font.size(self.text)
        if allow_resize:
            if self.text_w > self.rect.w:
                self.rect.w = self.text_w
            if self.text_h > self.rect.h:
                self.rect.h = self.text_h

    '''
    Adds a child component
    :param child_component: The child component to add
    '''
    def add_child(self, child_component):
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
    
        self.registered_events[event] = (member_func, callback)
        return True
    
    '''
    Evalutes whether or not the mouse is clicked inside the component
    :returns: True if the left or right mouse button has been clicked inside the component
    '''
    def is_clicked(self, game_ctxt):
        return self.is_left_clicked(game_ctxt) or self.is_right_clicked(game_ctxt)

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