import pygame
import time

from maze_generator import labirent_uret
from solver import en_kisa_yolu_bul
from renderer import labirenti_ciz
from renderer import cozum_yolunu_ciz

pygame.init()

HUCRE_BOYUTU = 25
OFFSET_Y = 40

font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

cozumu_goster = False
animasyon_index = 0
animasyon_hizi = 1


def yeni_labirent_olustur(boyut):
    global matris
    global yol
    global cozum_suresi
    global ekran
    global satir
    global sutun
    global EKRAN_GENISLIK
    global EKRAN_YUKSEKLIK
    global cozumu_goster
    global animasyon_index
    global tree_parent

    matris, tree_parent = labirent_uret(boyut, boyut)   
    baslama_zamani = time.time()
    yol = en_kisa_yolu_bul(matris)
    bitis_zamani = time.time()

    cozum_suresi = bitis_zamani - baslama_zamani

    satir = len(matris)
    sutun = len(matris[0])

    EKRAN_GENISLIK = sutun * HUCRE_BOYUTU
    EKRAN_YUKSEKLIK = satir * HUCRE_BOYUTU + OFFSET_Y

    ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK))
    pygame.display.set_caption("Maze Project")

    cozumu_goster = False
    animasyon_index = 0


yeni_labirent_olustur(31)

calisiyor = True

while calisiyor:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            calisiyor = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                yeni_labirent_olustur(31)

            elif event.key == pygame.K_SPACE:
                cozumu_goster = not cozumu_goster

                if cozumu_goster:
                    animasyon_index = 0

            elif event.key == pygame.K_1:
                yeni_labirent_olustur(21)

            elif event.key == pygame.K_2:
                yeni_labirent_olustur(31)

            elif event.key == pygame.K_3:
                yeni_labirent_olustur(41)
            elif event.key == pygame.K_UP:

                animasyon_hizi += 1

                if animasyon_hizi > 10:
                    animasyon_hizi = 10

            elif event.key == pygame.K_DOWN:

                animasyon_hizi -= 1

                if animasyon_hizi < 1:
                    animasyon_hizi = 1    
                

    ekran.fill((0, 0, 0))

    labirenti_ciz(ekran, matris, HUCRE_BOYUTU)

    if cozumu_goster:
        animasyon_index += 1
        animasyon_index += animasyon_hizi

        if animasyon_index > len(yol):
            animasyon_index = len(yol)

        cozum_yolunu_ciz(
            ekran,
            yol[:animasyon_index],
            HUCRE_BOYUTU
        )

    bilgi_yazisi = font.render(
        f"Yol: {len(yol)} | Sure: {cozum_suresi:.5f} sn | Hiz: {animasyon_hizi} | R: Yeni | SPACE: Cozum | 1-2-3: Boyut",
        True,
        (255, 255, 0)
    )
    
    ekran.blit(bilgi_yazisi, (10, 10))

    start_yazi = font.render("START", True, (0, 255, 0))
    end_yazi = font.render("END", True, (0, 0, 255))

    ekran.blit(start_yazi, (5, OFFSET_Y + 5))

    ekran.blit(
        end_yazi,
        (
            (sutun - 4) * HUCRE_BOYUTU,
            (satir - 2) * HUCRE_BOYUTU + OFFSET_Y + 5
        )
    )

    pygame.display.update()
    clock.tick(60)

pygame.quit()