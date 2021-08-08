import datetime
import urllib3
# import cssutils

from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup


if __name__ == '__main__':
    # urllib3
    http = urllib3.PoolManager()

    # url to generate feed from
    feed_url = 'https://retro.land'
    # get contents of webpage in utf-8
    html_text = http.request('GET', feed_url).data.decode('utf-8')
    # run it through the html.parser
    soup = BeautifulSoup(html_text, 'html.parser')

    # find articlebox css class (this is where the articles are stored)
    div_mainpage = soup.findAll('div', class_='articleBox')

    # create feedgenerator
    fg = FeedGenerator()
    fg.id(feed_url)
    fg.title('Retro Land')
    fg.link(href='https://retro.land', rel='alternate')
    fg.subtitle('Retro Land')
    fg.link(href='https://ds.sandorkovacs.hu/retroland.xml', rel='self')
    fg.language('en')

    # iterate through all of the elements
    for element in div_mainpage:
        # add each new item to the feed
        fe = fg.add_entry()

        title = element.find('a', class_='title')

        # for the image links we'll have to use the cssutils module
        # image = element.find('a')['style']
        # style = cssutils.parseStyle(image)
        # image_url = style['background-image']
        # adding the feed_url to the beginning of the image link so it will work correctly in the feed
        # image_url = image_url.replace('url(', feed_url).replace(')', '')
        # print('Image url :', image_url)

        article_url = element.find('a', class_='more', href=True)
        article_url = feed_url + article_url['href']

        lead = element.find('p', class_='lead')

        fe.title(title.text)
        fe.description(lead.text)
        # fe.id(article_url)
        fe.link(href=article_url)

fg.rss_file('rss.xml')  # Write the RSS feed to a file

