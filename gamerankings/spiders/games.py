# -*- coding: utf-8 -*-
import scrapy
from boilerpipe.extract import Extractor
from gamerankings.items import GameItem, ReviewItem

class GameReviewSpider(scrapy.Spider):
    name = 'games.py'

    # hand out every pages to "parse games list" method
    def start_requests(self):
        # step 1: crawl every games through 2011 
        for i in range(0, 500): # 499 is the last page limit
            url = 'https://www.gamerankings.com/browse.html?page={}&sort=5&numrev=2'.format(i)
            request = scrapy.Request(url=url, callback=self.parseGamesList)
            yield request

        # step 2: from 2011 to 2019 every 70 pages
        for i in range (2011, 2020):
            for j in range (0, 70):
                url = 'https://www.gamerankings.com/browse.html?year={}page={}&sort=5&numrev=2'.format(i, j)
                request = scrapy.Request(url=url, callback=self.parseGamesList)
                yield request


    # parse lists in the page into seperate games
    def parseGamesList(self, response):
        try:
            for link in response.xpath('//div[@class="body"]/table/tr/td[3]/a/@href').extract():
                link = '/'.join(link.split('/')[:-1])
                url = 'http://www.gamerankings.com' + link + '/articles.html'
                request = scrapy.Request(
                    url=url, 
                    callback=self.parseGame)
                yield request
        except IndexError:
            pass

    # extract article from review page and store into the object
    def parseGame(self, response):
        try:
            reviews = response.xpath('//table[@class="release"]/tbody/tr')
            for review in reviews:
                # prepare the object to store
                item = ReviewItem()
                
                # article extractor borrowed from https://github.com/misja/python-boilerpipe
                link = review.xpath('.//td[3]/a/@href').extract()[0]
                try:
                    extractor = Extractor(extractor='ArticleExtractor', url=link)
                    item['content'] = extractor.getText()
                except Exception as e:
                    item['content'] = str(e)

                # detailed informations
                item['source'] = review.xpath('.//td[1]/a/text()').extract()[0]
                item['date'] = review.xpath('.//td[2]/text()').extract()[0]
                item['game_name'] = response.xpath('//h1/text()').extract()[0]
                item['game_tag'] = response.xpath('//div[@class="crumbs"]/a/text()').extract()
                item['score'] = review.xpath('.//td[4]/text()').extract()[0]
                item['url'] = link
                print(item)

                # send to pipeline
                yield item
        except IndexError:
            pass