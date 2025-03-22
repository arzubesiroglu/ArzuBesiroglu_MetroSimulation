# Gerekli kütüphaneleri içe aktar
from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    """
    Metro istasyonlarını temsil eden sınıf.
    Her istasyonun bir ID'si, adı ve bağlı olduğu hattı vardır.
    """
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        """İstasyona bir komşu ekler."""
        self.komsular.append((istasyon, sure))

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

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        """İki istasyon arasında bağlantı kurar."""
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """
        BFS algoritması kullanarak EN AZ aktarmalı rotayı bulur.

        Kuyruk elemanı: (istasyon, rota_listesi, aktarma_sayısı, mevcut_hat)
        """
        # Başlangıç/hedef kontrolü
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # FIFO kuyruğu başlatılıyor; başlangıç için aktarma=0, mevcut_hat başlangıcın hattı
        queue = deque([(baslangic, [baslangic], 0, baslangic.hat)])
        # (istasyon_id, hat) çifti şeklinde ziyaret takibi
        visited = {(baslangic.idx, baslangic.hat)}

        while queue:
            current, path, transfers, curr_hat = queue.popleft()

            # Hedef bulunduysa rota döndürülür
            if current.idx == hedef.idx:
                return path

            # Komşular arasında dolaş
            for neighbor, _ in current.komsular:
                # Yeni aktarma sayısı: komşunun hattı farklıysa +1
                new_transfers = transfers + (neighbor.hat != curr_hat)
                state = (neighbor.idx, neighbor.hat)

                # Eğer bu istasyon-hat kombinasyonu daha önce görülmediyse kuyruğa ekle
                if state not in visited:
                    visited.add(state)
                    queue.append((neighbor, path + [neighbor], new_transfers, neighbor.hat))

        # Rota yoksa None döndür
        return None


    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """
        A* algoritması kullanarak en hızlı rotayı bulur.
        
        1) Kontrol: Başlangıç & hedef var mı?
        2) A* (f = g + h). Basit heuristic (hat farkına sabit ekleme).
        3) Rota yoksa None, varsa (rota, toplam_sure).
        """
        # Başlangıç ve hedef istasyonların varlığını kontrol et
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        def heuristic(ist: Istasyon) -> int:
            # Basit heuristic: Hedefin hattıyla farklıysa +5
            return 5 if ist.hat != hedef.hat else 0

        # pq: (fScore, gScore, istasyon, rota)
        pq = []
        import heapq

        gScore = {baslangic: 0}
        fScore = {baslangic: heuristic(baslangic)}

        # Tie-breaker: id(istasyon) eklenmesi, 'TypeError: < not supported' hatasını önler
        heapq.heappush(pq, (fScore[baslangic], gScore[baslangic], id(baslangic), baslangic, [baslangic]))

        visited = set()

        while pq:
            fNow, gNow, _, mevcut, path = heapq.heappop(pq)
            if mevcut == hedef:
                return path, gNow

            if mevcut not in visited:
                visited.add(mevcut)
                for (komsu, cost) in mevcut.komsular:
                    yeniSure = gNow + cost
                    if (komsu not in gScore) or (yeniSure < gScore[komsu]):
                        gScore[komsu] = yeniSure
                        fScore[komsu] = yeniSure + heuristic(komsu)
                        heapq.heappush(pq, (fScore[komsu], yeniSure, id(komsu), komsu, path + [komsu]))

        return None

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
