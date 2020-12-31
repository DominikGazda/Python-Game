import defines as gm
pygame = gm.pygame
screen = gm.screen

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, direction, rect_center_x, rect_center_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [rect_center_x, rect_center_y]
        self.direction_of_movement = direction


    def update(self):

        if self.direction_of_movement == 'right':
            self.rect.x += 20
        elif self.direction_of_movement == 'left':
            self.rect.x -= 20
        elif self.direction_of_movement == 'up':
            self.rect.y -= 20
        else:
            self.rect.y += 20

