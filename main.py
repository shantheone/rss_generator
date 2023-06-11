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
        image = element.find('a', class_='image')
        # print(str(image).split("src=")[1].split('"')[1])
        image_url = "https://retro.land" + str(image).split("src=")[1].split('"')[1]
        # adding the feed_url to the beginning of the image link so it will work correctly in the feed

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

    # URL to generate feed from
    feed_url = 'https://retro.land/napi-retro'
    # Get contents of webpage in utf-8
    html_text = http.request('GET', feed_url).data.decode('utf-8')
    # Run it through the html.parser
    soup = BeautifulSoup(html_text, 'html.parser')

    # Create feedgenerator
    fg = FeedGenerator()
    fg.id(feed_url)
    fg.title('Retro Land - Napi Retro')
    fg.link(href='https://retro.land/napi-retro', rel='alternate')
    fg.subtitle('Retro Land - Napi Retro')
    fg.language('hu')

    # Array to hold article dictionary
    daily_articles = []

    # Generate the article URL
    for div in soup.findAll('p', attrs={'class':'note'}):
        notes = str(div)
        if notes.__contains__("napi-retro"):
            article_dict = {"url": "https://retro.land/napi-retro" + notes.split("napi-retro")[1].split('"')[0]}
            daily_articles.append(article_dict)

    # Generate article content
    i = 0
    for div in soup.findAll('div', attrs={'itemprop':['articleBody']}):
        # Lead text
        daily_articles[i].update({"lead": div})

        # title
        title = (str(div).split("title")[1]).split('"')[1]
        daily_articles[i].update({"title": title})

        # Increment the array index by 1
        i += 1

    # Build the rest of the feed
    for item in daily_articles:
        fe = fg.add_entry()
        description = ''
        for key,value in item.items():
            if key == 'url':
                fe.link(href=value)
                fe.id(value)
            if key == 'title':
                fe.title(value)
            if key == 'lead':
                description = description + str(value)
                fe.description(description)

    fg.rss_file('retroland-daily.xml', pretty=True)  # Write the RSS feed to a file


if __name__ == '__main__':
    retroland_main()
    retroland_napi()
