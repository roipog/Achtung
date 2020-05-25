import pygame


class Block(pygame.sprite.Sprite):  # inheritance pygame.sprite.Sprite class, must contain self.image for draw and  self.rect for update
    """ map object"""

    img_paths = {"t": "../imgs/top_and_bottom.png", "s": "../imgs/sides.png"}

    def __init__(self, x, y, char):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.img_paths[char]).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))


class Map:
    """ map"""

    def __init__(self, blocks, group):
        block_list = [Block(0, 0, "t"), Block(0, 0, "s"), Block(0, 590, "t"), Block(1190, 0, "s")]
        for block in block_list:
            blocks.append(block)
            group.add(block)
