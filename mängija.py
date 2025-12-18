import pygame
from pygame import Rect, Vector2, image, transform
from kuul import Liikuja
from math import *
from sätted import *
from kuul import Kuul

class Mängija(Liikuja):
    #avatar tuleb vastavalt valitud avatarile
    # võimalik valikda 3-st üks

    def __init__(self, x, y, kiirus, valitud_tegelane):
        korrutaja = valitud_tegelane.get("kiirus_korrutaja", 1.0)
        super().__init__(x, y, Vector2(0,0), kiirus=kiirus, kiiruse_korrutaja=korrutaja)
        self.valitud_tegelane = valitud_tegelane
        self.suurus = 50
        self.pilt = transform.scale(image.load(valitud_tegelane["pilt"]), (self.suurus, self.suurus) )

        self.rect = self.pilt.get_rect(center=(self.x, self.y))
        self.kokkupõrke_rect = self.rect.copy()

        self.viimane_tulistamise_aeg = 0
        self.tulistamise_viivitus = 200/korrutaja

    def liiguta(self, keys):
        self.suund = Vector2(0,0)

        if keys[pygame.K_LEFT]:
            self.suund.x -= 1
        if keys[pygame.K_RIGHT]:
            self.suund.x += 1

        self.x += floor(self.suund.x * self.kiirus)

        self.x = max(self.suurus // 2, min(self.x, AKEN_LAIUS - self.suurus // 2))
        self.y = AKEN_KÕRGUS - 50

    def joonista(self, aken):
        self.rect.center = (self.x, self.y)
        self.kokkupõrke_rect.center = (self.x, self.y)
        aken.blit(self.pilt, self.rect)

    def tulista(self, kuulid):
        praegune_aeg = pygame.time.get_ticks()
        if praegune_aeg - self.viimane_tulistamise_aeg > self.tulistamise_viivitus:
            korrutaja = self.valitud_tegelane.get("kiirus_korrutaja", 1.0)
            kuul = self.valitud_tegelane["kuul"]
            uus_kuul = Kuul(self.x, self.y - 20, kuul, korrutaja)
            kuulid.append(uus_kuul)
            self.viimane_tulistamise_aeg = praegune_aeg
        aken.blit(kuuli_pilt, rect)
