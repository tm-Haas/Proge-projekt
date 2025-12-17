import pygame
from sätted import AKEN_LAIUS, ÜLEMINE_ÄÄR

bullet_speed = 10
bullet_width = 4
bullet_height = 8
shoot_cooldown = 300

mängija_pilt = pygame.image.load("pildid/tulistaja.png")
mängija_pilt = pygame.transform.smoothscale(mängija_pilt, (30, 30))

kuuli_pilt = pygame.image.load("pildid/bullet1.png")
kuuli_pilt = pygame.transform.smoothscale(kuuli_pilt, (bullet_width, bullet_height))

viimane_shoot_aeg = 0

def mängija_loogika(nupud, kuulid, mängija):
    global viimane_shoot_aeg
    current_time = pygame.time.get_ticks()

    kiirus = 6
    
    #liikumine
    if nupud[pygame.K_LEFT]:
        mängija["x"] -= kiirus
    if nupud[pygame.K_RIGHT]:
        mängija["x"] += kiirus
    
    mängija["x"] = max(0, min(AKEN_LAIUS, mängija["x"]))

    if nupud[pygame.K_SPACE]:
        if current_time - viimane_shoot_aeg >= shoot_cooldown:
            kuulid.append({
                "x": mängija["x"] - bullet_width // 2,
                "y": mängija["y"] - mängija["size"] // 2,
                "width": bullet_width,
                "height": bullet_height
            })
            viimane_shoot_aeg = current_time



def kuulide_loogika(kuulid):
    for kuul in kuulid[:]:
        kuul["y"] -= bullet_speed
        if kuul["y"] + kuul["height"] < 0:
            kuulid.remove(kuul)


def mängija_joonistamine(aken, mängija):
    rect = mängija_pilt.get_rect(center=(mängija["x"], mängija["y"]))
    aken.blit(mängija_pilt, rect)


def kuulide_joonistamine(aken, kuulid, põrked):
    for kuul in kuulid[:]:

        # eemaldada kokku põrganud kuulid
        if kuul in põrked.get("Kuul", []):
            kuulid.remove(kuul)
            continue

        # eemaldada kuulid, mis lendavad ekraani ülaosast kaugemale
        if kuul["y"] < 0:
            kuulid.remove(kuul)
            continue

        # kuuli joonistamine
        rect = kuuli_pilt.get_rect(topleft=(kuul["x"], kuul["y"]))
        aken.blit(kuuli_pilt, rect)
