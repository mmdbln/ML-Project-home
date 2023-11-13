import time
import scrapy
from scrapy_splash import SplashRequest
from divar.items import Item
from selenium.webdriver.chrome.service import Service as chromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Divar(scrapy.Spider):
    name = "divar"
    start_urls = ["https://divar.ir"]
    def __init__(self, *args, **kwargs):
        super(Divar, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=chromeService(
        "/home/mohe/Downloads/chromedriver"))
    

    def scroll_infinite_page(self, step):
        self.driver.execute_script(f"window.scrollBy(0, {step});")
        time.sleep(2)

    script = """
    function main(splash)
        splash:go(splash.args.url)
        splash:wait(3)  -- Adjust the wait time as needed
        return splash:html()
    end
    """
    
    def start_requests(self):
        url ="https://divar.ir/s/tehran/buy-apartment"
        self.driver.get(url)
        step = 1000
        for i in range(1, 2):
            hrefs = self.driver.find_elements(By.XPATH, "//a[@class=''][@href]")
            for href in hrefs:
                url = href.get_attribute("href")
                # self.url_list.append(url)
                yield SplashRequest(url, callback=self.parse)
            self.scroll_infinite_page(step)
        # self.url_list = list(set(self.url_list))

        


    def parse(self, response):
        item = Item()
        item["title"] = response.css(".kt-page-title__title.kt-page-title__title--responsive-sized::text").get()
        item["price"] = response.css(".kt-unexpandable-row__value::text").get()
        item["price_per_meter"] = response.css(".kt-unexpandable-row__value::text").get()
        item["floor"] = response.css(".kt-unexpandable-row__value::text").get()
        item["meterage_age_bedroom_facilities"] = response.css(".kt-group-row-item__value::text").getall()
        item["date"] = response.css(".kt-page-title__subtitle.kt-page-title__subtitle--responsive-sized::text").getall()
        yield item
        


    def parse_subpages(self, response):
        item = Item()
        item["title"] = response.css(".kt-page-title__title.kt-page-title__title--responsive-sized::text").getall()[0]
        item["price"] = response.css(".kt-unexpandable-row__value::text").getall()[0]
        item["price_per_meter"] = response.css(".kt-unexpandable-row__value::text").getall()[1]
        item["floor"] = response.css(".kt-unexpandable-row__value::text").getall()[2]
        item["meterage"] = response.css(".kt-group-row-item__value::text").getall()[0]
        item["age"] = response.css(".kt-group-row-item__value::text").getall()[1]
        item["bedroom"] = response.css(".kt-group-row-item__value::text").getall()[2]
        item["facilities"] = response.css(".kt-group-row-item__value::text").getall()[3:6]
        item["time"] = response.css(".kt-page-title__subtitle.kt-page-title__subtitle--responsive-sized::text").getall()
        yield item






    