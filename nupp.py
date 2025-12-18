import pygame

class Nupp():
    def __init__(self, pos, tekst_input, font, värv, hover_värv, bg_värv, bg_hover):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.tekst_input = tekst_input
        self.font = font
        self.värv, self.hover_värv = värv, hover_värv
        self.tekst = self.font.render(self.tekst_input, True, self.värv)
        self.rect = self.tekst.get_rect(center=(self.x_pos, self.y_pos))
        self.bg_värv = bg_värv
        self.bg_hover = bg_hover
        self.tekst_rect = self.tekst.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, aken):
        nuppu_rect = self.tekst.get_rect(center=(self.x_pos, self.y_pos))

        põhi = pygame.Surface(nuppu_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(põhi, self.aktiivne_bg, põhi.get_rect(), border_radius=10)

        tekst_rect_local = self.tekst.get_rect(center=(nuppu_rect.width / 2, nuppu_rect.height / 2))
        põhi.blit(self.tekst, tekst_rect_local)

        aken.blit(põhi, nuppu_rect.topleft)

        self.rect = nuppu_rect

    def kontrollForInput(self, asend):
        if asend[0] in range(self.rect.left, self.rect.right) and asend[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def muudaVärvi(self, asend):
        if self.kontrollForInput(asend):
            self.tekst = self.font.render(self.tekst_input, True, self.hover_värv)
            self.aktiivne_bg =self.bg_hover
        else:
            self.tekst = self.font.render(self.tekst_input, True, self.värv)
            self.aktiivne_bg = self.bg_värv
