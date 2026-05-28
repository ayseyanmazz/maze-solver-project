from collections import deque

def en_kisa_yolu_bul(matris):
    satir_sayisi = len(matris)
    sutun_sayisi = len(matris[0])

    baslangic = (1, 1)
    bitis = (satir_sayisi - 2, sutun_sayisi - 2)

    kuyruk = deque()
    kuyruk.append((baslangic, [baslangic]))

    ziyaret_edilen = set()
    ziyaret_edilen.add(baslangic)

    yonler = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while kuyruk:
        (r, c), yol = kuyruk.popleft()

        if (r, c) == bitis:
            return yol

        for dr, dc in yonler:
            yeni_r = r + dr
            yeni_c = c + dc

            if 0 <= yeni_r < satir_sayisi and 0 <= yeni_c < sutun_sayisi:
                if matris[yeni_r][yeni_c] == 0 and (yeni_r, yeni_c) not in ziyaret_edilen:
                    ziyaret_edilen.add((yeni_r, yeni_c))
                    kuyruk.append(((yeni_r, yeni_c), yol + [(yeni_r, yeni_c)]))

    return []