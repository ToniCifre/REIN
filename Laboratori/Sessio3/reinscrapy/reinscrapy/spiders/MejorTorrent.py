import scrapy
from scrapy.selector import Selector


class MejortorrentSpider(scrapy.Spider):
    name = 'MejorTorrent'
    allowed_domains = ['mejortorrentt.net']
    n_page = 10
    start_urls = ['http://www.mejortorrentt.net/secciones.php?sec=descargas&ap=peliculas&p=10']

    def parse(self, response):
        """
        Process the information of each page of TFGs

        :param response:
        :return:
        """

        for box in response.css('td.main_table_center_content_td')[1:2]:
            for films in box.css('a::attr(href)').getall()[1:2]:
                doc = {}
                link = response.urljoin(films)
                yield scrapy.Request(link, callback=self.parse_detail, meta=doc)

        if self.n_page < 10:
            self.n_page += 1
            next_page = response.urljoin(f'secciones.php?sec=descargas&ap=peliculas&p={self.n_page}')
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            print('sdfkljghskjdfhgjklshdfkljghskldfjh')

    def parse_detail(self, response):
        """
        Parses the information of the TFG detailed page

        :param response:
        :return:
        """
        sel = Selector(response).xpath('//*[@id="main_table_center_center1"]/table/tr/td[2]/table/tr/td[1]')

        aux = [str(k).replace('\n', '').replace('\t', '').replace('\r', '').lstrip() for k in sel.css('*::text').getall()]
        aux = [k for k in aux if k != '']

        filter = ['Género', 'Año', 'Director', 'Actores', 'Formato', 'Total Descargas', 'Fecha', 'Tamaño', 'Descripción']
        toni = 'title'
        doc = response.meta
        for t in aux:
            if toni != '':
                doc[toni] = t
                toni = ''
            elif ':' in t:
                toni = t.replace(':', '').replace(' ', '')
                if toni not in filter:
                    toni = ''

        yield scrapy.Request(response.urljoin(sel.css('a::attr(href)').getall()[0]), callback=self.parse_torrent, meta=doc)


    def parse_torrent(self, response):
        """
        Parses the information of the TFG detailed page

        :param response:
        :return:
        """
        detail = response.meta

        sel = Selector(response).xpath('//*[@id="contenido_descarga"]/table/tr/td[1]/table/tr/td[1]')
        for link in sel.css('a::attr(href)').getall():
            detail['download'] = response.urljoin(str(link))

        yield detail
