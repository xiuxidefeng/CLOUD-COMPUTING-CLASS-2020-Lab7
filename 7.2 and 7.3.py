import scrapy
import os
import uuid

from elasticsearch import Elasticsearch
from pip._vendor import certifi

# Establish connection to Elastic Cloud
ELASTIC_API_URL = os.environ['ELASTIC_API_URL']
ELASTIC_API_USERNAME = os.environ['ELASTIC_API_USERNAME']
ELASTIC_API_PASSWORD = os.environ['ELASTIC_API_PASSWORD']

es=Elasticsearch([ELASTIC_API_URL],
                 http_auth=(ELASTIC_API_USERNAME,ELASTIC_API_PASSWORD),
                 ca_certs=certifi.where())

class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/title/tt0111161/fullcredits/']

    def parse(self, response):
        #get the movie_id from the url
        id = response.url.split("/")[-3]

        #get the movie details
        movie_title = response.css('h3[itemprop~=name] a::text').extract_first()
        year = response.css('h3[itemprop~=name] span::text').extract_first()
        movie_year = year.split()[0].replace("\u2013","-")
        movie_year = movie_year[1:5]

        #iterate over the actors
        counter = 0
        for line in response.xpath('//*[@class="cast_list"]//tr'):
            counter += 1

            #skip the first dummy line
            if(counter == 1):
                continue
            tmp_actor = line.xpath('td[2]//text()').extract()
            if len(tmp_actor) < 2:
                continue

            actor = tmp_actor[1]
            actor = actor.split()
            if len(actor) == 1:
                actor = actor[0]
            else:
                actor = actor[0]+" "+actor[1]

            actor_href = line.xpath('td[2]/a/@href').extract()
            actor_id = actor_href[0].split('/')[2]
            role = line.xpath("td[@class='character']//text()").extract()
            if not role[0].strip():
                role = role[1].strip().replace("\n", "")
            else:
               role = role[0].strip().replace("\n", "")

            #import data to elasticsearch
            es.index(index='test',
                    doc_type='movies',
                     id=uuid.uuid4(),
                     body={
                        'movie_id': id,
                        'title': movie_title,
                        'movie_year': movie_year,
                        'actor_name': actor,
                        'actor_id': actor_id,
                        'role_name': role
                    })
            # yield {
            #         'movie_id': id,
            #         'title': movie_title,
            #         'movie_year': movie_year,
            #         'actor_name': actor,
            #         'actor_id': actor_id,
            #         'role_name': role,
            #      }

            #scrape actor's bio
            bio_url = "https://www.imdb.com/name/"+actor_id+"/bio"
            next_page = bio_url
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_bio)

            #scrape actor's movies
            actor_url = "https://www.imdb.com/name/"+actor_id
            next_page = actor_url
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_actor)

    def parse_bio(self, response):
        #get the actor_id from the url
        actor_id = response.url.split("/")[-2]

        #get the table that contains the details for the actor
        table =response.xpath('//*[@id="overviewTable"]//tr')

        #save this table in a dictionary in order to make the search simpler
        details = {}
        for k in table:
            details[k.xpath('td[1]//text()').extract()[0]] = k.xpath('td[2]//text()').extract()

        nickname = ""
        birth_name = ""
        birth_date = ""

        #check whether the dictionary has the information that we need (birth name, nickname or date)
        if("Birth Name" in details):
            birth_name = details["Birth Name"][0]
        if("Nickname" in details):
            nicknames = details["Nickname"]
            if len(nicknames) > 0:
                nickname = nicknames[0].strip()
            else:
                nickname = ""
        if("Born" in details):
            birth_date = details["Born"][2]+" "+details["Born"][4]

        #if there is at least one of the above, create a new document for this actor and
        #include his id
        if(birth_name != "" or nickname != "" or birth_date != ""):
            #import data to elasticsearch
            es.index(index='test',
                    doc_type='movies',
                     id=uuid.uuid4(),
                     body={
                        "actor_id":actor_id,
                        "birth name":birth_name,
                        "nickname":nickname,
                        "birth_date":birth_date
                    })
            # yield {
            #     "actor_id":actor_id,
            #     "birth name":birth_name,
            #     "nickname":nickname,
            #     "birth_date":birth_date,
            #     }

    def parse_actor(self, response):
        div = response.xpath('//div[@class="filmo-category-section"]')

        #iterate over the movies
        for d in div:
            movie_id = d.xpath('.//b/a/@href').extract_first()
            movie_year = d.xpath('.//span[@class="year_column"]/text()').extract_first().split()
            if len(movie_year) > 0:
                movie_year = movie_year[0]
            else:
                movie_year = "2000"
            movie_year = movie_year[:4]
            if movie_id is not None and int(movie_year) >= 1980 and int(movie_year) < 1990:
                next_page = "http://www.imdb.com"+movie_id+"fullcredits/"
                if next_page is not None:
                    yield response.follow(next_page, callback=self.parse)
