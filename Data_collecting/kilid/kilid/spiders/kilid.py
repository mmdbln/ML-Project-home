
import scrapy 
from kilid.items import KilidItem
class Kilid(scrapy.Spider):

    name = 'kilid'
    start_urls = ["https://kilid.com"]

    def page_hrefs(self):
        hrefs = []
        base = "/buy-apartment/tehran?page=0"
        for i in range(500):
             yield (base[:-1] + str(i))

    def start_requests(self):
        for href in self.page_hrefs():
            url = f'{self.start_urls[0]}{href}'
            yield scrapy.Request(url, callback=self.parse)
            
    def parse(self, response):
        hrefs = response.css(".style_plp-card-link__yPlrt::attr(href)").extract()
        for href in hrefs:
            yield response.follow(self.start_urls[0] + href, self.parse_subpage)

    def parse_subpage(self, response):
        item = KilidItem()
        item["title"] = response.css(".m-0.text-xl.font-bold::text").extract_first()
        item["price"] = response.css(".mb-6.font-semiBold.text-primary-800.text-display-sm::text").extract_first()
        item["price_per_meter"] = response.css(".text-xl.text-gray-500.font-regular::text").extract_first()
        item["longitude"] = response.css('meta[property="place:location:longitude"]::attr(content)').extract()
        item["latitude"] = response.css('meta[property="place:location:latitude"]::attr(content)').extract()
        item["region_city_loc"] = response.css(".inline-flex.mb-6::text").extract_first()
        item["properties"] = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").get()
        item["func"] = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[1]
        item["type"] = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[0]
        meterage = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[2:4]
        item["meterage"] = ", ".join(meterage)
        bedroom = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[4:6]
        item["bedroom"] = ", ".join(bedroom)
        parking = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[6:8]
        item["parking"] = ", ".join(parking)
        age = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[8:10]
        item["age"] = ", ".join(age)
        # item["facilities"] = response.css(".text-lg.text-gray-800::text").extract()
        item["date"] = response.css('div p.text-sm::text').extract()[-1]
        yield item