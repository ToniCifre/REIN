import scrapy
from scrapy.selector import Selector


class SensaCineSpider(scrapy.Spider):
    n_page = 1
    name = 'SensaCine'
    allowed_domains = ['sensacine.com']
    start_urls = [f'http://www.sensacine.com/peliculas/mejores/nota-espectadores/?page={n_page}']

    def parse(self, response):
        """
        Process the information of each page of films

        :param response:
        :return:
        """
        print(f'[INFO]: Number of page {self.n_page}')

        for film in response.css('div.img_side_content'):
            doc = {}
            data = film.css('div.content')
            doc['Titulo'] = str(data.css('div.titlebar_02 h2 a::text').extract_first()).replace('\n', '')
            doc['URL'] = response.urljoin(film.css('a::attr(href)').extract_first())
            doc['Image'] = film.css('img::attr(src)').extract_first()
            for info in data.css('ul li'):
                title = info.css('span::text').extract_first().replace(':', '').lstrip()
                inf = [k.replace('\n', '').replace(' ', '') for k in info.css('div.oflow_a *::text').extract() if k != '\n']
                doc[title] = ''.join(inf)

            for eval in data.css('div.margin_10v span.stars_medium '):
                ev = [k.replace('\n', '').lstrip() for k in eval.css('span.eval_source *::text').extract() if k != '\n']
                doc[''.join(ev)] = eval.css('span.note *::text').extract_first()

            yield scrapy.Request(doc['URL'], callback=self.parse_detail, meta=doc)
            # yield doc

        if self.n_page == 1 or int(response.request.url.split('=')[-1]) == self.n_page:
            self.n_page += 1
            next_page = response.urljoin(f'/peliculas/mejores/nota-espectadores/?page={self.n_page}')
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            print('-------------- End Of Scraper --------------')

    def parse_detail(self, response):
        """
        Parses the information of the film detailed page

        :param response:
        :return:
        """
        detail = response.meta
        sinopsis = [k.replace('\n', '').replace('  ', '')
                    for k in response.css('section.ovw-synopsis div.content-txt *::text').extract() if k != '\n']
        detail['Sinopsis'] = ''.join(sinopsis)

        yield detail
