import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.click_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 200

    def draw_click(self):
        self.game.draw_text('o', 15, self.click_rect.x, self.click_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
# reference: https://github.com/ChristianD37/YoutubeTutorials/blob/master/Menu%20System/main.py for menu class creation
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 0
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 100
        self.click_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Forest Chase', 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 250)
            self.game.draw_text('Main Menu', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 150)
            self.game.draw_text("Start Game", 40, self.startx, self.starty)
            self.game.draw_text("Controls", 40, self.controlsx, self.controlsy)
            self.game.draw_text("Credits", 40, self.creditsx, self.creditsy)
            self.draw_click()
            self.blit_screen()

# reference: https://www.youtube.com/watch?v=bmRFi7-gy5Y&ab_channel=ChristianDuenas
    def move_click(self):
        # if player presses down
        if self.game.DOWN:
            if self.state == 'Start':
                self.click_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.click_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.click_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
       # if player presses up
        elif self.game.UP:
            if self.state == 'Start':
                self.click_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Controls':
                self.click_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.click_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = 'Controls'

    def check_input(self):
        self.move_click()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Controls':
                self.game.curr_menu = self.game.controls
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class ControlsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Instructions'
        self.instr, self.instry = self.mid_w, self.mid_h + 20
# show menu
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('How to play', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 150)
            self.game.draw_text('Use the left and right arrow keys to move', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 40)
            self.game.draw_text('Use the space bar to jump', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 10)
            self.game.draw_text('Press SPACE twice to double jump', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.game.draw_text('Avoid the fire and keep running to earn points', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)
            self.game.draw_text('Catch the water droplets to earn extra points', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 90)
            self.draw_click()
            self.blit_screen()
# check player input
    def check_input(self):
        if self.game.BACK:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP or self.game.DOWN:
                self.state = 'Controls'
                self.click_rect.midtop = (self.controlsx + self.offset, self.controlsy)
        elif self.game.START_KEY:
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 150)
            self.game.draw_text('Brought to you by ', 48, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 0)
            self.game.draw_crText('Zenantsy', 100, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 90)
            self.blit_screen()