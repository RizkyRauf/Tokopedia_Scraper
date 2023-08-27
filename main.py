from packtokped import TokopediaScraper
from kota import Kota
from openpyxl import Workbook

def find_city_value(input_city):
    input_city_lower = input_city.lower()  # Mengubah input ke huruf kecil
    
    for kota, value in Kota.data.items():
        if kota.lower() == input_city_lower:
            print(f"Kota {kota} ditemukan")
            return value
    return None

def main():
    print("Selamat datang di Tokopedia!")
    print("=" * 20)
    print("Masukkan nilai kota dengan huruf kecil")
    
    try:
        key_search = input("Masukkan keyword: ").lower().replace(" ", "%20")
        key_city = input("Masukkan kota: ")
        key_page = int(input("Masukkan page: "))
        
        city_value = find_city_value(key_city)
        
        if city_value is not None:
            scraper = TokopediaScraper(chrome_driver_path='PATH CHROME DRIVER',
                                       user_data_dir='PATH USER DATA')
            links = []
            produk_texts = []
            rating_texts = []
            penjualan_texts = []

            workbook = Workbook()
            sheet = workbook.active

            # Menambahkan judul kolom
            sheet.append(["Link", "Produk", "Rating", "Penjualan"])

            for page in range(1, key_page + 1):
                cur_links, cur_produk_texts, cur_rating_texts, cur_penjualan_texts = scraper.run(key_search, city_value, page)
                links.extend(cur_links)
                produk_texts.extend(cur_produk_texts)
                rating_texts.extend(cur_rating_texts)
                penjualan_texts.extend(cur_penjualan_texts)

            for link, produk, rating, penjualan in zip(links, produk_texts, rating_texts, penjualan_texts):
                sheet.append([link, produk, rating, penjualan])

            # Simpan ke dalam file XLSX
            workbook.save("hasil_scraper.xlsx")
            print("Data berhasil disimpan dalam hasil_scraper.xlsx")

    except Exception as e:
        print("Terjadi kesalahan:", e)

if __name__ == "__main__":
    main()
