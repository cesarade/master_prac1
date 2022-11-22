import scrapy

class PatiotuercaGuayaquilSpider(scrapy.Spider):
    name = 'patiotuerca_guayaquil'
    allowed_domains = ['ecuador.patiotuerca.com']
    start_urls = [
        'https://ecuador.patiotuerca.com/usados/guayas-guayaquil/autos',
        'https://ecuador.patiotuerca.com/usados/pichincha-quito/autos',
        'https://ecuador.patiotuerca.com/usados/azuay-cuenca/autos',
        'https://ecuador.patiotuerca.com/usados/manabi-manta/autos'
    ]

    def parse(self, response):
        car_container = response.xpath('//div[@class = "usedList half-banner full-item"]//div[contains(@class, "vehicle-container")]')
        
        for car in car_container:
            try:
                name = car.xpath('.//div[contains(@class, "tittle")]/h4/text()').get()
                year = car.xpath('.//span[contains(@class, "year")]/text()').get()
                km = car.xpath('.//div[contains(@class, "vehicle-highlight")]/text()').getall()
                price = car.xpath('.//strong[contains(@class, "price-text")]/span/text()').get()

                yield {
                    'name': name,
                    'year': year,
                    'km': km[1],
                    'price': price
                }
            except:
                pass

        pagination = response.xpath('//ul[contains(@class, "pagination")]')
        next_page_url = pagination.xpath('.//li/a[contains(text(), ">")]/@href').get()

        if next_page_url:
            yield response.follow(url = next_page_url, callback = self.parse)


        
