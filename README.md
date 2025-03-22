
# 🚇 **ArzuBesiroglu_MetroSimulation**

**Python ile geliştirilmiş sürücüsüz metro simülasyonu:** BFS ve A* algoritmaları ile rota optimizasyonu.

---

## 📌 **Proje Tanımı**
Bu proje, **Global AI Hub & Akbank - Python ile Yapay Zekaya Giriş Bootcamp** kapsamında geliştirilen bir metro simülasyonudur.
Amaç, terminal tabanlı bir arayüz üzerinden iki metro istasyonu arasında:

- 🛤️ **En az aktarmalı rotayı** (BFS algoritması ile)
- ⏱️ **En hızlı rotayı** (A* algoritması ile) bulmaktır.

---

## 🎯 **Proje Hedefleri**
- **Metro istasyonlarının graf yapısı ile modellenmesi**
- **Breadth-First Search (BFS)** ile en az aktarma yapılan rotanın bulunması
- **A\*** algoritması ile süre bazlı en kısa rotanın bulunması
- **Kullanıcı etkileşimiyle** terminal üzerinden seçim yapılması
- **Terminal tabanlı tren animasyonu** ile kullanıcı deneyiminin artırılması

---

## ⚙️ **Kullanılan Teknolojiler ve Kütüphaneler**

| **Kütüphane**       | **Açıklama**                                   |
|---------------------|------------------------------------------------|
| `collections.deque` | BFS kuyruğu için hızlı liste yapısı            |
| `heapq`             | A* algoritması için öncelik kuyruğu            |
| `logging`           | Terminalde bilgi mesajları göstermek için      |
| `time`              | Tren animasyonu için gecikme efekti            |
| `typing`            | Tür ipuçları ile kodun okunabilirliği          |

---

## 🧠 **Algoritmaların Çalışma Mantığı**

### 1. **BFS – En Az Aktarma Bulma**
- **FIFO kuyruk yapısı** (`deque`)
- Her istasyonda **komşular gezilir**
- **Ziyaret edilen düğümler** takip edilir
- **Hedef istasyona** ulaşıldığında rota döndürülür

### 2. **A* – En Hızlı Rota Bulma**
- `f(n) = g(n) + h(n)` skor mantığı
- `g(n)`: Başlangıçtan şu ana kadar geçen süre
- `h(n)`: Heuristik (örnek: hat değişiminden kaynaklı sabit maliyet)
- **Öncelik kuyruğu** (`heapq`) ile minimum süreli istasyonlar öncelikli seçilir

---

## 🧪 **Örnek Test Senaryoları**
```bash
1. AŞTİ → OSB
2. Batıkent → Keçiören
3. Keçiören → AŞTİ
```
Bu testlerde hem en az aktarma hem de en kısa süreli rotalar başarıyla hesaplanmakta ve terminalde gösterilmektedir.

---

## 🎨 **Ekstra Özellikler**
- 🎨 **Terminalde renklendirilmiş istasyon isimleri** (ANSI kodları)
- 🚆 **ASCII tren animasyonu**
- 🧭 **Kullanıcıdan istasyon seçimini terminal üzerinden alma**
- 🪪 **Versiyonlu dosya yönetimi** (`v1`, `v2`... `v6`)
- 🔍 **Kodda kapsamlı yorumlar** ve `logging` modülü ile bilgi çıktıları

---

## 🔧 **Geliştirme Fikirleri**
- GUI (ör. Tkinter / PyQt) ile grafik arayüz
- Daha büyük ve gerçekçi metro verisi ile test
- JSON'dan metro ağı veri okuma
- Dijkstra algoritması karşılaştırması
- Harita görselleştirme (ör. matplotlib + networkx)

---

## 💾 **Nasıl Çalıştırılır?**
```bash
python ArzuBesiroglu_MetroSimulation.py
```
Komut satırında istasyonları seçtikten sonra **animasyonlu ve renkli rotalar** görüntülenir.

---

## 👩‍💻 **Proje Sahibi**
**Arzu Beşiroğlu**  
🔗 Linktree: [https://linktr.ee/arzubesiroglu](https://linktr.ee/arzubesiroglu)  
🐙 GitHub: [https://github.com/arzubesiroglu](https://github.com/arzubesiroglu)

---

## 📁 **Sürümler**
- `v1`: İlk sürüm, temel algoritmalar
- `v2`: Tekrarlayan duraklar filtrelendi
- `v3`: Logging eklendi
- `v4`: Renkli istasyonlar (ANSI)
- `v5`: Kullanıcı seçimli terminal menüsü
- `v6`: Tren animasyonu eklendi
- `Final`: Tüm özellikler entegre edildi, test senaryoları tamamlandı

---

## ⭐ **Katkı ve Destek**
Beğendiyseniz ⭐ verin, projeyi fork'lamaktan çekinmeyin!  
Geri bildirimlerinizi, katkı isteklerinizi ve yeni fikirlerinizi memnuniyetle karşılarım. 😊

---

## 🏁 **Teşekkürler**
**Global AI Hub** ve **Akbank** ekibine, bu proje sürecinde sağladıkları yönlendirmeler için teşekkür ederim.

> "**Veriyi takip eden kazanır, datayla kalın! 🚇📊**"

---




