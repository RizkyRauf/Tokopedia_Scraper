import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re

class TokopediaScraper:
    def __init__(self, chrome_driver_path, user_data_dir):
        self.chrome_driver_path = chrome_driver_path
        self.user_data_dir = user_data_dir

    def get_driver(self):
        service = Service(self.chrome_driver_path)
        options = Options()
        options.add_argument(f"user-data-dir={self.user_data_dir}")
        return webdriver.Chrome(service=service, options=options)

    def scrape_links(self, driver):
        link_path = "//div[@class='css-974ipl']/a"
        links = driver.find_elements(By.XPATH, link_path)

        processed_links = []

        for link_elem in links:
            link = link_elem.get_attribute('href')
            if 'https://ta.tokopedia.com' in link:
                link_regex = re.search(r'www\.tokopedia\.com(.+)', link)
                if link_regex:
                    link_part = link_regex.group(1).replace('%2F', '/')
                    processed_link = f'https://www.tokopedia.com{link_part}'
                    processed_link = re.sub(r'%3.*|&.*', '', processed_link)
                else:
                    processed_link = link
            elif 'https://www.tokopedia.com' in link:
                processed_link = re.sub(r'\?ext.*|&.*|\&keywords.*|\&page.*|&uid.*', '', link)
            else:
                processed_link = link

            processed_links.append(processed_link)

        return processed_links

    def scrape_text_elements(self, driver, element_path):
        elements = driver.find_elements(By.XPATH, element_path)

        processed_elements = []

        for elem in elements:
            elem_text = elem.text.strip() or "No Data Found"
            processed_elements.append(elem_text)

        return processed_elements

    def scrape_produk(self, driver):
        produk_path = "//div[@class='prd_link-product-name css-3um8ox']"
        return self.scrape_text_elements(driver, produk_path)

    def scrape_rating(self, driver):
        rating_path = "//div[@class='css-yaxhi2']/div/span[@class='prd_rating-average-text css-t70v7i']"
        return self.scrape_text_elements(driver, rating_path)

    def scrape_penjualan(self, driver):
        penjualan_path = "//div[@class='css-yaxhi2']/div/span[@class='prd_label-integrity css-1duhs3e']"
        return self.scrape_text_elements(driver, penjualan_path)

    def run(self, key_search, city_value, key_page):
        try:
            with self.get_driver() as driver:
                url = f'https://www.tokopedia.com/search?fcity={city_value}&navsource=&page={key_page}&q={key_search}'
                driver.get(url)

                old_height = driver.execute_script("return document.body.scrollHeight")

                while True:
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                    time.sleep(2)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    
                    if new_height == old_height:
                        break
                    
                    old_height = new_height

                links = self.scrape_links(driver)
                produk_texts = self.scrape_produk(driver)
                rating_texts = self.scrape_rating(driver)
                penjualan_texts = self.scrape_penjualan(driver)

                return links, produk_texts, rating_texts, penjualan_texts

        except Exception as e:
            print(e)
