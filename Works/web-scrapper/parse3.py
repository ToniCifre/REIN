def parse(self, response):
    """
    Process the information of each page of TFGs

    :param response:
    :return:
    """

    for tfg in response.css('li.ds-artifact-item'):
        doc = {}
        data = tfg.css('div.artifact-info')
        doc['title'] = tfg.css('h4 a::text').extract_first()
        doc['url'] = response.urljoin(tfg.css('h4 a::attr(href)').extract_first())
        doc['author'] = data.css('span.author span::text').extract_first()
        doc['publisher'] = data.css('span.publisher::text').extract_first()
        doc['date'] = data.css('span.date::text').extract_first()
        doc['rights'] = data.css('span.rights::text').extract_first()
        doc['abstract'] = data.css('div.artifact-abstract::text').extract_first()

        yield scrapy.Request(doc['url'], callback=self.parse_detail, meta=doc)

    next = response.css('a.next-page-link::attr(href)').extract_first()
    if next is not None:
        next_page = response.urljoin(next)
        yield scrapy.Request(next_page, callback=self.parse)

def parse_detail(self, response):
    """
    Parses the information of the TFG detailed page

    :param response:
    :return:
    """
    detail = response.meta
    detail['description'] = ' '.join(response.css('div.expandable::text').extract())
    detail['keywords'] = ' '.join(response.css('div.descripcio a::text').extract())

    yield detail
