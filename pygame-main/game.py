import pygame
from menu import *

# reference: https://github.com/ChristianD37/YoutubeTutorials/blob/master/Menu%20System/game.py for game loop creation
class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP, self.DOWN, self.START_KEY, self.BACK = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = '8 Bit.TTF'
        self.credit_font = 'Franchise.TTF'
        #self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.controls = ControlsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

# create game loop for start and end
    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False
            self.display.fill(self.BLACK)
            self.draw_text('Game over', 50, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()
            
# check player input
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK = True
                if event.key == pygame.K_DOWN:
                    self.DOWN = True
                if event.key == pygame.K_UP:
                    self.UP = True

    def reset_keys(self):
        self.UP, self.DOWN, self.START_KEY, self.BACK = False, False, False, False
# create text
    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
        
# custom font for text in the credits
    def draw_crText(self, text, size, x, y ):
        creditfont = pygame.font.Font(self.credit_font,size)
        credittext = creditfont.render(text, True, self.WHITE)
        creditrect = credittext.get_rect()
        creditrect.center = (x,y)
        self.display.blit(credittext,creditrect)