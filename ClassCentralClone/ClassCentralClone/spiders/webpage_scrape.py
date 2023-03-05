import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pathlib import Path
from ..items import ClasscentralcloneItem


class WebpageScrapeSpider(CrawlSpider):
    name = "assignment"
    allowed_domains = ["www.classcentral.com"]
    start_urls = ["http://www.classcentral.com/"]

    rules = (
        Rule(LinkExtractor(allow_domains=(r"universities/",
                                          r"university/",
                                          r"providers/",
                                          r"provider/",
                                          r"institutions/",
                                          r"institution/",
                                          r"report/",
                                          r"subjects/",
                                          r"subject/",
                                          r"collection/",
                                          r"rankings/",
                                          r"help/",
                                          )
                           ), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        page = response.url.split("/")[-2]
        filename = f'{page}.html'
        Path(filename).write_bytes(response.body)

        # Saving the images
        img_url = response.css("img").xpath("@src").get()
        svg_url = response.css("src").xpath("@src").get()
        item = ClasscentralcloneItem()
        item["image_urls"] = [img_url]
        item["image_urls"] = [svg_url]

        # item = {}
        # item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        # item["name"] = response.xpath('//div[@id="name"]').get()
        # item["description"] = response.xpath('//div[@id="description"]').get()
        return item
