import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

import re

class TokopediaScraper:
    def __init__(self, chrome_driver_path, user_data_dir):
        self.chrome_driver_path = chrome_driver_path
        self.user_data_dir = user_data_dir

    def get_driver(self):
        service = Service(self.chrome_driver_path)
        options = Options()
        return webdriver.Chrome(service=service, options=options)

    # method untuk scraping link non ternary
    def scrape_links(self, driver):
        link_path = "//div[@class='css-1asz3by']/a[@class='pcv3__info-content css-gwkf0u']"
        links = driver.find_elements(By.XPATH, link_path)
        processed_links = []

        for link in links:
            href = link.get_attribute('href')
            if href:
                if re.search(r'https://www\.tokopedia\.com', href):
                    href = re.sub(r'\?ext.*', '', href)
                else:
                    href = re.sub(r'^.*www\.', 'https://www.', href)
                    href = re.sub(r'%3Fex.*', '', href)
                    href = href.replace('%2F', '/')
                    
                processed_links.append(href)
            else:
                processed_links.append("N/A")

        return processed_links

    # method untuk scraping produk ternary
    def scrape_produk(self, driver):
        produk_path = "//div[@class='prd_link-product-name css-3um8ox']"
        produk = driver.find_elements(By.XPATH, produk_path)
        processed_produk = [produk.text if produk.text else "N/A" for produk in produk]
        return processed_produk

    # method untuk scraping rating ternary
    def scrape_rating(self, driver):
        rating_path = "//div[@class='css-yaxhi2']/div/span[@class='prd_rating-average-text css-t70v7i']"
        rating = driver.find_elements(By.XPATH, rating_path)
        processed_rating = [rating.text if rating.text else "N/A" for rating in rating]
        return processed_rating

    # method untuk scraping penjualan ternary
    def scrape_penjualan(self, driver):
        penjualan_path = "//div[@class='prd_shop-rating-average-and-label css-26zmlj']/span[@class='prd_label-integrity css-1sgek4h']"
        penjualan = driver.find_elements(By.XPATH, penjualan_path)
        processed_penjualan = [penjualan.text if penjualan.text else "N/A" for penjualan in penjualan]
        return processed_penjualan


    def run(self, key_search, city_value, key_page):
        try:
            with self.get_driver() as driver:
                url = f'https://www.tokopedia.com/search?fcity={city_value}&navsource=&page={key_page}&q={key_search}'
                driver.get(url)
                time.sleep(5)

                #scroll
                old_height = driver.execute_script("return document.body.scrollHeight")

                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    
                    if new_height == old_height:
                        break
                    
                    old_height = new_height


                links = self.scrape_links(driver)
                produk_texts = self.scrape_produk(driver)
                rating_texts = self.scrape_rating(driver)
                penjualan_texts = self.scrape_penjualan(driver)


                # Pastikan panjang semua list sama
                max_len = max(len(links), len(produk_texts), len(rating_texts), len(penjualan_texts))
                links += ["N/A"] * (max_len - len(links))
                produk_texts += ["N/A"] * (max_len - len(produk_texts))
                rating_texts += ["N/A"] * (max_len - len(rating_texts))
                penjualan_texts += ["N/A"] * (max_len - len(penjualan_texts))

                print("Links:", links)
                print("Produk:", produk_texts)
                print("Rating:", rating_texts)
                print("Penjualan:", penjualan_texts)

                return links, produk_texts, rating_texts, penjualan_texts

        except Exception as e:
            print(e)

    def save_to_excel(self, links, produk_texts, rating_texts, penjualan_texts, output_file):
        data = {
            "Link": links,
            "Produk": produk_texts,
            "Rating": rating_texts,
            "Penjualan": penjualan_texts
        }

        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
