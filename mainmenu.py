import defines as gm

pygame = gm.pygame
screen = gm.screen


class Option:
    hovered = False

    def __init__(self, text, pos, menu_font, screen):
        self.menu_font = menu_font
        self.screen = screen
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        self.screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (gm.GRAY)
        else:
            return (gm.WHITE)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos


def mm():
    pygame.event.pump()
    screen.blit(gm.bg_layer1, (0, 0))
    screen.blit(gm.bg_layer2, (0, 0))
    screen.blit(gm.bg_layer3, (0, 0))
    screen.blit(gm.bg_layer4, (0, 0))
    screen.blit(gm.bg_layer5, (0, 0))

    start_button = Option("START GAME", ((screen.get_width() / 3), screen.get_height() / 2), gm.menu_font, screen)
    exit_button = Option("EXIT", ((screen.get_width() / 3) + 140, screen.get_height() / 2 + 200), gm.menu_font, screen)
    options = [start_button, exit_button]

    for option in options:
        mouse = pygame.mouse.get_pos()
        if option.rect.collidepoint(mouse):
            option.hovered = True
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.rect.collidepoint(mouse):
                        return 1
                    if option_button.rect.collidepoint(mouse):  # decide to options or not
                        return 2
                    if exit_button.rect.collidepoint(mouse):
                        exit(1)
        else:
            option.hovered = False
        option.draw()


def lost_menu():
    screen.blit(gm.panel, (gm.WIDTH / 6 + 10, 200))
    font = gm.screens_font
    losttxt = 'You have lost, your score is'
    losttxt3 = str(gm.score.score_get())
    losttxt4 = 'press ESC'
    losttxt = font.render(losttxt, True, gm.WHITE)
    screen.blit(losttxt, (290, 230))
    losttxt3 = font.render(losttxt3, True, gm.WHITE)
    screen.blit(losttxt3, (gm.WIDTH / 2 + 40 - 100, 300))
    losttxt4 = font.render(losttxt4, True, gm.WHITE)
    screen.blit(losttxt4, (gm.WIDTH / 3 + 80, 370))

def chapter_win_screen():
    screen.blit(gm.panel, (gm.WIDTH / 6 + 10, 200))
    font = gm.screens_font
    inf1 = 'Stage completed!'
    inf2 = 'Score: ' + str(gm.score.score_get())
    inf3 = 'press ESC'
    w1 = font.render(inf1, True, gm.WHITE)
    screen.blit(w1, (gm.WIDTH / 3, 230))
    w2 = font.render(inf2, True, gm.WHITE)
    screen.blit(w2, (gm.WIDTH / 3 + 40, 300))
    w3 = font.render(inf3, True, gm.WHITE)
    screen.blit(w3, (gm.WIDTH / 3 + 40 + 20, 370))
