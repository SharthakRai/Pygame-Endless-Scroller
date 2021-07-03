
import pygame
import random

BLACK = (0, 0, 0)
WIDTH = 1280
HEIGHT = 720
FPS = 30
BACKGROUND = BLACK


pygame.init()
# initialize sound
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Chase")
appIcon = pygame.image.load('background/game icon.png')
pygame.display.set_icon(appIcon)

# define game variables
bg_scroll_speed = 3
front_scroll_speed = 15
ground_scroll_speed = 20

class GameStats:
    score = 0
    lives = 5

game_stats = GameStats()

# background music
backgroundMusic = pygame.mixer.music.load('music/bgMusic.mp3')
pygame.mixer.music.play(-1)

# sky image
bg_sky = pygame.image.load('background/bg1.png')

# background trees image
bg_surface = pygame.image.load('background/bg2.png')
bg_surface = pygame.transform.scale(bg_surface, (1280, 720))
bg_surfaceX = 0
bg_surfaceX2 = bg_surface.get_width()

# front trees image
front_surface = pygame.image.load('background/bg5.png')
front_surface = pygame.transform.scale(front_surface, (1280, 720))
front_surfaceX = 0
front_surfaceX2 = front_surface.get_width()

# ground image
ground_img = pygame.image.load('background/game_ground.jpg')
ground_img = pygame.transform.scale(ground_img, (1280, 60))
ground_imgX = 0
ground_imgX2 = ground_img.get_width()
ground_rect = ground_img.get_rect(center = (1280,60)) # for collison detection


# start the clock
clock = pygame.time.Clock()
game_font = pygame.font.Font('Franchise.ttf', 50)
hitSound = pygame.mixer.Sound('music/hit sound.wav')
waterSound = pygame.mixer.Sound('music/water.wav')
jumpSound = pygame.mixer.Sound('music/8 bit jump.wav')
gameOverSound = pygame.mixer.Sound('music/game over.wav')

def redraw_window():
    screen.fill(BACKGROUND)
    screen.blit(bg_sky, (0, 0))

    screen.blit(bg_surface, (bg_surfaceX, 0))
    screen.blit(bg_surface, (bg_surfaceX2, 0))

    screen.blit(front_surface, (front_surfaceX, 0))
    screen.blit(front_surface, (front_surfaceX2, 0))

    screen.blit(ground_img, (ground_imgX, 658))
    screen.blit(ground_img, (ground_imgX2, 658))



# display player score + lives
def score_count():
    score_display = game_font.render('Score: '+ str(int(game_stats.score)), True, (255,255,255))
    score_rect = score_display.get_rect()
    score_rect.x = 20
    score_rect.y = 20
    screen.blit(score_display, score_rect)
    lives_display = game_font.render('Lives: ' + str(game_stats.lives), True,(255, 255, 255))
    lives_rect = lives_display.get_rect()
    lives_rect.x = 20
    lives_rect.y = 75
    screen.blit(lives_display, lives_rect)



#reference: https://github.com/russs123/Platformer player class inspiration
class Character():
    def __init__(self, x, y):
        self.sprites_right = []
        self.sprites_left = []
        self.index = 0
        self.counter = 0
        for sprite in range(1, 5):
            # loop through images named 1 to 4
            move_right = pygame.image.load(f'character/{sprite}.png')
            move_right = pygame.transform.scale(move_right, (130, 100))
            move_left = pygame.transform.flip(move_right, True, False) # horizontally flip the image to left
            # # add images on to the list
            self.sprites_right.append(move_right)
            self.sprites_left.append(move_left)
        self.image = self.sprites_right[self.index]	# initial image (index = 0)
        self.rect = self.image.get_rect() # draw rectangle around for collision detection
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jump = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        run_timer = 2

        #character keys
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jump == False:
            self.vel_y -= 32
            self.jump = True
            jumpSound.play()
        if not key[pygame.K_SPACE] and self.rect.bottom == HEIGHT - 50:
            self.jump = False
        #acceleration towards ground
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #move left or right
        if key[pygame.K_LEFT]:
            dx -= 12
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 12
            self.direction = 1

        #character right and left movement animation
        self.counter += 1
        if self.counter > run_timer:
            self.counter = 0
            self.index += 1
            # iterate through the images images list
            # index = 0 if index is greater than size of list
            if self.index >= len(self.sprites_right):
                self.index = 0
            self.image = self.sprites_right[self.index]
            if self.direction == 1:
                self.image = self.sprites_right[self.index]
            if self.direction == -1:
                self.image = self.sprites_left[self.index]

        #character coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            dy = 0
        if self.rect.left < 0:
            self.rect.left = 0
            dx = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            dx = 1280


        #draw character onto screen
        screen.blit(self.image, self.rect)

        #character starting position
player = Character(300, HEIGHT - 150)

class FallingObject:
    to_delete = False
    def __init__(self, image_path):
        self.image = pygame.transform.scale(pygame.image.load(image_path), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.random() * WIDTH
        self.rect.y = 0

    def redraw(self, screen: pygame.Surface):
        self.rect.y += 4
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.right > player.rect.left and self.rect.left < player.rect.right and self.rect.top < player.rect.bottom and self.rect.bottom > player.rect.top:
            self.on_player_collide()
            self.to_delete = True

        if self.rect.top > HEIGHT:
            self.to_delete = True

    def on_player_collide(self):
        pass

class Firebomb(FallingObject):
    def __init__(self):
        super().__init__('background/forest_fireball.png')

    def on_player_collide(self):
        hitSound.play()
        game_stats.lives -= 1

class Waterbomb(FallingObject):
    def __init__(self):
        super().__init__('background/water_bomb.png')

    def on_player_collide(self):
        waterSound.play()
        game_stats.score += 10
        

falling_objects = []


running = True
# start the game loop
while running:
    redraw_window()
    # keep the loop running at the right speed
    clock.tick(FPS)
    #increase player score
    game_stats.score += 0.1
    # display and count score
    score_count()

    # scrolling trees

    bg_surfaceX -= bg_scroll_speed
    bg_surfaceX2 -= bg_scroll_speed
    if bg_surfaceX < bg_surface.get_width() * -1:
        bg_surfaceX = bg_surface.get_width()
    if bg_surfaceX2 < bg_surface.get_width() * -1:
        bg_surfaceX2 = bg_surface.get_width()

    front_surfaceX -= front_scroll_speed
    front_surfaceX2 -= front_scroll_speed
    if front_surfaceX < front_surface.get_width() * -1:
        front_surfaceX = front_surface.get_width()
    if front_surfaceX2 < front_surface.get_width() * -1:
        front_surfaceX2 = front_surface.get_width()

    # scrolling ground
    ground_imgX -= ground_scroll_speed
    ground_imgX2 -= ground_scroll_speed
    if ground_imgX < ground_img.get_width() * -1:
        ground_imgX = ground_img.get_width()
    if ground_imgX2 < ground_img.get_width() * -1:
        ground_imgX2 = ground_img.get_width()

    # falling objects
    if random.random() < 0.1:
        falling_objects.append(Firebomb()if random.random() < 0.5 else Waterbomb())

    for falling_object in falling_objects:
        falling_object.redraw(screen)

    falling_objects = list(filter(lambda o: not o.to_delete, falling_objects))


    #character class in while loop
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    pygame.display.update()
