#Projekti teema on avoider-mäng
#Autorid: Tuuli-Mia Haas ja Ulyana Galimova

import pygame, sys
from nupp import Nupp
import math
from pygame.math import Vector2
from pygame.event import  Event, EventType
from random import randint, choice
from pygame import font
from asteroid_ja_vaenlane import Asteroid, Vaenlane
from sätted import *
from mängija import Mängija
from kuul import Kuul

pygame.init()

aken = pygame.display.set_mode((AKEN_LAIUS, AKEN_KÕRGUS))

m_taust = pygame.image.load(MENÜÜ_TAUST)
taust = pygame.image.load(TAUST)
kell = pygame.time.Clock()
kell.tick(FPS) 

# Siin on mänguga seotud osad

def kattumise_lahendaja(*args:list) -> None:
    kõik_objektid = []
    for jada in args:
        kõik_objektid.extend(jada)

    for _ in range(3): #jooksutame mitu korda, sest et nihe oleks täpsem
        for i in range(len(kõik_objektid)):
            for j in range(i+1, len(kõik_objektid)):
                o1 = kõik_objektid[i]
                o2 = kõik_objektid[j]

                if o1.kokkupõrke_rect.colliderect(o2.kokkupõrke_rect):
                    #nihke suund
                    pos1 = Vector2(o1.x, o1.y)
                    pos2 = Vector2(o2.x, o2.y)
                    suund = pos1-pos2

                    if suund.length() == 0:
                        suund = Vector2(randint(-1,1), randint(-1, 1))

                    #jõustame nihke
                    nihe = suund.normalize() * 2
                    o1.x += nihe.x
                    o1.y += nihe.y
                    o2.x -= nihe.x
                    o2.y -= nihe.y
                    
                    o1.rect.center = (o1.x, o1.y)
                    o1.kokkupõrke_rect.center = (o1.x - KOKKUPÕRGE_RECT_LIIGE, o1.y - KOKKUPÕRGE_RECT_LIIGE)
                    
                    o2.rect.center = (o2.x, o2.y)
                    o2.kokkupõrke_rect.center = (o2.x - KOKKUPÕRGE_RECT_LIIGE, o2.y - KOKKUPÕRGE_RECT_LIIGE)

def kokkupõrke_lahendaja(kuulid: list, asteroidid:list, vaenlased:list, mängija = None) -> dict[str,list]:
    vastus = {"Kuul":[],"Mängija":[]}

    for kuul in kuulid[:]:
        for vaenlane in vaenlased[:]:
            if kuul.rect.colliderect(vaenlane.kokkupõrke_rect):
                #kui pihta saadud saab vaenlane lisatud vastusesse, punktide jaoks
                vastus["Kuul"].append(vaenlane)
                if vaenlane in vaenlased: vaenlased.remove(vaenlane)
                if kuul in kuulid: kuulid.remove(kuul)
                break

    if mängija:
        m_rect = getattr(mängija, "kokkupõrke_rect", mängija.rect)

        for oht in asteroidid + vaenlased:
            if m_rect.colliderect(oht.kokkupõrke_rect):
                vastus["Mängija"].append(oht)
    
    return vastus
    

def tekita_asteroide(asteroidid:list) -> None:
    x = randint(0, AKEN_LAIUS)
    r = choice(ASTEROIDI_SUURUSED)
    suund = Vector2(0,1)
    #Asteroidid normaliseeruvad vektoreid ise
    asteroidid.append(Asteroid(x, -50, r,suund))
    #kontrollime ikka et ei tekitanud nad üksteise peale
    kattumise_lahendaja(asteroidid)

def tekita_vaenlasi(vaenlased:list) -> None:
    x = randint(150, AKEN_LAIUS-150)
    suund = Vector2(0,1)
    vaenlased.append(Vaenlane(x, -50,suund))
    kattumise_lahendaja(vaenlased)

