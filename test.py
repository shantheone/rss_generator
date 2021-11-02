import urllib3
import cssutils
from dataclasses import dataclass

from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup
from urllib3.filepost import encode_multipart_formdata

@dataclass
class article:
    url: str
    lead: str

def retroland_napi():
    # urllib3
    http = urllib3.PoolManager()

    # url to generate feed from
    feed_url = 'https://retro.land/napi-retro'
    # get contents of webpage in utf-8
    html_text = http.request('GET', feed_url).data.decode('utf-8')
    # run it through the html.parser
    soup = BeautifulSoup(html_text, 'html.parser')

    daily_articles = []

    # URL
    for div in soup.findAll('p', attrs={'class':'note'}):
        notes = str(div)
        if notes.__contains__("jelenleg"):
            article_dict = {"url": "https://retro.land" + (notes.split("jelenleg")[1]).split('"')[1]}
            daily_articles.append(article_dict)

    # Article content
    i = 0
    for div in soup.findAll('div', attrs={'class':['editable component', 'cols component']}):
        # Image
        image = "https://retro.land/" + (str(div).split('src=')[1].split('../../../../')[1])[:-2]
        daily_articles[i].update({"image": image})
        
        # Lead text
        daily_articles[i].update({"lead": div.text})
        
        # Title
        title = (str(div).split("title")[1]).split('"')[1]
        daily_articles[i].update({"title": title})
        
        # Increment the array index by 1
        i += 1

    for item in daily_articles:
        for key,value in item.items():
            print(key, ':', value)
            
        print()


if __name__ == '__main__':
    retroland_napi()