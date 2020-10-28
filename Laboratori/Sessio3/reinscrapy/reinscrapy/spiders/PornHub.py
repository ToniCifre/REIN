import scrapy


class PornhubSpider(scrapy.Spider):
    name = 'PornHub'
    allowed_domains = ['Pornhub.com', 'es.pornhub.com']
    start_urls = ['https://es.pornhub.com']

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
            doc['url'] = response.urljoin(data.css('span a::attr(href)').extract_first())
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
        # if self.nPage < 100:
        #     self.nPage += 1
        #     next_page = response.urljoin(f'video?page={self.nPage}')
        #     print(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        # else:
        #     print('sdfkljghskjdfhgjklshdfkljghskldfjh')

    def parse_detail(self, response):
        """
        Parses the information of the TFG detailed page

        :param response:
        :return:
        """
        detail = response.meta

        yield detail
