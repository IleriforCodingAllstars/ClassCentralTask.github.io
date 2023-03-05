import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from pathlib import Path
from ..items import ClasscentralcloneItem


class WebpageSpider(scrapy.Spider):
    name = "webpage"
    allowed_domains = [""]

    start_urls = [
        'https://www.classcentral.com/'
    ]

    def parse(self, response):
        # Link Extractor
        page_urls = LinkExtractor(allow_domains=(r"universities/",
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
                                                 r"help/",),
                                  tags=("a", "img", "buttons")).extract_links(response)
        for page in page_urls:
            yield Request(page.url, callback=self.parse_item)

    def parse_item(self, response):
        # Saving the pages
        page = response.url.split("/")[-2]
        filename = f'{page}.html'
        Path(filename).write_bytes(response.body)

        # Saving the images
        img_url = response.css("img").xpath("@src").get()
        svg_url = response.css("src").xpath("@src").get()
        item = ClasscentralcloneItem()
        item["image_urls"] = [img_url]
        item["image_urls"] = [svg_url]
        yield item
