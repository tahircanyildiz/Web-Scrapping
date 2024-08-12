# Web Uygulaması: Makale Arama Motoru

Bu web uygulaması, kullanıcıların belirli anahtar kelimelerle makale araması yapmalarına ve ardından tarih ve yazar adına göre filtreleme yapmalarına olanak tanıyan bir arama motoru içermektedir.

## Özellikler

### 1. Anahtar Kelime ile Makale Arama
- Kullanıcı, arama çubuğuna anahtar kelimeleri girerek makale araması yapabilir.
- Anahtar kelimeler, arXiv veritabanında bulunan makaleler üzerinde arama yapmak için kullanılır.
- Kullanıcının girdiği anahtar kelimelere uygun olan ilk 10 makale listelenir.
- Listelenen her makale başlığı tıklanabilir.

### 2. Tarih ve Yazar Adına Göre Filtreleme
- Kullanıcı, tarih ve/veya yazar adını belirterek makaleleri filtreleyebilir.
- Eğer tarih ve/veya yazar adı belirtilirse, ilgili kriterlere uyan ilk 10 makale listelenir.
- Her bir makale başlığı tıklanabilir.

### 3. Makale Detayları
- Kullanıcı, makale başlığına tıklayarak bir makalenin detaylı bilgilerine erişebilir.
- Detaylar arasında makale başlığı, yazarlar, özet, gönderim tarihi, arXiv ID, DOI, proje bağlantısı, referanslar ve PDF indirme bağlantısı bulunur.

### 4. PDF İndirme
- Kullanıcı, makale detay sayfasındayken "PDF İndir" butonuna tıklayarak ilgili makalenin PDF dosyasını indirebilir.

## Teknolojiler

- **Flask:** Uygulamanın arka ucunu oluşturan Python web çerçevesi.
- **MongoDB:** Makale bilgilerini depolamak için kullanılan NoSQL veritabanı.
- **arXiv API:** Makale aramaları için kullanılan arXiv veritabanı API'si.

## Kullanım

1. Uygulamanın ana sayfasında arama çubuğuna anahtar kelimeleri girin ve "Ara" butonuna tıklayın.
2. Arama sonuçlarından bir makale başlığına tıklayarak makale detaylarını görüntüleyin.
3. İlgili makale sayfasında, "PDF İndir" butonuna tıklayarak makalenin PDF dosyasını indirin.
4. Dilerseniz, arama işlemini tarih ve yazar adı ile filtreleyin.

## Kurulum

1. Bu projeyi bilgisayarınıza klonlayın:
   ```bash
   git clone https://github.com/tahircanyildiz/Web-Scrapping.git
