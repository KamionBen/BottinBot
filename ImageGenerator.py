import pygame
from pygame.locals import *

pygame.init()

RESOLUTION = (1280, 720)
DISPLAYSURF = pygame.display.set_mode((RESOLUTION[0]/2, RESOLUTION[1]))

DEFAULT_FONT = pygame.font.Font(None, 40)
BOLD_FONT = pygame.font.Font(None, 40)
#BOLD_FONT.set_bold(True)
LITTLE_FONT = pygame.font.Font(None, 20)
BG_IMG = pygame.image.load('img/bg_image.png').convert()


def round_number(number):
    """ Return a readable version of the subscribers number """
    if number > 1000000:
        return f"{round(number / 1000000, 2)}M"
    elif number > 1000:
        return f"{round(number / 1000)}k"
    else:
        return number


def generate_image(sublist, title, subtitle, output=None, panel=1, preview=False):
    """ Creating the background """
    resolution = (640, 720)
    display_surf = pygame.display.set_mode(resolution)
    display_surf.fill((0,0,0))
    if panel == 1:
        display_surf.blit(BG_IMG, (0,0))  # First half of the background image
    elif panel == 2:
        display_surf.blit(BG_IMG, (-resolution[0], 0))  # Second half

    """ HEADER """
    title = DEFAULT_FONT.render(title, True, (255, 255, 255))
    subtitle = DEFAULT_FONT.render(subtitle, True, (255, 255, 255))
    DISPLAYSURF.blit(title, (resolution[0] / 2 - title.get_width() / 2, 10))
    DISPLAYSURF.blit(subtitle, (resolution[0] / 2 - subtitle.get_width() / 2, 40))

    """ GET SUB LIST """
    top = sublist[0].subscribers  # Get the maximum subscribers to display
    y = 100
    """ ADD THEM TO THE IMAGE """
    for i, sub in enumerate(sublist):
        name = str(sub)
        category = f"[{sub.category.upper()}]"
        subscribers = sub.subscribers

        sub_frame = pygame.surface.Surface((resolution[0] - 100, 50), pygame.SRCALPHA, 32)
        sub_frame.convert_alpha()
        sub_frame.fill((128, 128, 128, 128))  # I need to find a way to set the alpha to 128 here

        width = subscribers / top * (resolution[0] - 100)
        pygame.draw.rect(sub_frame, (0, 0, 0), (0, 0, width, 50))

        sub_name = DEFAULT_FONT.render(name, True, (255, 255, 255))
        title_shadow = BOLD_FONT.render(name, True, (0,0,0))
        cat = LITTLE_FONT.render(category, True, (255, 255, 255))
        sub_nb = DEFAULT_FONT.render(round_number(subscribers), True, (255, 255, 255))

        sub_frame.blit(sub_nb, (100 - sub_nb.get_width(), 25-(sub_nb.get_height()/2)))
        sub_frame.blit(title_shadow, (122, 22))
        sub_frame.blit(sub_name, (120, 20))
        sub_frame.blit(cat, (120, 5))

        display_surf.blit(sub_frame, (50, 60 * i + y))

    while preview:
        for event in pygame.event.get():
            pygame.display.update()
            if event.type == QUIT:
                preview = False

    if output is not None:
        pygame.image.save(DISPLAYSURF, output)

