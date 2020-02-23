import scrapy
from time import sleep

class contentFetch(scrapy.Spider):
    name="get_content"
    join_dict = lambda self,a,b: dict(list(a.items())+list(b.items()))

    def header_fetch(self, article):
        content = {}
        content['title'] = article.css('h1::text').extract_first()
        content['subtitle'] = article.css('h2::text').extract_first()
        content['title_img'] = article.css('img::attr(src)').extract_first()
        content['author_img'] = article.css('a::attr(href)').extract_first()
        content['author_name'] = article.css('img::attr(alt)').extract_first()
        date_length_div = article.css('span')[3]
        content['date'] = date_length_div.css('a::text').get()
        text_selector_array = date_length_div.css('div::text')[-2:]
        text_array = map(lambda x: x.get(), text_selector_array)
        content['duration'] = ''.join(text_array)
        return content

    def parse(self, response):
        content = {}
        article = response.css('article')
        content = self.scrape_it_all(response)
        yield content

    def scrape_it_all(self, response):
        csslinks = '\n'.join([i.get() for i in response.css('link')])
        styles = '\n'.join([i.get() for i in response.css('style')])
        article = response.css('article')[0].get()
        scripts = '\n'.join([i.get() for i in response.css('script')])
        html = """
            <html>
                <head>
                    {}
                </head>
                <body>
                    {}
                    {}
                    {}
                </body>
            </html>
        """.format(csslinks,article,styles,scripts)
        # self.logger.info('HTML is\n',html)
        # For storing the html content in a file
        # import os
        # path = os.path.join('html',response.url.split('/')[-1]+'.html')
        # with open(path,'w') as f:
        #     f.write(html)

        body = '\n'.join((article,styles,scripts))
        body = body.replace('<noscript>','').replace('</noscript>','')
        return {
            'head': csslinks,
            'body': body
        }
