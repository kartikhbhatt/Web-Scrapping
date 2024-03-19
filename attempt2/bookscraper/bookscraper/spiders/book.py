import scrapy


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()

            if 'catalogue/' not in relative_url:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/' + relative_url
            
            yield response.follow(book_url, callback= self.parse_book_page)


        # to travel to next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' not in next_page:   
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/' + next_page
            yield response.follow(next_page_url, callback=self.parse)




    def parse_book_page(self, response):
        table_rows = response.css('table tr')

        yield{
            'url': response.url,
            'title': response.css('.product_main h1::text').get(),
            'product_type' : table_rows[1].css('td::text').get(),
            'category' : response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'stars' : response.css('p.star-rating::attr(class)').get(),
            'price': response.css('p.price_color::text').get(),
            'price_exc_tax': table_rows[2].css('td::text').get(),
            'price_inc_tax': table_rows[3].css('td::text').get(),
            'tax': table_rows[4].css('td::text').get(),
            'availability': table_rows[5].css('td::text').get(),
            'num_reviews': table_rows[6].css('td::text').get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),

        }