import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class TrapstarlondonSpider(scrapy.Spider):
    name = "trapstarlondon"
    allowed_domains = ["uk.trapstarlondon.com"]
    start_urls = ["https://uk.trapstarlondon.com/collections/new-drop"]

    def parse(self, response):
        # Use Selenium to scroll down the page
        driver = webdriver.Chrome()
        driver.get(response.url)

        try:
            # Wait for the first popup to appear (adjust timeout as needed)
            first_popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "recommendation-modal__close-button"))
            )
            # Close the first popup by clicking the close button
            first_popup.click()
            # Wait for the second popup to appear (adjust timeout as needed)
            second_popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "omnisend-form-5f4906684c7fa469cfd02c58-close-action"))
            )
            # Close the second popup by clicking the close button
            second_popup.click()

        finally:
            # Continue with your automation logic
            pass
        # Scroll the page multiple times
        for _ in range(11):  # Adjust the number of times you want to scroll
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)

        time.sleep(5)

        # Create a new response from the updated HTML content after scrolling
        body = driver.page_source
        new_response = HtmlResponse(url=response.url, body=body, encoding='utf-8')

        # Parse the products from the updated response
        products = new_response.css('div.grid-view-item.product-card')
        for product in products:
            yield {
                'name': product.css('div.h4.grid-view-item__title.product-card__title::text').get(),
                'regularPrice': product.css('span.price-item.price-item--regular::text').get().replace('\n', '').replace(' ', ''),
                'salePrice': product.css('span.price-item.price-item--sale::text').get().replace('\n', '').replace(' ', ''),
                'img': product.css('div.grid-view-item__image-wrapper.product-card__image-wrapper.js img::attr(src)').get()
            }

        driver.quit()  # Close the browser after scraping