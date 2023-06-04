import math
import Helpers
class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.05

    def rotate(self, left=False, right=False):
        self.angle += left * 2 + right * -2

    def draw(self, win):
        Helpers.blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move(self):
        rad = math.radians(-self.angle)
        vertical_v = -math.cos(rad)*self.vel
        horizontal_v = math.sin(rad)*self.vel
        self.x += horizontal_v
        self.y += vertical_v

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel) #threshold is max_vel
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel) #threshold is max_vel
        self.move()

    def reduce_speed(self):
        if self.vel>0:
            self.vel = max(self.vel - self.acceleration / 4, 0)

        if self.vel<0:
            self.vel = min(self.vel + self.acceleration / 4, 0)
        self.move()