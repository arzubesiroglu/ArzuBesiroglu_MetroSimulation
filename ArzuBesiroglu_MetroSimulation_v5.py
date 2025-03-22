# Gerekli kütüphaneleri içe aktar

import logging
from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional

# ANSI Renk Kodları (Terminalde durakları renklerine göre ayırmak için)
RENKLER = {
    "Kırmızı Hat": "\033[91m",  # Kırmızı
    "Mavi Hat":    "\033[94m",  # Mavi
    "Turuncu Hat": "\033[93m",  # Turuncu
    "Varsayılan":  "\033[0m"     # Varsayılan renk
}
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class Istasyon:
    """Metro istasyonlarını temsil eden sınıf."""
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        """İstasyona bir komşu ekler."""
        self.komsular.append((istasyon, sure))

    def renkli_ad(self):
        """İstasyon adını hattının rengine göre renklendirir."""
        renk = RENKLER.get(self.hat, RENKLER["Varsayılan"])
        return f"{renk}{self.ad}{RENKLER['Varsayılan']}"

class MetroAgi:
    """Metro ağı sınıfı. İstasyonları ve bağlantıları yönetir."""
    def __init__(self):
        self.istasyonlar: Dict[str, List[Istasyon]] = defaultdict(list)
        self._counter = 0

    def istasyon_ekle(self, idx: str, ad: str, hat: str):
        """Yeni bir istasyon ekler."""
        ist = Istasyon(idx, ad, hat)
        self.istasyonlar[ad].append(ist)
        logging.info(f"İstasyon eklendi: {ist.renkli_ad()} ({hat})")

    def baglanti_ekle(self, id1: str, id2: str, sure: int):
        """İki istasyon arasında çift yönlü bağlantı kurar."""
        all_ist = sum(self.istasyonlar.values(), [])
        i1 = next(i for i in all_ist if i.idx == id1)
        i2 = next(i for i in all_ist if i.idx == id2)
        i1.komsu_ekle(i2, sure)
        i2.komsu_ekle(i1, sure)
        logging.info(f"Bağlantı eklendi: {i1.renkli_ad()} ↔ {i2.renkli_ad()} ({sure} dk)")

    def en_az_aktarma_bul(self, bas: Istasyon, hedef: Istasyon) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur."""
        queue = deque([(bas, [bas])])
        visited = {bas}
        while queue:
            curr, path = queue.popleft()
            if curr == hedef:
                logging.info(f"En az aktarmalı rota bulundu: {' -> '.join(i.renkli_ad() for i in path)}")
                return path
            for nbr, _ in curr.komsular:
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append((nbr, path + [nbr]))
        logging.warning("Rota bulunamadı!")
        return None

    def en_hizli_rota_bul(self, bas: Istasyon, hedef: Istasyon) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur."""
        pq = []
        self._counter = 0
        heapq.heappush(pq, (0, self._counter, bas, [bas]))
        visited = set()
        while pq:
            cost, _, curr, path = heapq.heappop(pq)
            if curr == hedef:
                logging.info(f"En hızlı rota bulundu ({cost} dk): {' -> '.join(i.renkli_ad() for i in path)}")
                return path, cost
            if curr in visited:
                continue
            visited.add(curr)
            for nbr, t in curr.komsular:
                if nbr not in visited:
                    self._counter += 1
                    heapq.heappush(pq, (cost + t, self._counter, nbr, path + [nbr]))
        logging.warning("Rota bulunamadı!")
        return None

    def format_rota(self, rota: List[Istasyon]) -> str:
        """Rotayı renkli formatta döndürür."""
        return " -> ".join(i.renkli_ad() for i in rota)

def temizle_rota(rota: List[Istasyon]) -> List[Istasyon]:
    """Ardışık aynı durak isimlerini temizler."""
    return [s for prev, s in zip([None] + rota, rota) if prev is None or s.ad != prev.ad]

def terminal_menusu(metro: MetroAgi):
    """Kullanıcıya interaktif terminal menüsü sunar."""
    while True:
        print("\n🚇 Metro Simülasyonu Başlatıldı! 🚇\n")
        stations = sorted(metro.istasyonlar.keys())
        for i, name in enumerate(stations, 1):
            print(f"{i} - {name}")
        try:
            b = int(input("\n🔹 Başlangıç seç: ")) - 1
            bas = metro.istasyonlar[stations[b]][0]
            h = int(input("🔹 Hedef seç: ")) - 1
            hedef = metro.istasyonlar[stations[h]][0]
        except Exception:
            print("\n⚠️ Geçersiz seçim, tekrar deneyin!\n")
            continue

        r1 = metro.en_az_aktarma_bul(bas, hedef)
        if r1:
            r1 = temizle_rota(r1)
            print("\n🛤️ En Az Aktarmalı:", metro.format_rota(r1))
        r2 = metro.en_hizli_rota_bul(bas, hedef)
        if r2:
            rota, sure = r2
            rota = temizle_rota(rota)
            print(f"\n⏱️ En Hızlı ({sure} dk):", metro.format_rota(rota))
        if input("\nYeni rota? (e/h): ").lower() != "e":
            print("\n🚆 İyi yolculuklar! 🚆")
            break

if __name__ == '__main__':
    metro = MetroAgi()
    data = [
        ("K1", "Kızılay", "Kırmızı Hat"),
        ("K2", "Ulus", "Kırmızı Hat"),
        ("K3", "Demetevler", "Kırmızı Hat"),
        ("K4", "OSB", "Kırmızı Hat"),
        ("M1", "AŞTİ", "Mavi Hat"),
        ("M2", "Kızılay", "Mavi Hat"),
        ("M3", "Sıhhıye", "Mavi Hat"),
        ("M4", "Gar", "Mavi Hat"),
        ("T1", "Batıkent", "Turuncu Hat"),
        ("T2", "Demetevler", "Turuncu Hat"),
        ("T3", "Gar", "Turuncu Hat"),
        ("T4", "Keçiören", "Turuncu Hat")
    ]
    for idx, ad, hat in data:
        metro.istasyon_ekle(idx, ad, hat)

    con = [
        ("K1", "K2", 4), ("K2", "K3", 6), ("K3", "K4", 8),
        ("M1", "M2", 5), ("M2", "M3", 3), ("M3", "M4", 4),
        ("T1", "T2", 7), ("T2", "T3", 9), ("T3", "T4", 5),
        ("K1", "M2", 2), ("K3", "T2", 3), ("M4", "T3", 2),
        ("K3", "M2", 10), ("K2", "T2", 12), ("M3", "T3", 15)
    ]
    for a, b, s in con:
        metro.baglanti_ekle(a, b, s)

    terminal_menusu(metro)

