# -*- coding: utf-8 -*-
import scrapy
from boilerpipe.extract import Extractor
from gamerankings.items import GameItem, ReviewItem

class GameReviewSpider(scrapy.Spider):
    name = 'games.py'

    # hand out every pages to "parse games list" method
    def start_requests(self):
        for i in range(0, 2): # 259 is the last page
            url = 'https://www.gamerankings.com/browse.html?page={}&sort=5&numrev=1'.format(i)
            request = scrapy.Request(url=url, callback=self.parseGamesList)
            yield request

    # parse lists in the page into seperate games
    def parseGamesList(self, response):
        for link in response.xpath('//div[@class="body"]/table/tr/td[3]/a/@href').extract():
            link = '/'.join(link.split('/')[:-1])
            url = 'http://www.gamerankings.com' + link + '/articles.html'
            request = scrapy.Request(
                url=url, 
                callback=self.parseGame, 
                meta={'dont_redirect': False, 
                    'handle_httpstatus_list': [302]})
            yield request

    # extract article from review page and store into the object
    def parseGame(self, response):
        reviews = response.xpath('//table[@class="release"]/tbody/tr')
        for review in reviews:
            # prepare the object to store
            item = ReviewItem()
            
            # article extractor borrowed from https://github.com/misja/python-boilerpipe
            link = review.xpath('.//td[3]/a/@href').extract()[0]
            extractor = Extractor(extractor='ArticleExtractor', url=link)

            # detailed informations
            item['source'] = review.xpath('.//td[1]/a/text()').extract()[0]
            item['date'] = review.xpath('.//td[2]/text()').extract()[0]
            item['game_name'] = response.xpath('//h1/text()').extract()[0]
            item['game_tag'] = response.xpath('//div[@class="crumbs"]/a/text()').extract()
            item['score'] = review.xpath('.//td[4]/text()').extract()[0]
            item['url'] = link
            item['content'] = extractor.getText()
            print(item)

            # send to pipeline
            yield item
