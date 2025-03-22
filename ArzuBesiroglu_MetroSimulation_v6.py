# Gerekli kütüphaneleri içe aktar
import logging
from collections import defaultdict, deque
import heapq
import time
from typing import Dict, List, Tuple, Optional

# ANSI renk kodları
RENKLER = {"Kırmızı Hat": "\033[91m", "Mavi Hat": "\033[94m", "Turuncu Hat": "\033[93m", "Varsayılan": "\033[0m"}
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx; self.ad = ad; self.hat = hat; self.komsular: List[Tuple['Istasyon', int]] = []
    def komsu_ekle(self, istasyon, sure): self.komsular.append((istasyon, sure))
    def renkli_ad(self): return f"{RENKLER.get(self.hat)}{self.ad}{RENKLER['Varsayılan']}"

class MetroAgi:
    def __init__(self): self.istasyonlar: Dict[str, List[Istasyon]] = defaultdict(list); self._count = 0
    def istasyon_ekle(self, idx, ad, hat):
        ist = Istasyon(idx, ad, hat); self.istasyonlar[ad].append(ist); logging.info(f"Eklendi: {ist.renkli_ad()} ({hat})")
    def baglanti_ekle(self, id1, id2, sure):
        all_ist = sum(self.istasyonlar.values(), []);
        i1 = next(i for i in all_ist if i.idx == id1);
        i2 = next(i for i in all_ist if i.idx == id2);
        i1.komsu_ekle(i2, sure); i2.komsu_ekle(i1, sure);
        logging.info(f"Bağlantı: {i1.renkli_ad()} ↔ {i2.renkli_ad()} ({sure}dk)")
    def en_az_aktarma_bul(self, bas, hedef):
        queue = deque([(bas, [bas])]); visited = {bas}
        while queue:
            curr, path = queue.popleft()
            if curr == hedef: return path
            for nbr, _ in curr.komsular:
                if nbr not in visited:
                    visited.add(nbr); queue.append((nbr, path + [nbr]))
        return None
    def en_hizli_rota_bul(self, bas, hedef):
        pq = []; self._count = 0
        heapq.heappush(pq, (0, self._count, bas, [bas])); visited = set()
        while pq:
            cost, _, curr, path = heapq.heappop(pq)
            if curr == hedef: return path, cost
            if curr in visited: continue
            visited.add(curr)
            for nbr, t in curr.komsular:
                if nbr not in visited:
                    self._count += 1; heapq.heappush(pq, (cost + t, self._count, nbr, path + [nbr]))
        return None
    def format_rota(self, rota): return " -> ".join(i.renkli_ad() for i in rota)


def animate_train(distance=30, delay=0.05):
    print("\nAnimasyon başlıyor...")
    for pos in range(distance):
        print(' ' * pos + '🚆', end='\r', flush=True)
        time.sleep(delay)
    print()

if __name__ == '__main__':
    metro = MetroAgi()
    data = [
        ('K1','Kızılay','Kırmızı Hat'),('K2','Ulus','Kırmızı Hat'),('K3','Demetevler','Kırmızı Hat'),('K4','OSB','Kırmızı Hat'),
        ('M1','AŞTİ','Mavi Hat'),('M2','Kızılay','Mavi Hat'),('M3','Sıhhıye','Mavi Hat'),('M4','Gar','Mavi Hat'),
        ('T1','Batıkent','Turuncu Hat'),('T2','Demetevler','Turuncu Hat'),('T3','Gar','Turuncu Hat'),('T4','Keçiören','Turuncu Hat')
    ]
    for idx, ad, hat in data: metro.istasyon_ekle(idx, ad, hat)
    con = [
        ('K1','K2',4),('K2','K3',6),('K3','K4',8),('M1','M2',5),('M2','M3',3),('M3','M4',4),
        ('T1','T2',7),('T2','T3',9),('T3','T4',5),('K1','M2',2),('K3','T2',3),('M4','T3',2)
    ]
    for a, b, s in con: metro.baglanti_ekle(a, b, s)

    while True:
        print("\n" + "─" * 70)
        print("🚆 Lütfen gitmek istediğiniz durağın numarasını seçiniz:")
        names = sorted(metro.istasyonlar.keys())
        for i, n in enumerate(names, 1): print(f"{i}. {n}")
        try:
            b = int(input('🔹 Başlangıç numarası: ')) - 1
            h = int(input('🔹 Hedef numarası: ')) - 1
            print("\n" + "─" * 70)
        except ValueError:
            print("⚠️ Lütfen geçerli bir sayı giriniz!")
            continue
        if b < 0 or b >= len(names) or h < 0 or h >= len(names):
            print("⚠️ Geçersiz seçim, lütfen listede gösterilen numaraları girin!")
            continue
        bas = metro.istasyonlar[names[b]][0]; hedef = metro.istasyonlar[names[h]][0]
        az = metro.en_az_aktarma_bul(bas, hedef)
        if az:
            print('🛤️ En Az Aktarmalı:', metro.format_rota(az))
        hiz, sure = metro.en_hizli_rota_bul(bas, hedef) or (None, None)
        if hiz:
            print(f'⏱️ En Hızlı ({sure} dk):', metro.format_rota(hiz))
        animate_train()
        if input('Yeni rota? (e/h): ').lower() != 'e': break
    print('🚆 İyi yolculuklar! 🚆')