def vastaste_loogika(asteroidid:list,vaenlased:list) -> None:
    asteroidide_hulk = len(asteroidid)
    vaenlaste_hulk = len(vaenlased)

    if asteroidide_hulk < MIN_ASTEROIDIDE_ARV:
        tekita_asteroide(asteroidid)
    elif asteroidide_hulk >= MIN_ASTEROIDIDE_ARV and asteroidide_hulk < MAX_ASTEROIDIDE_ARV:
        if randint(0, 100) == 0:
            tekita_asteroide(asteroidid)

    if vaenlaste_hulk < MIN_VAENLASTE_ARV:
        tekita_vaenlasi(vaenlased)
    elif vaenlaste_hulk >= MIN_VAENLASTE_ARV and vaenlaste_hulk < MAX_VAENLASTE_ARV:
        if randint(0, 50) == 0:
            tekita_vaenlasi(vaenlased)
            
    for asteroid in asteroidid[:]:
        asteroid.asteroid_liikumine()
        if asteroid.y > ALUMINE_ÄÄR:
            asteroidid.remove(asteroid)

    for vaenlane in vaenlased[:]:
        vaenlane.vaenlane_liikumine()
        if vaenlane.y > ALUMINE_ÄÄR:
            vaenlased.remove(vaenlane)

#argumentideks nupuvajutused
def mängija_loogika(mängija, nupuvajutused:list[EventType],kuulid) -> None:
    mängija.liiguta(nupuvajutused)

    if nupuvajutused[pygame.K_SPACE]:
        mängija.tulista(kuulid)

def kuulide_loogika(kuulid) -> None:
    for kuul in kuulid[:]:
        kuul.liiguta()

        if kuul.y < 0:
            kuulid.remove(kuul)

def vastaste_joonistamine(asteroidid:list,vaenlased:list) -> None:

    for vaenlane in vaenlased:
        vaenlane.joonista_vaenlane(aken)
    for asteroid in asteroidid:
        asteroid.joonista_asteroid(aken)

def mängija_joonistamine(mängija) -> None:
    if mängija:
        mängija.joonista(aken)

def kuulide_joonistamine(kuulid) -> None:
   for kuul in kuulid:
       aken.blit(kuul.pilt, kuul.rect)

#Skoori ja edetabeliga seotud asjad
#Iga tabatud vaenlane annab ühe punkti
def punkti_koguja(põrked: dict[str, list], hetke_skoor: int) -> int:
    uued_punktid = len(põrked["Kuul"])
    return hetke_skoor + uued_punktid

def skoori_joonistamine(skoor,font) -> None:
    tekst = font.render(f"Skoor: {skoor}",True, pygame.Color(NUPUD))
    teksti_asukoht = tekst.get_rect(topleft=(0,0))
    aken.blit(tekst,teksti_asukoht)

def edetabel(uus_skoor:int) -> list:
    fail = "edetabel.txt"
    skoorid = []

    try:
        with open(fail, "r") as f:
            skoorid = [int(rida.strip()) for rida in f.readlines()]
    except (FileNotFoundError, ValueError):
        pass

    if uus_skoor not in skoorid:
        skoorid.append(uus_skoor)
        skoorid.sort(reverse=True)
        top_3 = skoorid[:3]

        with open(fail, "w") as f:
            for s in top_3:
                f.write(f"{s}\n")

        return top_3
    
    return skoorid[:3]

# Menüü ja vahelehtedega seotud osad

olek_praegu = "Stardi menüü" #See muutuja määrab, millline ekraan parasjagu ees on
valitud_tegelane = None

def get_font(suurus):
    return pygame.font.Font(FONT, suurus)

