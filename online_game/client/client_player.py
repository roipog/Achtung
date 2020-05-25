import pygame

UDP_MSG_LENGTH = 4


class Player(pygame.sprite.Sprite):
    """ main game object"""
    # inheritance pygame.sprite.Sprite class, must contain self.image for draw and  self.rect for place update

    def __init__(self, path, xy):
        self.path = path
        self.x, self.y = xy
        pygame.sprite.Sprite.__init__(self)  # as super()
        self.image = pygame.image.load(self.path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.trail = []
        self.new_trail = None

    def set_data(self, x, y, tx, ty):
        self.rect.x = x
        self.rect.y = y
        if tx and ty and tx != 0 and ty != 0:
            self.new_trail = Client_trail(tx, ty)
            self.trail.append(self.new_trail)

    def draw_text(self, text):
        """Center text in window
        """
        fw, fh = self.font.size(text)  # fw: font width,  fh: font height
        surface = self.font.render(text, True, (0, 255, 0))
        # // makes integer division in python3
        self.screen.blit(surface, (self.rect.x, self.rect.y))


class Client_trail(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.path = "../imgs/trail.png"
        pygame.sprite.Sprite.__init__(self)  # as super()
        self.image = pygame.image.load(self.path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
