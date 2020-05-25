import pygame


class Player(pygame.sprite.Sprite):
    """ main game object"""
    # inheritance pygame.sprite.Sprite class, must contain self.image for draw and  self.rect for place update

    def __init__(self, xy, start_speed):
        self.x, self.y = xy
        self.start_speed = start_speed
        self.max_speed = 5
        self.min_speed = self.max_speed * -1
        pygame.sprite.Sprite.__init__(self)  # as super()
        self.dx = 0  # future x offset from current position
        self.dy = 0  # future y offset from current position
        self.trail = []
        self.new_trail = None
        self.playing = True
        self.counter = 0

    def p_update(self):
        # Move each axis separately. Note that this checks for collisions both times.
        if self.dx != 0:
            self.move_single_axis(self.dx, 0)
        if self.dy != 0:
            self.move_single_axis(0, self.dy)

    def sp_set_dxy(self, key):
        if key == "start":
            if self.dx == 0 and self.dy == 0 and self.playing:
                self.dx = self.start_speed
        elif key == "left":
            self.move_left()
        elif key == "right":
            self.move_right()

    def move_left(self):
        if self.dx == 0:
            if self.dy == self.max_speed:
                self.dx += 1
                self.dy -= 1
            elif self.dy == self.min_speed:
                self.dx -= 1
                self.dy += 1
        elif self.dy == 0:
            if self.dx == self.max_speed:
                self.dx -= 1
                self.dy -= 1
            elif self.dx == self.min_speed:
                self.dx += 1
                self.dy += 1
        elif self.dx > 0:
            if self.dy < 0:
                self.dx -= 1
                self.dy -= 1
            elif self.dy > 0:
                self.dx += 1
                self.dy -= 1
        elif self.dx < 0:
            if self.dy < 0:
                self.dx -= 1
                self.dy += 1
            elif self.dy > 0:
                self.dx += 1
                self.dy += 1

    def move_right(self):
        if self.dx == 0:
            if self.dy == self.max_speed:
                self.dx -= 1
                self.dy -= 1
            elif self.dy == self.min_speed:
                self.dx += 1
                self.dy += 1
        elif self.dy == 0:
            if self.dx == self.max_speed:
                self.dx -= 1
                self.dy += 1
            elif self.dx == self.min_speed:
                self.dx += 1
                self.dy -= 1
        elif self.dx > 0:
            if self.dy < 0:
                self.dx += 1
                self.dy += 1
            elif self.dy > 0:
                self.dx -= 1
                self.dy += 1
        elif self.dx < 0:
            if self.dy < 0:
                self.dx += 1
                self.dy -= 1
            elif self.dy > 0:
                self.dx -= 1
                self.dy -= 1

    def move_single_axis(self, dx, dy):
        # Move the rect
        self.x += dx
        self.y += dy
        if self.counter < 12:
            self.new_trail = Trail(self)
            self.trail.append(self.new_trail)
        elif self.counter == 20:
            self.counter = 0
        self.counter += 1


class Trail(pygame.sprite.Sprite):
    def __init__(self, player):
        if player.dx == 0 and player.dy == 0:
            self.x = 0
            self.y = 0
        else:
            if player.dx <= 0:
                self.x = player.x - player.dx + 1
            elif player.dx > 0:
                self.x = player.x - player.dx - 1
            if player.dy <= 0:
                self.y = player.y - player.dy + 1
            elif player.dy > 0:
                self.y = player.y - player.dy - 1