def j_main_menu(aken, menüü_hiir_pos):
    
    mängi_nupp = Nupp(pos=(370, 180), tekst_input="MÄNGI", font=get_font(30), värv="#d7fcd4", hover_värv="White", bg_värv=NUPU_BG_VÄRV, bg_hover=NUPU_BG_HOVER)
    edetabel_nupp = Nupp(pos=(370, 270), tekst_input="EDETABEL", font=get_font(30), värv="#d7fcd4", hover_värv="White", bg_värv=NUPU_BG_VÄRV, bg_hover=NUPU_BG_HOVER)
    quit_nupp = Nupp(pos=(370, 360), tekst_input="QUIT", font=get_font(30), värv="#d7fcd4", hover_värv="White", bg_värv=NUPU_BG_VÄRV, bg_hover=NUPU_BG_HOVER)

    aken.blit(m_taust, (0, 0))
    
    menüü_tekst = get_font(57).render("AvoiDER", True, "#b68f40")
    menüü_rect = menüü_tekst.get_rect(center=(381, 100))
    aken.blit(menüü_tekst, menüü_rect)

    for nupp in [mängi_nupp, edetabel_nupp, quit_nupp]:
        nupp.muudaVärvi(menüü_hiir_pos)
        nupp.update(aken)
        
    return mängi_nupp, edetabel_nupp, quit_nupp # Tagastame nupud sündmuste töötlemiseks

