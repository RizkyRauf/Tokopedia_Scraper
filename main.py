from packtokped import TokopediaScraper
from kota import Kota 

def find_city_value(input_city):
    input_city_lower = input_city.lower()
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
        key_page = int(input("Masukkan page:"))

        city_value = find_city_value(key_city)

        if city_value is not None:
            chrome_driver_path = 'C:\Driver\chromedriver.exe'
            user_data_dir = ''
            scraper = TokopediaScraper(chrome_driver_path, user_data_dir)

            links, produk_texts, rating_texts, penjualan_texts = [], [], [], []

            for page in range(1, key_page + 1):
                cur_links, cur_produk_texts, cur_rating_texts, cur_penjualan_texts = scraper.run(key_search, city_value, page)
                links.extend(cur_links)
                produk_texts.extend(cur_produk_texts)
                rating_texts.extend(cur_rating_texts)
                penjualan_texts.extend(cur_penjualan_texts)

            result_file = "hasil_scraper.xlsx"
            scraper.save_to_excel(links, produk_texts, rating_texts, penjualan_texts, result_file)
            print(f"Data berhasil disimpan dalam {result_file}")
        else:
            print(f"Kota {key_city} tidak ditemukan dalam daftar Kota.data")

    except Exception as e:
        print("Terjadi kesalahan:", e)

if __name__ == "__main__":
    main()
