import datetime
import urllib3
import cssutils

from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup


def retroland_main():
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
    fg.title('Retro Land - Nagy Cikkek')
    fg.link(href='https://retro.land', rel='alternate')
    fg.subtitle('Retro Land')
    fg.language('hu')

    # iterate through all of the elements
    for element in div_mainpage:
        # add each new item to the feed
        fe = fg.add_entry()

        title = element.find('a', class_='title')

        # for the image links we'll have to use the cssutils module
        image = element.find('a')['style']
        style = cssutils.parseStyle(image)
        image_url = style['background-image']
        # adding the feed_url to the beginning of the image link so it will work correctly in the feed
        image_url = image_url.replace('url(', '').replace(')', '')

        # creating article url
        article_url = element.find('a', class_='more', href=True)
        article_url = feed_url + article_url['href']

        lead = element.find('p', class_='lead')

        lead_text = lead.text.replace('tovább...', )

        fe.title(title.text)
        fe.description("<p><img src=" + '"' + image_url + '"' + "/></p>" + lead.text)
        fe.link(href=article_url)

    # fg.rss_file('retroland.xml')  # Write the RSS feed to a file


def retroland_napi():
    # urllib3
    http = urllib3.PoolManager()

    # url to generate feed from
    feed_url = 'https://retro.land/napi-retro'
    # get contents of webpage in utf-8
    html_text = http.request('GET', feed_url).data.decode('utf-8')
    # run it through the html.parser
    soup = BeautifulSoup(html_text, 'html.parser')

    # find articlebox css class (this is where the articles are stored)
    div_dailylist = soup.findAll('div', id='dailyList')

    # create feedgenerator
    fg = FeedGenerator()
    fg.id(feed_url)
    fg.title('Retro Land - Napi Retro')
    fg.link(href='https://retro.land/napi-retro', rel='alternate')
    fg.subtitle('Retro Land - Napi Retro')
    fg.language('hu')

    # iterate through all of the elements
    for element in div_dailylist:
        # add each new item to the feed
        fe = fg.add_entry()

        title = "retro.land - napi retro cikk"

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
        # fe.enclosure(url='"' + image_url + '"', type="image")
        fe.link(href=article_url)

    fg.rss_file('rss.xml')  # Write the RSS feed to a file


if __name__ == '__main__':
    retroland_main()
    # retroland_napi()
