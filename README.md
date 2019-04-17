## POEMS SCRAPER

#### This scraper scrapes poems.org

### RUN:
* `pip install -r requirements.txt`
* `scrapy crawl poems -a theme_id=886 -a max_pages=2 -o poems.csv`
* The site of animals theme is `https://www.poets.org/poetsorg/poems?field_poem_themes_tid=886`, hence `theme_id=886`
* max_pages is the no of pages you want to scrape, 1 page contains 10 poems. Check the max no of pages available