import datetime
import urllib3
import cssutils
from rfeed import *
from bs4 import BeautifulSoup

# item1 = Item(
#     title="Napi Retro",
#     link="https://retro.land/napi-retro",
#     description="This is the description of the first article",
#     author="Shan",
#     guid=Guid("https://retro.land/napi-retro"),
#     pubDate=datetime.datetime(2021, 8, 7, 10, 00))
#
# feed = Feed(
#     title="Sample RSS Feed",
#     link="http://www.example.com/rss",
#     description="This is an example of how to use rfeed to generate an RSS 2.0 feed",
#     language="en-US",
#     lastBuildDate=datetime.datetime.now(),
#     items=[item1])

if __name__ == '__main__':
    # print(feed.rss())

    # urllib3
    http = urllib3.PoolManager()

    # url to generate feed from
    feed_url = 'https://retro.land'
    # get contents of webpage in utf-8
    html_text = http.request('GET', feed_url).data.decode('utf-8')
    # run it through the html.parser
    soup = BeautifulSoup(html_text, 'html.parser')

    # Find articlebox css class (this is where the articles are stored)
    div_mainpage = soup.findAll('div', class_='articleBox')

    # iterate through all of the elements
    for element in div_mainpage:
        print()
        title = element.find('a', class_='title')
        print('Title     :', title.text)
        print('Scanned   :', datetime.datetime.now())

        # for the image links we'll have to use the cssutils module
        image = element.find('a')['style']
        style = cssutils.parseStyle(image)
        image_url = style['background-image']
        # adding the feed_url to the beginning of the image link so it will work correctly in the feed
        image_url = image_url.replace('url(', feed_url).replace(')', '')
        print('Image url :', image_url)

        lead = element.find('p', class_='lead')
        print('Lead      :', lead.text)

        # results.append(title.text)
