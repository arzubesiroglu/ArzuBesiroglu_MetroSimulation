# Gerekli kütüphaneleri içe aktar

import logging
from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional

# ANSI Renk Kodları (Terminalde durakları renklerine göre ayırmak için)
RENKLER = {
    "Kırmızı Hat": "\033[91m",  # Kırmızı
    "Mavi Hat": "\033[94m",     # Mavi
    "Turuncu Hat": "\033[93m",  # Sarı/Turuncu
    "Varsayılan": "\033[0m"      # Varsayılan Renk
}

# Loglama ayarları
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

    def renkli_ad(self):
        """İstasyon adını hattının rengine göre renklendirir."""
        renk = RENKLER.get(self.hat, RENKLER["Varsayılan"])
        return f"{renk}{self.ad}{RENKLER['Varsayılan']}"

class MetroAgi:
    """
    Metro ağı sınıfı. İstasyonları ve bağlantıları yönetir.
    """
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        """Yeni bir istasyon ekler."""
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)
            logging.info(f'İstasyon eklendi: {istasyon.renkli_ad()} ({hat})')

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        """İki istasyon arasında bağlantı kurar."""
        ist1 = self.istasyonlar[istasyon1_id]
        ist2 = self.istasyonlar[istasyon2_id]
        ist1.komsu_ekle(ist2, sure)
        ist2.komsu_ekle(ist1, sure)
        logging.info(f'Bağlantı eklendi: {ist1.renkli_ad()} ↔ {ist2.renkli_ad()} ({sure} dk)')

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritmasını kullanarak en az aktarmalı rotayı bulur."""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            logging.error("Geçersiz istasyon ID'si girildi!")
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        queue = deque([(baslangic, [baslangic])])
        visited = {baslangic}

        while queue:
            mevcut, rota = queue.popleft()
            if mevcut == hedef:
                logging.info(f'En az aktarmalı rota bulundu: {" -> ".join(i.renkli_ad() for i in rota)}')
                return rota

            for komsu, _ in mevcut.komsular:
                if komsu not in visited:
                    visited.add(komsu)
                    queue.append((komsu, rota + [komsu]))

        logging.warning("Hedefe ulaşan bir rota bulunamadı!")
        return None


    def en_hizli_rota_bul(self, bas_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritmasını kullanarak en hızlı rotayı bulur."""
        if bas_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            logging.error("Geçersiz istasyon ID'si girildi!")
            return None
        bas = self.istasyonlar[bas_id]
        hedef = self.istasyonlar[hedef_id]
        pq = [(0, bas, [bas])]
        visited = set()
        while pq:
            sure, current, path = heapq.heappop(pq)
            if current == hedef:
                logging.info(f'En hızlı rota bulundu ({sure} dk): {" -> ".join(i.renkli_ad() for i in path)}')
                return path, sure
            if current not in visited:
                visited.add(current)
                for komsu, gecis_suresi in current.komsular:
                    if komsu not in visited:
                        heapq.heappush(pq, (sure + gecis_suresi, komsu, path + [komsu]))
        logging.warning("Hedefe ulaşan bir rota bulunamadı!")
        return None

# Örnek Kullanım
if __name__ == "__main__":
    logging.info("Program başlatıldı. Metro ağı oluşturuluyor...")
    metro = MetroAgi()

    # İstasyon ekleme
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")

    # Bağlantılar
    metro.baglanti_ekle("K1", "K2", 4)
    metro.baglanti_ekle("K1", "M1", 2)
    metro.baglanti_ekle("M4", "K2", 3)

    # Test Senaryoları
    print("\n=== En Az Aktarmalı Rota Testi ===")
    metro.en_az_aktarma_bul("K1", "M4")

    print("\n=== En Hızlı Rota Testi ===")
    metro.en_hizli_rota_bul("K1", "M4")