def j_mäng_ekraan(aken, mäng_hiir_pos):
    global valitud_tegelane
    
    aken.blit(taust, (0, 0))
    
    mäng_tekst = get_font(30).render("Vali tegelane", True, "White")
    mäng_rect = mäng_tekst.get_rect(center=(AKEN_LAIUS//2, 50))
    aken.blit(mäng_tekst, mäng_rect)

    nupud = []
    mängi = Nupp(pos=(AKEN_LAIUS-100, 30), tekst_input="MÄNGI", font=get_font(15), värv="Yellow", hover_värv="Red", bg_värv=NUPU_BG_VÄRV, bg_hover=NUPU_BG_HOVER)
    nupud += [mängi]
    mäng_tagasi = Nupp(pos=(100, 30), tekst_input="TAGASI", font=get_font(15), värv="Yellow", hover_värv="Red", bg_värv=NUPU_BG_VÄRV, bg_hover=NUPU_BG_HOVER) 
    nupud += [mäng_tagasi]

    x_start = (AKEN_LAIUS//2) - (400//2)
    y_pos = 250
    
    #nupp iga tegelase kohta järjest ühel joonel
    for nimi, andmed in TEGELASED.items():
        on_valitud = valitud_tegelane is not None and valitud_tegelane["pilt"] == andmed["pilt"]
        nupu_värv = "Yellow" if on_valitud else "White" 
        nupu_bg = NUPU_BG_HOVER if on_valitud else NUPU_BG_VÄRV

        tegelane = Nupp(pos=(x_start, y_pos),
                        tekst_input=nimi,
                        font=get_font(18),
                        värv=nupu_värv,
                        hover_värv=NUPUD_HOVER,
                        bg_värv=nupu_bg,
                        bg_hover=NUPU_BG_HOVER)
        nupud += [tegelane]
        x_start += 200

    for nupp in nupud:
        nupp.muudaVärvi(mäng_hiir_pos)
        nupp.update(aken)

    return nupud

def j_edetabel_ekraan(aken, edtabel_hiir_pos):
    aken.blit(taust, (0, 0))

    try:
        with open("edetabel.txt", "r") as fail:
            skoorid = [rida.strip() for rida in fail.readlines()]
    
    except FileNotFoundError:
        skoorid = []

    edetabel_tekst = get_font(40).render("EDETABEL TOP 3", True, "Gold")
    edetabel_rect = edetabel_tekst.get_rect(center=(368, 100))
    aken.blit(edetabel_tekst, edetabel_rect)

    y_asukoht = 180
    for i, s in enumerate(skoorid):
        tekst = get_font(30).render(f"{i+1}. koht: {s} punkti", True, "White")
        aken.blit(tekst, tekst.get_rect(center=(368, y_asukoht)))
        y_asukoht += 50

    edetabel_tagasi = Nupp(pos=(100, 30), tekst_input="TAGASI", font=get_font(15), värv="Yellow", hover_värv="Red", bg_värv=NUPU_BG_VÄRV, bg_hover=NUPU_BG_HOVER)
    edetabel_tagasi.muudaVärvi(edtabel_hiir_pos)
    edetabel_tagasi.update(aken)
    
    return edetabel_tagasi

def j_mäng_läbi_ekraan(aken, mäng_läbi_hiir_pos, skoor):
    #kõikide nende ilusate nupude ja info taustaks on kast + still frame mängust mis on selle kasti all
    kasti_laius, kasti_kõrgus = 450, 350
    taust_kast = pygame.Surface((kasti_laius, kasti_kõrgus), pygame.SRCALPHA)

    taust_kast.fill((NUPU_BG_VÄRV))

    kast_rect = taust_kast.get_rect(center=(AKEN_LAIUS//2, AKEN_KÕRGUS//2))
    aken.blit(taust_kast, kast_rect)

    pealkiri = get_font(40).render("MÄNG LÄBI", True, "Red")
    pealkiri_rect = pealkiri.get_rect(center=(AKEN_LAIUS//2, 120))

    skoor_tekst = get_font(30).render(f'Sinu skoor: {skoor}', True, "White")
    skoor_rect = skoor_tekst.get_rect(center=(AKEN_LAIUS//2, 200))

    aken.blit(pealkiri, pealkiri_rect)
    aken.blit(skoor_tekst, skoor_rect)

    #tagasi stardi menüü juurde
    menüü_nupp = Nupp(pos=(AKEN_LAIUS//2, AKEN_KÕRGUS//2 + 50), tekst_input="PEAMENÜÜ", font=get_font(30), värv="White", hover_värv="Yellow", bg_värv=NUPU_BG_VÄRV, bg_hover=NUPU_BG_HOVER)
    menüü_nupp.muudaVärvi(mäng_läbi_hiir_pos)
    menüü_nupp.update(aken)
    
    #tagasi mäng ekraani juurde
    mängi_uuesti = Nupp(pos=(AKEN_LAIUS//2, AKEN_KÕRGUS//2 + 120), tekst_input="MÄNGI UUESTI", font=get_font(30), värv="White", hover_värv="Yellow", bg_värv=NUPU_BG_VÄRV, bg_hover=NUPU_BG_HOVER)
    mängi_uuesti.muudaVärvi(mäng_läbi_hiir_pos)
    mängi_uuesti.update(aken)

    return menüü_nupp, mängi_uuesti


# SIIN ON MAAGIA: main game loop
def mäng():
    global olek_praegu
    global jookseb
    jookseb = True

    mängija = None
    kuulid = []
    asteroidid = []
    vaenlased = []
    skoor = 0
    edetabel_uuendatud = False
    mängu_font = get_font(20)


    while jookseb:

        menüü_hiir_pos = pygame.mouse.get_pos()

        # ---- MENÜÜDE JA MÄNGU EKRAANIKD ---

        #Joonistame vaid selle ekraani, mis vastab praegusele olekule
        #Seega vastavalt kontrollile

        if olek_praegu == "Stardi menüü":
            pygame.display.set_caption(AKNA_NIMI)
            mängi_nupp, edetabel_nupp, quit_nupp = j_main_menu(aken, menüü_hiir_pos)

        elif olek_praegu == "Mäng":
            pygame.display.set_caption(OLEK_MÄNG)
            valiku_nupud = j_mäng_ekraan(aken, menüü_hiir_pos)

        elif olek_praegu == "Edetabel":
            pygame.display.set_caption(OLEK_EDETABEL)
            edetabel_tagasi_nupp = j_edetabel_ekraan(aken, menüü_hiir_pos)

        #----- Kõige tähtsam olek sest siin lüüakse mäng käima

        elif olek_praegu == "Mängi":
            pygame.display.set_caption(OLEK_MÄNGI)

            if mängija:

                vastaste_loogika(asteroidid, vaenlased) 
                mängija_loogika(mängija, pygame.key.get_pressed(), kuulid)
                kuulide_loogika(kuulid)
                
                põrked = kokkupõrke_lahendaja(kuulid, asteroidid, vaenlased, mängija)
                skoor = punkti_koguja(põrked, skoor)
                
                #KONTROLL: kas ängija sai surma ?

                mängija_surm = len(põrked["Mängija"]) > 0
                vaenlane_möödas = any(v.y > ALUMINE_ÄÄR - 20 for v in vaenlased)
                
                if mängija_surm or vaenlane_möödas:
                    olek_praegu = "Mäng läbi"

                    if not edetabel_uuendatud:
                        edetabel_top = edetabel(skoor)
                        edetabel_uuendatud = True
                    

                # --- Joonistamine ---
                aken.blit(taust, (0, 0))
                vastaste_joonistamine(asteroidid, vaenlased)
                kuulide_joonistamine(kuulid)
                mängija_joonistamine(mängija)
                skoori_joonistamine(skoor, mängu_font)

            else:
                olek_praegu = "Mäng"

        # ------- Kui surm siis

        elif olek_praegu == "Mäng läbi":
            pygame.display.set_caption("MÄNG LÄBI")

            # jätame taustaks alles mängu, mis nüüd seisab
            aken.blit(taust, (0, 0))
            vastaste_joonistamine(asteroidid, vaenlased)
            kuulide_joonistamine(kuulid)
            mängija_joonistamine(mängija)
            skoori_joonistamine(skoor, mängu_font)
            
            #meil kaks varianti kas tagasi stardi menüü juurde või mängida uuesti, mis lihtsalt viib tagasi 
            # tegelast valima, ning siis mäng algab uuesti
            tagasi_menüüsse_nupp, mängi_uuesti_nupp = j_mäng_läbi_ekraan(aken, menüü_hiir_pos, skoor)


        #Sündmuste töötlemine
        #Käsitleme vastavalt olekule/mida vajutati, selle põhjal olek muutub

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if olek_praegu == "Stardi menüü":
                    if mängi_nupp.kontrollForInput(menüü_hiir_pos):
                        olek_praegu = "Mäng" # OLEKU MUUTUS
                    if edetabel_nupp.kontrollForInput(menüü_hiir_pos):
                        olek_praegu = "Edetabel" # OLEKU MUUTUS
                    if quit_nupp.kontrollForInput(menüü_hiir_pos):
                        pygame.quit()
                        sys.exit()


                # tegelase valiku juurest on võimalik tagasi saada kui ka edasi minna mängima
                elif olek_praegu == "Mäng":
                    for nupp in valiku_nupud:
                        if nupp.kontrollForInput(menüü_hiir_pos):
                            if nupp.tekst_input == "TAGASI":
                                global valitud_tegelane
                                valitud_tegelane = None
                                olek_praegu = "Stardi menüü" # TAGASI OLEKU MUUTUS
                                break

                            elif nupp.tekst_input == "MÄNGI":
                                #kui tegelast ei valitud siis võetakse default ja default on praegu meil esimene valik
                                # sest kosmoselaev on standard
                                if valitud_tegelane is None:
                                    valitud_tegelane = TEGELASED[list(TEGELASED.keys())[0]]
                                else:
                                    # kui valiti siis võetakse valik
                                    tegelane = valitud_tegelane

                                mängija = Mängija(368, 364, MÄNGIJA_KIIRUS, valitud_tegelane)
                                asteroidid, vaenlased, kuulid = [], [], []
                                skoor = 0
                                olek_praegu = "Mängi"
                                break

                            else:
                                valitud_tegelane = TEGELASED[nupp.tekst_input]


                elif olek_praegu == "Edetabel":
                    if edetabel_tagasi_nupp.kontrollForInput(menüü_hiir_pos):
                        olek_praegu = "Stardi menüü" # TAGASI OLEKU MUUTUS

                elif olek_praegu == "Mäng läbi":
                    if tagasi_menüüsse_nupp.kontrollForInput(menüü_hiir_pos):
                        olek_praegu = "Stardi menüü"
                        mängija = None
                        skoor = 0
                    
                    if mängi_uuesti_nupp.kontrollForInput(menüü_hiir_pos):
                        olek_praegu = "Mäng"
                        mängija = None
                        skoor = 0
                        viimane_spawn = pygame.time.get_ticks()
                        spawn_viivitus = 2000
                        edetabel_uuendatud = False


        pygame.display.update()
        kell.tick(FPS)

mäng() #see rida siin laseb meil kõike seda näha
