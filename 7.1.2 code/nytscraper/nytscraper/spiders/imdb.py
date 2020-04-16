import scrapy

class NytimesSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['https://www.imdb.com/title/tt0096463/fullcredits/']
    start_urls = ['https://www.imdb.com/title/tt0096463/fullcredits/']

    def parse(self, response):
        for section in response.css("section[data-testid]"):
            section_name = section.attrib['data-block-tracking-id']
            for article in section.css("article"):
                yield {
                    "movie_id": "tt0096463",
                    "movie_name": "Working Girl",
                     "movie_year": 1988,
                    'actor_name': response.xpath('//*[@id="fullcredits_content"]/table[3]/tbody/tr[2]/td[2]/a'),
                    "actor_id": "nm0000228",
                    'role_name': response.xpath('//*[@id="fullcredits_content"]/table[3]/tbody/tr[2]/td[4]/a'),
                   }