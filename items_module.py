import defines as gm
from random import choice
pygame = gm.pygame
screen = gm.screen

#klasa przedmiotu
class Item(pygame.sprite.Sprite):
    def __init__(self, image, name, rect_center_x, rect_center_y):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.name = name
        self.rect.center = [rect_center_x, rect_center_y]

class ItemWithAnimation(Item):
    def __init__(self, image , image_list, name , rect_center_x, rect_center_y):
        super().__init__(image, name ,rect_center_x,rect_center_y)
        self.lifes = 4
        self.image_list = image_list
        self.count = 0
        self.rect_center_x = rect_center_x
        self.rect_center_y = rect_center_y

        self.rect_1  = pygame.draw.rect(screen, gm.LIGHTBLUE, (
                   self.rect.x,self.rect.y , 0, 0))


        self.rect_2 = pygame.draw.rect(screen, gm.LIGHTBLUE, (
                   self.rect.x,self.rect.y , 0, 0))

    def update(self):
        if self.lifes == 4:
            self.image = self.image_list[0]
        elif self.lifes == 3:
            self.image = self.image_list[1]
        elif self.lifes == 2:
            self.image = self.image_list[2]
        elif self.lifes == 1:
            self.image = self.image_list[3]
        elif self.lifes == 0:
            self.image = self.image_list[4]
            self.name = 'strong_card'
        if self.name =='spikes':
            if self.count < 2:
                self.image = self.image_list[0]
            elif self.count < 12:
                self.image = self.image_list[1]
            elif self.count < 22:
                self.image = self.image_list[2]
            elif self.count < 32:
                self.image = self.image_list[3]
            elif self.count < 52:
                self.image = self.image_list[4]

            if self.count >= 52:
                self.count = 0
            else:
                self.count += 1
        if self.name == 'explosion':
            if self.count < 2:
                self.image = self.image_list[0]
            elif self.count < 12:
                self.image = self.image_list[1]
            elif self.count < 22:
                self.image = self.image_list[2]
            elif self.count < 32:
                self.rect.center = [self.rect_center_x-54, self.rect_center_y-50]
                self.rect_1 = pygame.draw.rect(screen, ((255, 0, 0)), (
                    self.rect.x , self.rect.y +60, self.rect.right - self.rect.left + 100,
                    int((self.rect.bottom - self.rect.top) - 30)))

                self.rect_2 = pygame.draw.rect(screen, ((255, 0, 0)), (
                    self.rect.x +68, self.rect.y , self.rect.right - self.rect.left - 30,
                    int((self.rect.bottom + 50 - self.rect.top) + 50)))
                self.image = self.image_list[3]
            elif self.count < 42:
                self.image = self.image_list[4]
            elif self.count < 52:
                self.image = self.image_list[5]
            elif self.count < 62:
                self.image = self.image_list[6]
            elif self.count < 72:
                self.image = self.image_list[7]
            if self.count == 71:
                self.name = 'end_explosion'
            else:
                self.count += 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)
