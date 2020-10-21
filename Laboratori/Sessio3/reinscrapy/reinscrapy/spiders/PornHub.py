import scrapy


class PornhubSpider(scrapy.Spider):
    name = 'PornHub'
    allowed_domains = ['Pornhub.com']
    start_urls = ['http://es.pornhub.com']

    def parse(self, response):
        """
        Process the information of each page of TFGs

        :param response:
        :return:
        """

        for tfg in response.css('li.videoBox'):
            doc = {}
            data = tfg.css('div.wrap div.thumbnail-info-wrapper')
            doc['title'] = str(data.css('span a::text').extract_first()).replace('\n', '').replace('  ', '')
            doc['url'] = data.css('span a::attr(href)').extract_first()
            doc['author'] = data.css('div.videoUploaderBlock div a::text').extract_first()
            doc['views'] = data.css('div.videoDetailsBlock span var::text').extract_first()
            doc['rating'] = data.css('div.videoDetailsBlock div div.value::text').extract_first()

            yield doc

    def parse(self, response):
        """
        Process the information of each page of TFGs

        :param response:
        :return:
        """

        for tfg in response.css('li.videoBox'):
            doc = {}
            data = tfg.css('div.wrap div.thumbnail-info-wrapper')
            doc['title'] = str(data.css('span a::text').extract_first()).replace('\n', '').replace('  ', '')
            doc['url'] = data.css('span a::attr(href)').extract_first()
            doc['author'] = data.css('div.videoUploaderBlock div a::text').extract_first()
            doc['views'] = data.css('div.videoDetailsBlock span var::text').extract_first()
            doc['rating'] = data.css('div.videoDetailsBlock div div.value::text').extract_first()

            yield doc

        next = response.css('li.page_next a::attr(href)').extract_first()
        if next is not None:
            next_page = response.urljoin(next)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            print('sdfkljghskjdfhgjklshdfkljghskldfjh')
