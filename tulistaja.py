import pygame
from sätted import AKEN_LAIUS, ÜLEMINE_ÄÄR

bullet_speed = 10
bullet_width = 4
bullet_height = 8

mängija_pilt = pygame.image.load("pildid/tulistaja.png")
mängija_pilt = pygame.transform.smoothscale(mängija_pilt, (30, 30))

kuuli_pilt = pygame.image.load("pildid/bullet1.png")
kuuli_pilt = pygame.transform.smoothscale(kuuli_pilt, (bullet_width, bullet_height))


def mängija_loogika(nupuvajutused, kuulid, mängija):
    for event in nupuvajutused:
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                if mängija["x"] - mängija["size"] // 2 > 0:
                    mängija["x"] -= 5

            if event.key == pygame.K_RIGHT:
                if mängija["x"] + mängija["size"] // 2 < AKEN_LAIUS:
                    mängija["x"] += 5

            if event.key == pygame.K_SPACE:
                kuulid.append([
                    mängija["x"] - bullet_width // 2,
                    mängija["y"] - mängija["size"],
                    bullet_width,
                    bullet_height
                ])


def kuulide_loogika(kuulid):
    for kuul in kuulid[:]:
        kuul[1] -= bullet_speed
        if kuul[1] < 0:
            kuulid.remove(kuul)


def mängija_joonistamine(aken, mängija):
    rect = mängija_pilt.get_rect(center=(mängija["x"], mängija["y"]))
    aken.blit(mängija_pilt, rect)


def kuulide_joonistamine(aken, kuulid, põrked):
    for kuul in kuulid[:]:

        # eemaldada kokku põrganud kuulid
        if kuul in põrked.get["Kuul", []]:
            kuulid.remove(kuul)
            continue

        # eemaldada kuulid, mis lendavad ekraani ülaosast kaugemale
        if kuul[1] < ÜLEMINE_ÄÄR:
            kuulid.remove(kuul)
            continue

        # kuuli joonistamine
        rect = kuuli_pilt.get_rect(topleft=(kuul[0], kuul[1]))
        aken.blit(kuuli_pilt, rect)
