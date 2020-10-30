import scrapy
from scrapy.selector import Selector


class MejortorrentSpider(scrapy.Spider):
    name = 'MejorTorrent'
    allowed_domains = ['mejortorrentt.net']
    n_page = 1
    start_urls = [f'http://www.mejortorrentt.net/secciones.php?sec=descargas&ap=peliculas&p={n_page}']

    def parse(self, response):
        """
        Process the film link of each page

        :param response:
        :return:
        """
        print(f'[INFO]: Number of page {self.n_page}')
        for box in response.css('td.main_table_center_content_td'):
            for films in box.css('a::attr(href)').getall():
                link = response.urljoin(films)
                yield scrapy.Request(link, callback=self.parse_film_detail)

        if int(response.request.url.split('=')[-1]) == self.n_page:
            self.n_page += 1
            next_page = response.urljoin(f'secciones.php?sec=descargas&ap=peliculas&p={self.n_page}')
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            print('-----------------------------------')
            print(response.request.url.split('='), self.n_page)

    def parse_film_detail(self, response):
        """
        Parses the information of the film

        :param response:
        :return:
        """
        doc = {}
        sel = Selector(response).xpath('//*[@id="main_table_center_center1"]/table/tr/td[2]/table/tr/td[1]')

        aux = [str(k).replace('\n', '').replace('\t', '').replace('\r', '').lstrip()
               for k in sel.css('*::text').getall()]
        aux = [k for k in aux if k != '']

        info_list = ['Género', 'Año', 'Director', 'Actores', 'Formato',
                     'Total Descargas', 'Fecha', 'Tamaño', 'Descripción']
        info_title = 'title'
        for data in aux:
            if info_title != '':
                doc[info_title] = data
                info_title = ''
            elif ':' in data:
                info_title = data.replace(':', '').replace(' ', '')
                if info_title not in info_list:
                    info_title = ''

        yield scrapy.Request(response.urljoin(sel.css('a::attr(href)').getall()[0]),
                             callback=self.parse_torrent, meta=doc)

    def parse_torrent(self, response):
        """
        Parses the download link of torrent

        :param response:
        :return:
        """
        detail = response.meta
        sel = Selector(response).xpath('//*[@id="contenido_descarga"]/table/tr/td[1]/table/tr/td[1]')

        link = sel.css('a::attr(href)').getall()
        if len(link) != 0:
            detail['download'] = response.urljoin(str(link[0]))

        yield detail
