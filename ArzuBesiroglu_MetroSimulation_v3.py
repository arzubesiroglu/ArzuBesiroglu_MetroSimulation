# Gerekli kütüphaneleri içe aktar

import logging
from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional

# Loglama ayarları – DEBUG seviyesine ayarlarsanız tüm adım adım loglar görünür
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class Istasyon:
    """
    Metro istasyonlarını temsil eden sınıf.
    Her istasyonun bir ID'si, adı ve bağlı olduğu hattı vardır.
    """
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        """İstasyona bir komşu ekler."""
        self.komsular.append((istasyon, sure))

    def __lt__(self, other):
        # heapq için tie‑breaker
        return self.idx < other.idx

class MetroAgi:
    """
    Metro ağı sınıfı: istasyonları ve bağlantıları tutar,
    en az aktarmalı ve en hızlı rotaları hesaplar.
    """
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        """Yeni bir istasyon ekler."""
        if idx not in self.istasyonlar:
            ist = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = ist
            self.hatlar[hat].append(ist)
            logging.info(f"İstasyon eklendi: {ad} ({hat}) [ID={idx}]")

    def baglanti_ekle(self, id1: str, id2: str, sure: int) -> None:
        """İki istasyon arasında çift yönlü bağlantı kurar."""
        i1 = self.istasyonlar[id1]
        i2 = self.istasyonlar[id2]
        i1.komsu_ekle(i2, sure)
        i2.komsu_ekle(i1, sure)
        logging.info(f"Bağlantı eklendi: {i1.ad} ↔ {i2.ad} ({sure} dk)")

    def en_az_aktarma_bul(self, bas_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """
        BFS kullanarak EN AZ aktarmalı rotayı bulur.
        Kuyruk elemanı: (istasyon, rota_listesi, aktarma_sayısı, mevcut_hat)
        """
        if bas_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            logging.error("Geçersiz istasyon ID")
            return None

        bas = self.istasyonlar[bas_id]
        hedef = self.istasyonlar[hedef_id]
        queue = deque([(bas, [bas], 0, bas.hat)])
        visited = {(bas.idx, bas.hat)}

        while queue:
            current, path, transfers, curr_hat = queue.popleft()
            if current.idx == hedef.idx:
                logging.info(f"[BFS] Rota bulundu (aktarma={transfers}): {' -> '.join(i.ad for i in path)}")
                return path

            for nbr, _ in current.komsular:
                new_transfers = transfers + (nbr.hat != curr_hat)
                state = (nbr.idx, nbr.hat)
                if state not in visited:
                    visited.add(state)
                    queue.append((nbr, path + [nbr], new_transfers, nbr.hat))

        logging.warning("[BFS] Rota bulunamadı")
        return None

    def en_hizli_rota_bul(self, bas_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """
        A* algoritması kullanarak en hızlı rotayı bulur.
        """
        if bas_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            logging.error("Geçersiz istasyon ID")
            return None

        bas = self.istasyonlar[bas_id]
        hedef = self.istasyonlar[hedef_id]
        def heuristic(ist): return 5 if ist.hat != hedef.hat else 0

        pq = [(heuristic(bas), 0, id(bas), bas, [bas])]
        gScore = {bas: 0}
        visited = set()

        while pq:
            _, g, _, current, path = heapq.heappop(pq)
            if current == hedef:
                logging.info(f"[A*] Rota bulundu ({g} dk): {' -> '.join(i.ad for i in path)}")
                return path, g
            if current in visited:
                continue
            visited.add(current)
            for nbr, cost in current.komsular:
                ng = g + cost
                if nbr not in gScore or ng < gScore[nbr]:
                    gScore[nbr] = ng
                    heapq.heappush(pq, (ng + heuristic(nbr), ng, id(nbr), nbr, path + [nbr]))

        logging.warning("[A*] Rota bulunamadı")
        return None

def temizle_rota(rota: List[Istasyon]) -> List[Istasyon]:
    """Ardışık aynı durak isimlerini temizler."""
    return [s for prev, s in zip([None] + rota, rota) if prev is None or s.ad != prev.ad]

if __name__ == '__main__':
    metro = MetroAgi()

    # Örnek veri ekleme
    metro.istasyon_ekle("K1","Kızılay","Kırmızı Hat")
    metro.istasyon_ekle("M1","AŞTİ","Mavi Hat")
    metro.baglanti_ekle("K1","M1",2)

    print("\n=== Test Senaryoları ===")
    for start, end in [("K1","M1")]:
        rota = metro.en_az_aktarma_bul(start,end)
        if rota:
            rota = temizle_rota(rota)
            print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        sonuc = metro.en_hizli_rota_bul(start,end)
        if sonuc:
            rota, sure = sonuc
            rota = temizle_rota(rota)
            print(f"En hızlı rota ({sure} dk):", " -> ".join(i.ad for i in rota))
