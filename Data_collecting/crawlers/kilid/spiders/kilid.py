
import scrapy 
from kilid.items import Item
import json
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
        start_index = response.body.find(b'\\"longitude\\":')
        end_index = response.body.find(b',\\"targetGlobalLocation\\":')
        relevant_text = response.body[start_index:end_index+1].decode('unicode_escape')

        # Clean up the string to make it a valid JSON
        relevant_text = relevant_text.replace('x8c ', '').replace('\\",\\"', '","').rstrip(',')
        relevant_text = f'{{{relevant_text}}}'  # Wrap in curly braces to form a valid JSON object

        print(f'Relevant Text: {relevant_text}')  # Add this line for debugging

        try:
            # Load the JSON string into a Python dictionary
            data = json.loads(relevant_text)

            # Extract latitude and longitude
            longitude = data.get('longitude')
            latitude = data.get('latitude')
            self.log(f'Longitude: {longitude}, Latitude: {latitude}')

            # Continue with your parsing logic
        except json.JSONDecodeError as e:
            self.log(f'Error decoding JSON: {e}')

        
        item = Item()
        item["title"] = response.css(".m-0.text-xl.font-bold::text").extract_first()
        item["price"] = response.css(".mb-6.font-semiBold.text-primary-800.text-display-sm::text").extract_first()
        item["price_per_meter"] = response.css(".text-xl.text-gray-500.font-regular::text").extract_first()
        item["longitude"] = longitude
        item["latitude"] = latitude
        item["address"] = response.css(".inline-flex.mb-6::text").extract_first()
        item["properties"] = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").get()
        item["func"] = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[1]
        item["type"] = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[0]
        meterage = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[2:4][0]
        item["meterage"] = ", ".join(meterage)
        bedroom = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[4:6][0]
        item["bedroom"] = ", ".join(bedroom)
        parking = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[6:8][0]
        item["parking"] = ", ".join(parking)
        age = response.css(".px-2.py-1.text-sm.rounded-lg.bg-grey-100::text").getall()[8:10][0]
        item["age"] = ", ".join(age)
        # item["facilities"] = response.css(".text-lg.text-gray-800::text").extract()
        # item["date"] = response.css('div p.text-sm::text').extract()[-1]
        yield item