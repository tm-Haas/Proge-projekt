#Projekti teema on avoider-mäng
#Autorid: Tuuli-Mia Haas ja Ulyana Galimova

import pygame
from pygame.math import Vector2
from pygame.event import  Event, EventType
from random import randint, choice
from pygame import font
from asteroidid_ja_vaenlased import Asteroid, Vaenlane
from sätted import *

#TO-DO: Start menüü, suremismenüü: ehk paar nuppu ja ilusad pildid
#vb ka hääli
#...ja 99% koodist


# Initialize Pygame
pygame.init()
# Set up the game window
aken = pygame.display.set_mode((AKEN_LAIUS, AKEN_KÕRGUS))
pygame.display.set_caption(AKNA_NIMI)
kell = pygame.time.Clock()

def mängu_kinnipaneku_kontroll(event: EventType) -> None:
    if event.type == pygame.QUIT:
            global jookseb
            jookseb = False

#TO-DO: selle funktsiooni eesmärk on mitte lasta objektide kokkupõrke_rektid olla üksteise sees siis kui nad sisse tekivad
#muidu nad panevad hullu ja lendu
#Peamiselt asteroidide ja vaenlaste jaoks
#Muudab asukohti ise ja ei tagasta midagi
#Muudab normaalvektorite suunas paar pikslit
#Parima efekti jaoks jooksutada funktsiooni mitu korda
def kattumise_lahendaja(*args:list) -> None:
    for jada in args:
        pass

#TO-DO: selle funktsiooni eesmärk on kontrollida millal teatud tähtsad objektid on kokkupõrkel
#Nendeks oleksid siis: Kuulid + vaenlased ja asteroidid. Mängija + vaenlased ja asteroidid.
#See on üldine funktsioon ja tagastasb kes põrkus kokku kellega sõnastiku vormis

def kokkupõrke_lahendaja(*args:list, mängija = None) -> dict[str,list]:
    vastus = {"Kuul":[],"Mängija":[]}
    for jada in args:
        pass
    return vastus


#Puntkid! 
def punkti_koguja(sõnastik:dict[str,list],skoor) -> int:
    skoor += len(list(filter(lambda x: type(x) != Asteroid,sõnastik["Kuul"])))
    return skoor

def tekita_asteroide(asteroidid:list) -> None:
    x = randint(0, AKEN_LAIUS)
    r = choice(ASTEROIDI_SUURUSED)
    suund = Vector2(0,1)
    #Asteroidid normaliseeruvad vektoreid ise
    asteroidid.append(Asteroid(x, -50, r,suund))
    #kontrollime ikka et ei tekitanud nad üksteise peale
    kattumise_lahendaja(asteroidid)

def tekita_vaenlasi(vaenlased:list) -> None:
    x = randint(0, AKEN_LAIUS)
    suund = Vector2(0,1)
    vaenlased.append(Vaenlane(x, -50,suund))
    kattumise_lahendaja(vaenlased)

