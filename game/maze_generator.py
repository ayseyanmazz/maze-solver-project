import random

def labirent_uret(satir=31, sutun=31):
    matris = [[1 for _ in range(sutun)] for _ in range(satir)]

    baslangic = (1, 1)
    matris[1][1] = 0

    stack = [baslangic]
    ziyaret_edilen = {baslangic}

    # TREE yapısı: child -> parent
    parent = {
        baslangic: None
    }

    yonler = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        r, c = stack[-1]

        komsular = []

        for dr, dc in yonler:
            nr = r + dr
            nc = c + dc

            if 1 <= nr < satir - 1 and 1 <= nc < sutun - 1:
                if (nr, nc) not in ziyaret_edilen:
                    komsular.append((nr, nc, dr, dc))

        if komsular:
            nr, nc, dr, dc = random.choice(komsular)

            # Duvarı kır
            matris[r + dr // 2][c + dc // 2] = 0
            matris[nr][nc] = 0

            ziyaret_edilen.add((nr, nc))
            stack.append((nr, nc))

            # TREE bağlantısı
            parent[(nr, nc)] = (r, c)

        else:
            stack.pop()

    return matris, parent