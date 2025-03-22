# ArzuBesiroglu_MetroSimulation.py
# Terminal tabanlı Metro Rota Planlayıcı (Final Versiyon)
# BFS ve A* algoritmaları ile rota optimizasyonu

# Gerekli kütüphaneleri içe aktar
import logging
from collections import defaultdict, deque
import heapq
import time
from typing import Dict, List, Tuple, Optional

# Terminalde renkli çıktı için ANSI renk kodları
RENKLER = {
    "Kırmızı Hat": "\033[91m",    # Kırmızı
    "Mavi Hat":    "\033[94m",    # Mavi
    "Turuncu Hat": "\033[93m",    # Turuncu
    "Varsayılan":  "\033[0m"     # Renk sıfırlama
}

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class Istasyon:
    """
    Metro istasyonlarını temsil eden sınıf.
    Her istasyonun bir ID'si, adı ve bağlı olduğu hattı vardır.
    Aynı isimde birden fazla istasyon (aktarma) olabilir.
    """
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (komşu istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon, sure):
        """İstasyona bir komşu bağlantısı ekler."""
        self.komsular.append((istasyon, sure))

    def renkli_ad(self):
        """Hattına göre renkli istasyon adı döndürür."""
        return f"{RENKLER.get(self.hat)}{self.ad}{RENKLER['Varsayılan']}"

class MetroAgi:
    """
    Metro ağını grafik olarak modelleyen sınıf.
    İstasyonları ve aralarındaki bağlantıları yönetir.
    """
    def __init__(self):
        self.istasyonlar: Dict[str, List[Istasyon]] = defaultdict(list)  # istasyon adı -> istasyon nesneleri
        self._count = 0  # A* için eşit maliyetlerde öncelik belirlemek amacıyla sayaç

    def istasyon_ekle(self, idx, ad, hat):
        """Ağa yeni bir istasyon ekler."""
        ist = Istasyon(idx, ad, hat)
        self.istasyonlar[ad].append(ist)
        logging.info(f"İstasyon eklendi: {ist.renkli_ad()} ({hat})")

    def baglanti_ekle(self, id1, id2, sure):
        """İki istasyon arasında çift yönlü bağlantı ekler."""
        tum = sum(self.istasyonlar.values(), [])  # tüm istasyon nesneleri düz listede
        i1 = next(i for i in tum if i.idx == id1)
        i2 = next(i for i in tum if i.idx == id2)
        i1.komsu_ekle(i2, sure)
        i2.komsu_ekle(i1, sure)
        logging.info(f"Bağlantı: {i1.renkli_ad()} ↔ {i2.renkli_ad()} ({sure} dk)")

    def en_az_aktarma_bul(self, bas, hedef):
        """
        BFS algoritması kullanarak EN AZ aktarmalı rotayı bulur.
        Kuyruk elemanı: (istasyon, rota_listesi)
        """
        queue = deque([(bas, [bas])])
        visited = {bas}
        while queue:
            curr, path = queue.popleft()
            if curr == hedef:
                return path
            for nbr, _ in curr.komsular:
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append((nbr, path + [nbr]))
        return None

    def en_hizli_rota_bul(self, bas, hedef):
        """
        A* benzeri algoritma ile EN HIZLI rotayı bulur.
        Öncelik kuyruğu ile toplam süreye göre seçim yapar.
        """
        pq = []
        self._count = 0
        heapq.heappush(pq, (0, self._count, bas, [bas]))
        visited = set()
        while pq:
            cost, _, curr, path = heapq.heappop(pq)
            if curr == hedef:
                return path, cost
            if curr in visited:
                continue
            visited.add(curr)
            for nbr, t in curr.komsular:
                if nbr not in visited:
                    self._count += 1
                    heapq.heappush(pq, (cost + t, self._count, nbr, path + [nbr]))
        return None

    def format_rota(self, rota):
        """Verilen rotayı okunabilir şekilde renkli yazı olarak döndürür."""
        return " -> ".join(st.renkli_ad() for st in rota)

def animate_train(distance=30, delay=0.05):
    """Terminalde tren hareketini simüle eden animasyon."""
    print("\nAnimasyon başlıyor...")
    for pos in range(distance):
        print(' ' * pos + '🚆', end='\r')
        time.sleep(delay)
    print()

if __name__ == '__main__':
    metro = MetroAgi()

    # İstasyonları ekle
    data = [
        ('K1','Kızılay','Kırmızı Hat'),('K2','Ulus','Kırmızı Hat'),('K3','Demetevler','Kırmızı Hat'),('K4','OSB','Kırmızı Hat'),
        ('M1','AŞTİ','Mavi Hat'),('M2','Kızılay','Mavi Hat'),('M3','Sıhhıye','Mavi Hat'),('M4','Gar','Mavi Hat'),
        ('T1','Batıkent','Turuncu Hat'),('T2','Demetevler','Turuncu Hat'),('T3','Gar','Turuncu Hat'),('T4','Keçiören','Turuncu Hat')
    ]
    for idx, ad, hat in data:
        metro.istasyon_ekle(idx, ad, hat)

    # Bağlantıları ekle
    con = [
        ('K1','K2',4),('K2','K3',6),('K3','K4',8),
        ('M1','M2',5),('M2','M3',3),('M3','M4',4),
        ('T1','T2',7),('T2','T3',9),('T3','T4',5),
        ('K1','M2',2),('K3','T2',3),('M4','T3',2)
    ]
    for a, b, s in con:
        metro.baglanti_ekle(a, b, s)

    # Test senaryoları: farklı istasyonlar arası örnek rotalar
    print("\n=== Test Senaryoları ===")
    scenarios = [("AŞTİ", "OSB"), ("Batıkent", "Keçiören"), ("Keçiören", "AŞTİ")]
    for start, end in scenarios:
        start_station = metro.istasyonlar[start][0]
        end_station = metro.istasyonlar[end][0]
        az = metro.en_az_aktarma_bul(start_station, end_station)
        hiz, sure = metro.en_hizli_rota_bul(start_station, end_station) or (None, None)
        print(f"\n{start} → {end}")
        if az:
            print("🛤️ En az aktarmalı:", metro.format_rota(az))
        if hiz:
            print(f"⏱️ En hızlı ({sure} dk):", metro.format_rota(hiz))
        animate_train()
