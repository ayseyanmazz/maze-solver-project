import pygame

OFFSET_Y = 40

def labirenti_ciz(ekran, matris, hucre_boyutu):

    satir_sayisi = len(matris)
    sutun_sayisi = len(matris[0])

    for r in range(satir_sayisi):
        for c in range(sutun_sayisi):

            if matris[r][c] == 1:
                renk = (0, 0, 0)
            else:
                renk = (255, 255, 255)

            pygame.draw.rect(
                ekran,
                renk,
                (
                    c * hucre_boyutu,
                    r * hucre_boyutu + OFFSET_Y,
                    hucre_boyutu,
                    hucre_boyutu
                )
            )

    pygame.draw.rect(
        ekran,
        (0, 255, 0),
        (
            1 * hucre_boyutu,
            1 * hucre_boyutu + OFFSET_Y,
            hucre_boyutu,
            hucre_boyutu
        )
    )

    pygame.draw.rect(
        ekran,
        (0, 0, 255),
        (
            (sutun_sayisi - 2) * hucre_boyutu,
            (satir_sayisi - 2) * hucre_boyutu + OFFSET_Y,
            hucre_boyutu,
            hucre_boyutu
        )
    )


def cozum_yolunu_ciz(ekran, yol, hucre_boyutu):

    noktalar = []

    for r, c in yol:

        x = c * hucre_boyutu + hucre_boyutu // 2
        y = r * hucre_boyutu + hucre_boyutu // 2 + OFFSET_Y

        noktalar.append((x, y))

    if len(noktalar) > 1:
        pygame.draw.lines(
            ekran,
            (255, 0, 0),
            False,
            noktalar,
            5
        )