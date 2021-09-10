import urllib3
import cssutils

from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup
from urllib3.filepost import encode_multipart_formdata


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

        lead_text = lead.text.replace('tovább...', '')

        fe.title(title.text)
        fe.description("<p><img src=" + '"' + image_url + '"' + "/></p>" + lead_text)
        fe.id(article_url)
        fe.link(href=article_url)

    fg.rss_file('retroland-main.xml', pretty=True)  # Write the RSS feed to a file


def retroland_napi():
    # urllib3
    http = urllib3.PoolManager()

    # url to generate feed from
    feed_url = 'https://retro.land/napi-retro'
    # get contents of webpage in utf-8
    html_text = http.request('GET', feed_url).data.decode('utf-8')
    # run it through the html.parser
    soup = BeautifulSoup(html_text, 'html.parser')

    # find articleBody itemprop (this is where the articles are stored)
    div_columnns = soup.findAll('div', itemprop='articleBody')

    # create feedgenerator
    fg = FeedGenerator()
    fg.id(feed_url)
    fg.title('Retro Land - Napi Retro')
    fg.link(href='https://retro.land/napi-retro', rel='alternate')
    fg.subtitle('Retro Land - Napi Retro')
    fg.language('hu')

    # iterate through all of the elements
    for element in div_columnns:
        # add each new item to the feed
        fe = fg.add_entry()

        article_url_all = element.findAll('a')
        if (len(article_url_all) == 2):
            article_url = str(article_url_all[1])
        else:
            article_url = str(article_url_all)

        if (article_url.endswith('>')):
            article_url = "https://retro.land" + (article_url.split('=')[1]).split('"')[1]
        
        if (article_url.endswith(']')):
            article_url = "https://retro.land/" + (article_url.split('<a href="/')[1].split('"')[0])

        fe.link(href=article_url)
        fe.id(article_url)

        lead = element.findAll('p')

        for lead_element in lead:
            lead_element.find('p', class_='')
            if (not lead_element.text.startswith('Forrás')) and (len(lead_element.text) != 0):
                lead_text = lead_element.text

        fe.title(element.find('img')['title'])

        enclosure = element.find('img')['src']
        enclosure = "https://retro.land" + enclosure

        fe.description("<p><img src=" + '"' + enclosure + '"' + "/></p>" + lead_text)

    fg.rss_file('retroland-daily.xml', pretty=True)  # Write the RSS feed to a file


if __name__ == '__main__':
    retroland_main()
    retroland_napi()
