from pygame import Rect, Vector2, image, transform
from kuul import Liikuja
from sätted import *
from math import floor 
from random import uniform, choice

class Asteroid(Liikuja):
    asteroidi_pildid = [
        image.load("pildid/asteroid_1.png"),
        image.load("pildid/asteroid_2.png")
    ]
    #kiiruse korrutaja idee on, et mida kauem mäng kestab seda kiiremini asteroidid lendavad
    def __init__(self, x:int, y:int, r:str, suund:Vector2,kiiruse_korrutaja:float = 1.0,kiirus:int = ASTEROIDI_KIIRUS):
        super().__init__(x,y,suund, kiirus=kiirus*kiiruse_korrutaja)
        match r:
          case  "Suur": self.size = 80
          case  "Keskmine": self.size = 50
          case  default: self.size = 25
        self.r = r
        self.kiirus = uniform(kiirus, kiirus + 2)
        self.pilt = choice(Asteroid.asteroidi_pildid)
        self.pilt = transform.scale(self.pilt, (self.size, self.size))

        self.rect = self.pilt.get_rect(center=(self.x, self.y))
        #Teooria selle taga paikneb https://www.pygame.org/docs/tut/newbieguide.html#don-t-bother-with-pixel-perfect-collision-detection
        self.kokkupõrke_rect = self.pilt.get_rect(center=(self.x-KOKKUPÕRGE_RECT_LIIGE, self.y-KOKKUPÕRGE_RECT_LIIGE))
   
    # Siia teha asteroidi sprite


    def asteroid_liikumine(self) -> None:
        self.x += floor(self.suund.x*self.kiirus)
        self.y += floor(self.suund.y*self.kiirus)



    def joonista_asteroid(self, aken) -> None:
        self.asteroid_liikumine()
        self.rect.center = (self.x, self.y)
        self.kokkupõrke_rect.center = (self.x-KOKKUPÕRGE_RECT_LIIGE, self.y-KOKKUPÕRGE_RECT_LIIGE)
        aken.blit(self.pilt, self.rect) 


class Vaenlane(Liikuja):
    vaenlase_pildid = [
        image.load("pildid/vaenlane_1.png"),
        image.load("pildid/vaenlane_2.png"),
        image.load("pildid/vaenlane_3.png"),
    ]
    def __init__(self,x:int,y:int,suund:Vector2,kiiruse_korrutaja:float = 1.0,kiirus:int = VAENLASE_KIIRUS):
        super().__init__(x,y,suund, kiirus=kiirus*kiiruse_korrutaja)
        self.size = 45
        self.kiirus = uniform(kiirus, kiirus+2)
        self.pilt = choice(Vaenlane.vaenlase_pildid)
        self.pilt = transform.scale(self.pilt, (self.size, self.size))
        self.rect = self.pilt.get_rect(center=(self.x, self.y))
        self.kokkupõrke_rect = self.pilt.get_rect(center=(self.x-KOKKUPÕRGE_RECT_LIIGE, self.y-KOKKUPÕRGE_RECT_LIIGE))

    def vaenlane_liikumine(self) -> None:
        self.x += self.suund.x*self.kiirus
        self.y += self.suund.y*self.kiirus


    def joonista_vaenlane(self, aken) -> None:
        self.rect.center = (self.x, self.y)
        self.kokkupõrke_rect.center = (self.x-KOKKUPÕRGE_RECT_LIIGE, self.y-KOKKUPÕRGE_RECT_LIIGE)
        aken.blit(self.pilt, self.rect)
        aken.blit(self.pilt, self.rect)
