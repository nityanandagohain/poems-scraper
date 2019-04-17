# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from ..items import PoemsScraperItem

class PoemsSpider(scrapy.Spider):
    name = 'poems'
    # start_urls = ['https://www.poets.org/poetsorg/poems?field_poem_themes_tid=886']
    page_no = 1
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["theme","poem"],
    }
    def __init__(self, *args, **kwargs): 
        super(PoemsSpider, self).__init__(*args, **kwargs) 

        print(kwargs.get('theme_id'))
        self.start_urls = ["https://www.poets.org/poetsorg/poems?field_poem_themes_tid={}".format(kwargs.get('theme_id'))]

    def parse(self, response):    
        max_pages = int(getattr(self,'max_pages'))
        theme = response.css(".title")[0].xpath("text()")[0].extract()
        bsObj = BeautifulSoup(response.text,"lxml")
        poems_tds = bsObj.find_all("td")
        for p_link in poems_tds:
            try:
                link = p_link.find("a")['href']
                if "poem" in link:
                    poem_link = "https://www.poets.org{}".format(link)
                    yield response.follow(poem_link, callback=self.parse_poem, meta = {'theme': theme})
            except:
                pass
        next_link = "https://www.poets.org/poetsorg/poems?field_poem_themes_tid=886&page={}".format(PoemsSpider.page_no)
        if PoemsSpider.page_no < max_pages:
            PoemsSpider.page_no += 1
            yield response.follow(next_link, callback=self.parse)
        
    

    def parse_poem(self, response):
        items = PoemsScraperItem()
        items['theme'] = response.meta.get("theme")
        poem = response.css("pre::text").extract()
        if(poem == ''):
            poem = response.css("#poem-content .even").extract()
        poem = "".join(poem)
        poem = re.sub(" +"," ",poem)
        poem = poem.replace("\n"," ").replace("\t","").replace("\r","")
        items['poem'] = poem
        yield items