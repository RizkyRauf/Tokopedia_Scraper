# Tokopedia_Scraper

Selamat datang di proyek Tokopedia Scraper! Proyek ini adalah alat sederhana untuk mengumpulkan informasi produk dari Tokopedia menggunakan Selenium.

## Deskripsi

Proyek ini terdiri dari beberapa modul yang bekerja bersama untuk melakukan scraping data dari situs web Tokopedia. Modul-modul tersebut adalah:

- `main.py`: Skrip utama yang mengatur alur kerja, menerima input dari pengguna, dan menggunakan modul `packtokped` dan `kota` untuk melakukan scraping dan menyimpan data dalam file XLSX.
- `packtokped.py`: Modul yang berisi kelas `TokopediaScraper` untuk melakukan scraping pada situs Tokopedia. Modul ini menggunakan Selenium untuk mengotomatisasi proses browsing.
- `kota.py`: Modul yang berisi kelas `Kota` yang menyimpan data daftar kota beserta nilai yang digunakan dalam URL pencarian Tokopedia.
- `requirements.txt`: Berkas yang berisi daftar pustaka yang diperlukan untuk menjalankan proyek ini. Anda dapat menginstal pustaka-pustaka ini dengan menjalankan perintah `pip install -r requirements.txt`.

## Cara Penggunaan

1. Pastikan Anda memiliki Python 3.x terinstal di komputer Anda.
2. Clone repositori ini ke komputer Anda.
3. Instal pustaka-pustaka yang diperlukan dengan menjalankan perintah berikut di terminal atau command prompt:

   ```
   pip install -r requirements.txt
   ```
Jalankan skrip utama dengan menjalankan perintah:
```
python main.py
```
Skrip ini akan meminta Anda untuk memasukkan keyword, kota, dan halaman yang ingin Anda scraping. Hasilnya akan disimpan dalam file hasil_scraper.xlsx.

**Kontribusi**
Kontribusi dan masukan Anda sangat dihargai. Jika Anda ingin berkontribusi pada proyek ini, silakan buat pull request atau ajukan issue di repositori ini.
