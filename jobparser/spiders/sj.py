import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='//div[@class='acdxh GPKTZ _1tH7S']/div/a/@href").get()
        next_page = response.xpath("//a[@class='f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").get()
        vac_salary = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
        vac_url = response.url
        yield JobparserItem(name=vac_name, salary=vac_salary, url=vac_url)
