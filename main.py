import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')


# define game variables
ground_scroll = 0
scroll_speed = 4
is_flying = False
is_game_over = False

# load images
bg = pygame.image.load('assets/environment/bg.png')
ground_img = pygame.image.load('assets/environment/ground.png')


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'assets/character/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.clicked = False

    def update(self):

        # handle gravity
        if is_flying:
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.velocity)
        if is_game_over == False:
            # handle flap
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False

            # handle the flap animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # handle bird facing direction
            self.image = pygame.transform.rotate(
                self.images[self.index], self.velocity * -3)
        else:
            self.image = pygame.transform.rotate(
                self.images[self.index], -90)


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)


run = True
while run:

    clock.tick(fps)

    # draw background
    screen.blit(bg, (0, 0))

    # draw bird
    bird_group.draw(screen)
    bird_group.update()

    # draw ground
    screen.blit(ground_img, (ground_scroll, 768))

    # check if bird hit ground
    if flappy.rect.bottom > 768:
        is_game_over = True
        is_flying = False

    # scroll the ground under background
    if is_game_over == False:
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and is_flying == False and is_game_over == False:
            is_flying = True

    pygame.display.update()

pygame.quit()
