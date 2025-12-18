from pygame import Vector2, image, transform
from math import floor

class Liikuja:
    def __init__(self, x, y, suund:Vector2, kiirus, kiiruse_korrutaja: float=1.0):
        self.x = x
        self.y = y
        self.kiirus = kiirus
        self.suund = suund

    def uuenda_suunda(self, uus_suund):
        self.suund = uus_suund.normalize()

class Kuul(Liikuja):
    def __init__(self, x:int, y:int, kuul_pilt, korrutaja):
        tegelik_kiirus = 10 * korrutaja
        super().__init__(x, y, Vector2(0, -1), kiirus=tegelik_kiirus)

        self.pilt = image.load(kuul_pilt)
        self.pilt = transform.scale(self.pilt, (25, 35))
        self.rect = self.pilt.get_rect(center=(self.x, self.y))

    def liiguta(self):
        self.x += floor(self.suund.x * self.kiirus)
        self.y += floor(self.suund.y * self.kiirus)
        self.rect.center = (self.x, self.y)


