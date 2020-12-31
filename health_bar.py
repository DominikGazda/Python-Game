import defines as gm
pygame = gm.pygame
screen = gm.screen

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, health):
        super().__init__()
        self.health_max = health
        self.health_current = health
        self.width = 80

    def decreaseHealth(self):
         self.health_current -= 1
         if self.health_current <= 0:
             self.width = 0
             self.bar = None
         else:
            dzielnik = self.health_max / self.health_current
            self.width = int(80 / dzielnik)

    def increaseHealth(self):
        self.health_current += 1
        dzielnik = self.health_max / self.health_current
        self.width = int(80 / dzielnik)

    def draw(self, rect_x, rect_y):
        if self.health_current > 0:
            self.frame = pygame.draw.rect(screen, gm.WHITE, (rect_x - 2, rect_y - 17, 84, 14))
            self.bar = pygame.draw.rect(screen, gm.RED, (rect_x, rect_y - 15, self.width, 10))