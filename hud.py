from defines import *

class HUD:
    def __init__(self):
        self.score = 0
        self.bombs = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 40)

    def display(self):
        self.score = score.score_get()
        text = f'Score = ' + str(self.score)
        pkt = self.font.render(text, True, (100, 255, 100))
        screen.blit(pkt, (20, 10))

        screen.blit(BOMB, (WIDTH - 80, 10,  30, 30))
        counter = self.font.render(str(self.bombs), True, (100, 255, 100))
        screen.blit(counter, (WIDTH - 100, 10))

    def set_bombs_count(self, number):
        self.bombs = number