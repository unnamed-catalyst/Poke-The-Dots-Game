# Poke The Dots
# This is a graphical game where two dots move around
# the screen, bouncing off the edges. The user tries 
# to prevent the dots from colliding by pressing and 
# releasing the mouse button to teleport the dots to 
# a random location. The score is the number of seconds 
# from the start of the game.

from uagame import Window
from random import randint
from pygame import QUIT, Color, MOUSEBUTTONUP
from pygame.time import Clock, get_ticks
from pygame.event import get as get_events
from pygame.draw import circle as draw_circle
from math import sqrt

# User-defined functions

def main():
    game = Game()
    game.play_game() 
           
class Game:
    # An object in this class represents a complete game.
    # - window
    # - frame_rate
    # - close_selected
    # - clock
    # - small_dot
    # - big_dot
    # - score
    
    def __init__(self):
        self._window = Window('Poke the Dots', 500, 400)
        self._adjust_window()
        self._frame_rate = 90
        self._close_selected = False
        self._clock = Clock()
        self._small_dot = Dot('red', [50,75], 30, [1,2], self._window)
        self._big_dot = Dot('blue', [200,100], 40, [2,1], self._window)
        self._small_dot.randomize_dot()
        self._big_dot.randomize_dot()
        self._score = 0
        self._continue_game = True
        
    def _adjust_window(self):
        self._window.set_font_name('ariel')
        self._window.set_font_size(64)
        self._window.set_font_color('white')
        self._window.set_bg_color('black')
        
    def play_game(self):
        # Play the game until the player presses the close icon.
        # - game is the Game to play

        while not self._close_selected:
            self.handle_events()
            self.draw_game() 
            self.update_game()
        self._window.close()
    
    def handle_events(self):
        # Handle the current game events by changing the game
        # state appropriately.
        # - game is the Game whose events will be handled
        
        event_list = get_events()
        for event in event_list:
            self.handle_one_event(event)
    
    def handle_one_event(self, event):
        # Handle one event by changing the game state
        # appropriately.
        # - self is the Game whose event will be handled
        # - event is the Event object to handle

        if event.type == QUIT:
            self._close_selected = True
        elif self._continue_game and event.type == MOUSEBUTTONUP:
            self.handle_mouse_up()
    
    def handle_mouse_up(self):
        # Respond to the player releasing the mouse button by
        # taking appropriate actions.
        # - game is the Game where the mouse up occured
        # - event is the Event object to handle

        self._small_dot.randomize_dot()
        self._big_dot.randomize_dot()
    
    def draw_game(self):
        # Draw all game objects.
        # - game is the Game to draw for
    
        self._window.clear()
        self.draw_score()
        self._small_dot.draw_dot()
        self._big_dot.draw_dot()
        if not self._continue_game:
            self.draw_game_over()
        self._window.update()
    
    def draw_game_over(self):
        string = 'GAME OVER'
        font_color = self._small_dot.get_color()
        bg_color = self._big_dot.get_color()
        original_font_color = self._window.get_font_color()
        original_bg_color = self._window.get_bg_color()
        self._window.set_font_color(font_color)
        self._window.set_bg_color(bg_color)
        height = self._window.get_height() - self._window.get_font_height()
        self._window.draw_string(string, 0, height)
        self._window.set_font_color(original_font_color)
        self._window.set_bg_color(original_bg_color)
        
    def draw_score(self):
        # Draw the time since the game began as a score.
        # - game is the Game to draw for
    
        string = 'Score: ' + str(self._score)
        self._window.draw_string(string, 0, 0)

    def update_game(self):
        # Update all game objects with state changes
        # that are not due to user events.
        # - game is the Game to update
    
        if self._continue_game:
            self._small_dot.move_dot()
            self._big_dot.move_dot()
            self._score = get_ticks() // 1000
        self._clock.tick(self._frame_rate)
        if self._small_dot.intersects(self._big_dot):
            self._continue_game = False

class Dot:
    # An object in this class represents a colored circle
    # that can move.
    # - color
    # - center
    # - radius
    # - velocity
    # - window
    
    def __init__(self, color, center, radius, velocity, window):
        self._color = color
        self._center = center
        self._radius = radius
        self._velocity = velocity
        self._window = window
        
    def randomize_dot(self):
        # Change the dot so that its center is at a random
        # point on the surface. Ensure that no part of a dot
        # extends beyond the surface boundary.
        # - dot is the Dot to randomize
        
        size = (self._window.get_width(), self._window.get_height())
        for index in range(0, 2):
            self._center[index] = randint(self._radius, size[index] - self._radius)    
    
    def draw_dot(self):
        # Draw the dot on the window.
        # - dot is the Dot to draw

        surface = self._window.get_surface()
        color = Color(self._color)
        draw_circle(surface, color, self._center, self._radius)
    
    def move_dot(self):
        # Change the location and the velocity of the Dot so it
        # remains on the surface by bouncing from its edges.
        # - dot is the Dot to move
    
        size = (self._window.get_width(), self._window.get_height())
        for index in range(0, 2):
            self._center[index] = self._center[index] + self._velocity[index]
            if (self._center[index] < self._radius) or (self._center[index] + self._radius > size[index]):
                self._velocity[index] = - self._velocity[index]    
    
    def get_radius(self):
        return self._radius
    
    def get_center(self):
        return self._center
    
    def get_color(self):
        return self._color
    
    def intersects(self, dot):
        # Return True if the two dots intersect and False if
        # they do not.
        # - self is a Dot
        # - dot is the other Dot
    
        distance = sqrt((self._center[0] - dot._center[0])**2 + (self._center[1] - dot._center[1])**2)
        return distance <= self._radius + dot._radius    
        
main()