def vastaste_loogika(asteroidid:list,vaenlased:list) -> None:
    asteroidide_hulk = len(asteroidid)
    vaenlaste_hulk = len(vaenlased)
    # TO-DO: teha seda huvitavamaks, praegu on täiesti suvalise tekitamisloogikaga ja asukohtadega
    # samuti tuleb arvestada vaenlaste ja asteroidide suurustega, et nad ei kattuks teineteisega
    # selleks on vist tark kasutada rect.collidelistall()
    # LISAKS peab tegema nii et vaenlased ei saaks tekkida asteroidide taga, või kui tekivad, siis omaksid suunda mis laseks neil
    # mööda saada. Selleks saab kasutada ajutist kontrollkasti mis ulatub ekraani lõpuni ning otsib kas tema all asub asteroid, kui jah, siis nt ei lase vaenlasel tekkida.
    if asteroidide_hulk < MIN_ASTEROIDIDE_ARV:
        tekita_asteroide(asteroidid)
    elif asteroidide_hulk > MIN_ASTEROIDIDE_ARV and asteroidide_hulk < MAX_ASTEROIDIDE_ARV:
        if randint(0, 50) == 0:
            tekita_asteroide(asteroidid)

    if vaenlaste_hulk < MIN_VAENLASTE_ARV:
        tekita_vaenlasi(vaenlased)
    elif vaenlaste_hulk > MIN_VAENLASTE_ARV and vaenlaste_hulk < MAX_VAENLASTE_ARV:
        if randint(0, 50) == 0:
            tekita_vaenlasi(vaenlased)

            


    #Tegeleb asteroidide liigutamisega ja hävitab neid kui jõuavad ekraani lõppu
    for asteroid in asteroidid[:]:
        asteroid.asteroid_liikumine()
        if asteroid.y > ALUMINE_ÄÄR:
            asteroidid.remove(asteroid)

    for vaenlane in vaenlased[:]:
        vaenlane.vaenlane_liikumine()
        if vaenlane.y > ALUMINE_ÄÄR:
            vaenlased.remove(vaenlane)


#Eeldan et argumentideks tulevad nupuvajutused
def mängija_loogika(nupuvajutused:list[EventType],kuulid) -> None:
    #tantsib ringi teeb asju ja laseb kuule
    pass

def kuulide_loogika(kuulid) -> None:
    pass

def vastaste_joonistamine(asteroidid:list,vaenlased:list) -> None:

    for vaenlane in vaenlased:
        vaenlane.joonista_vaenlane(aken)
    for asteroid in asteroidid:
        asteroid.joonista_asteroid(aken)

def mängija_joonistamine(mängija) -> None:
    #aken.blit(pilt, rect)
    pass

def kuulide_joonistamine(mängija,põrked) -> None:
    #eeldan et nad lendavad suht ääreni
    #selleks on ÜLEMINE_ÄÄR konstant
    #samuti hävitada need kuulid kes on kellegagi kokku põrganud
    #aken.blit(pilt, rect)
    pass

def skoori_joonistamine(skoor,font) -> None:
    #Font on comic sans ;)
    tekst = font.render(f"Vaenlasi kõmmutatud: {skoor}",True, pygame.Color(FONT_VÄRV))
    teksti_asukoht = tekst.get_rect(topleft=(0,0))
    aken.blit(tekst,teksti_asukoht)
# Game loop
def mäng() -> None:
    mängija = None
    kuulid = []
    asteroidid = []
    vaenlased = []
    global jookseb
    jookseb = True
    skoor = 0
    font = pygame.font.Font(FONT,64)
    while jookseb:
        #iga raam ikka uued nupuvajutused meil
        nupuvajutused = []

        for event in pygame.event.get():
            mängu_kinnipaneku_kontroll(event)
     
        vastaste_loogika(asteroidid,vaenlased)
        kattumise_lahendaja(asteroidid,vaenlased) #just in case
        mängija_loogika(nupuvajutused,kuulid)
        kuulide_loogika(kuulid)
        põrked = kokkupõrke_lahendaja(kuulid,asteroidid,vaenlased,mängija = mängija)
        skoor += punkti_koguja(põrked,skoor)

        # Ennem seda tuleb mänguloogika
        aken.fill(pygame.Color(VÄRSKENDUSVÄRV)) #Teeb puhta lehe mille peale saab joonistada
        # Pärast seda tuleb kaardile joonistamine

        kuulide_joonistamine(kuulid,põrked)
        vastaste_joonistamine(asteroidid,vaenlased)
        mängija_joonistamine(mängija)
        skoori_joonistamine(skoor,font)

        #kas tal on elu? vist mitte
        if "Mängija" in põrked.keys():
            break #you lost!!!!!

        pygame.display.flip()
        
        kell.tick(FPS)



mäng()
# Quit Pygame
pygame.quit()
