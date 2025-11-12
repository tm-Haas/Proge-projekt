from sätted import ASTEROIDI_KIIRUS, VAENLASE_KIIRUS, KOKKUPÕRGE_RECT_LIIGE
from pygame import Rect, Vector2, image, transform
from random import uniform, choice
from math import floor

class Liikuja:
    def __init__(self, x:int, y:int, suund:Vector2, kiiruse_korrutaja:float = 1.0, kiirus = 10):
        self.x = x
        self.y = y
        self.kiirus = kiirus
        self.suund = suund.normalize()

    
    def uuenda_suuna(self,uus_suund:Vector2) -> None:
        self.suund = uus_suund.normalize()
    

class Asteroid(Liikuja):
    asteroidi_pildid = [
        image.load("pildid/asteroid_1.png"),
        image.load("pildid/asteroid_2.png")
    ]
    #kiiruse korrutaja idee on, et mida kauem mäng kestab seda kiiremini asteroidid lendavad
    def __init__(self, x:int, y:int, r:str, suund:Vector2,kiiruse_korrutaja:float = 1.0,kiirus:int = ASTEROIDI_KIIRUS):
        super().__init__(x,y,suund)
        match r:
          case  "Suur": self.size = 100
          case  "Keskmine": self.size = 60
          case  default: self.size = 35
        self.r = r
        self.kiirus = uniform(0.3*kiirus, (kiirus - self.size) * 4/15)
        self.pilt = choice(Asteroid.asteroidi_pildid)
        self.pilt = transform.scale(self.pilt, (self.size, self.size))

        self.rect = self.pilt.get_rect(center=(self.x, self.y))
        #Teooria selle taga paikneb https://www.pygame.org/docs/tut/newbieguide.html#don-t-bother-with-pixel-perfect-collision-detection
        self.kokkupõrke_rect = self.pilt.get_rect(center=(self.x-KOKKUPÕRGE_RECT_LIIGE, self.y-KOKKUPÕRGE_RECT_LIIGE))
   
    # Siia teha asteroidi sprite


    def asteroid_liikumine(self) -> None:
        #ei tohi jätta ujukomaarvudena muidu rect.center hakkab nutma suuri pisaraid waaa
        self.x += floor(self.suund.x*self.kiirus)
        self.y += floor(self.suund.y*self.kiirus)



    def joonista_asteroid(self, aken) -> None:
        self.asteroid_liikumine()
        self.rect.center = (self.x, self.y)
        self.kokkupõrke_rect.center = (self.x-KOKKUPÕRGE_RECT_LIIGE, self.y-KOKKUPÕRGE_RECT_LIIGE)
        aken.blit(self.pilt, self.rect) 


class Vaenlane(Liikuja):
    #vaja teisi pilte:)
    vaenlase_pildid = [
        image.load("pildid/asteroid_1.png"),
        image.load("pildid/asteroid_2.png")
    ]
    def __init__(self,x:int,y:int,suund:Vector2,kiiruse_korrutaja:float = 1.0,kiirus:int = VAENLASE_KIIRUS):
        super().__init__(x,y,suund)
        self.size = 10
        self.kiirus = uniform(10, 20 * 4/15)
        self.pilt = choice(Vaenlane.vaenlase_pildid)
        self.pilt = transform.scale(self.pilt, (self.size, self.size))
        self.rect = self.pilt.get_rect(center=(self.x, self.y))
        self.kokkupõrke_rect = self.pilt.get_rect(center=(self.x-KOKKUPÕRGE_RECT_LIIGE, self.y-KOKKUPÕRGE_RECT_LIIGE))

    def vaenlane_liikumine(self) -> None:
        self.x += floor(self.suund.x*self.kiirus)
        self.y += floor(self.suund.y*self.kiirus)


    def joonista_vaenlane(self, aken) -> None:
        self.vaenlane_liikumine()
        self.rect.center = (self.x, self.y)
        self.kokkupõrke_rect.center = (self.x-KOKKUPÕRGE_RECT_LIIGE, self.y-KOKKUPÕRGE_RECT_LIIGE)
        aken.blit(self.pilt, self.rect)