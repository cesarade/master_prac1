import scrapy


class AutocosmosSpider(scrapy.Spider):
    name = 'autocosmos'
    allowed_domains = ['www.autocosmos.com.ec']
    start_urls = ['https://www.autocosmos.com.ec/auto/usado']

    def parse(self, response):
        # Obtener el contenedor (listing-container) que contiene toda la data que queremos: name, model, version..
        car_container = response.xpath('//div[contains(@class, "listing-container")]/article')

        # Hacer un "bucle for" a cada auto listado en el "listing-container"
        for car in car_container:
            name = car.xpath('.//*[contains(@class, "listing-card__brand")]/text()').get()
            model = car.xpath('.//*[contains(@class, "listing-card__model")]/text()').get()
            version = car.xpath('.//*[contains(@class, "listing-card__version")]/text()').get()
            year = car.xpath('.//*[contains(@class, "listing-card__year")]/text()').get()
            km = car.xpath('.//*[contains(@class, "listing-card__km")]/text()').get()
            city = car.xpath('.//*[contains(@class, "listing-card__city")]/text()').get()
            province = car.xpath('.//*[contains(@class, "listing-card__province")]/text()').get()
            price = car.xpath('.//*[contains(@class, "listing-card__price-value")]/text()').get()

            # Devolver la data extraida
            yield {
                    'name': name,
                    'model': model,
                    'version': version,
                    'year': year,
                    'km': km,
                    'city': city,
                    'province': province,
                    'price': price
            }

        # Obtener la barra de paginacion (pagination) y luego el link del boton que nos lleva a la siguiente pagina
        pagination = response.xpath('//footer[contains(@class, "pagenav")]')
        next_page_url = pagination.xpath('//a[contains(text(), "Siguiente")]/@href').get()

        # Ir al link "Siguiente"
        if next_page_url:
            yield response.follow(url = next_page_url, callback = self.parse)
