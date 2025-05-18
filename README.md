# Trafik_isareti_tanima
1210606071 -Zeynep Nur Pekelgil  
1200606004- Sudegül Bayram
1200606011- Mustafa Bağrıaçık 
📌 Proje Adı:
Görüntü İşleme ile Trafik İşareti Tanıma Sistemi

🧠 Kullanılan Yöntemler:
Kenar Algılama: Canny Edge Detection

Morfolojik İşlemler: Dilate ve Erode (OpenCV)

Kontur Tespiti: cv2.findContours()

Öznitelik Çıkartımı: ORB (Oriented FAST and Rotated BRIEF)

Öznitelik Eşleştirme: Brute-Force Matcher (BFMatcher)

Maskeleme: Bitwise işlemlerle işaret çıkarımı

🧰 Kullanılan Kütüphaneler:
OpenCV (cv2) – Görüntü işleme işlemleri için

NumPy (np) – Matris işlemleri için

Flask – Web arayüzü

uuid – Benzersiz dosya isimleri üretmek için

os – Dosya yolları ve klasör işlemleri

🧩 Klasör Yapısı:

trafik_isareti_tanima/
├── app.py
├── utils.py
├── templates/
│   └── index.html
├── static/
│   ├── uploads/          ← Yüklenen görseller
│   └── processed/        ← İşlenmiş görseller
├── templates_data/       ← Trafik işareti şablonları
└── labels.txt            ← Sınıf adlarını içeren etiket dosyası
🧠 Tahmin Mekanizması:
Kullanıcı fotoğraf yükler.

Görsel işlenir (blur, kenar tespiti, kontur çıkarımı).

İşaret bölgesi maske ile ayrılır.

ORB ile anahtar noktalar çıkarılır.

Daha önce çıkarılmış şablonlar ile eşleştirme yapılır.

En çok eşleşen şablona göre trafik işareti tahmini yapılır.

📘 2. Kullanım Kılavuzu
💻 Gereksinimler
Python 3.8+
Pip paket yöneticisi

📸 Kullanım Adımları
Web sayfasına git.

"Fotoğraf Yükle" butonuna tıkla.

Trafik işareti içeren bir görsel seç ve yükle.

Sistem otomatik olarak görseli işler.

Ekranda:

Tahmin edilen trafik işareti adı,

Yüklediğin orijinal fotoğraf,

Kenarları işaretlenmiş hali gösterilir.



