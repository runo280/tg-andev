import feedparser
import requests

import db
import telegram


def get_feeds_url():
    return [row.rstrip('\n') for row in open('feeds.txt')]


def is_url_ok(url):
    try:
        r = requests.head(url)
        if r.status_code == 200:
            print('Url is OK: ' + url)
            return True
        else:
            print('StatusCode is {}: {} '.format(r.status_code, url))
            telegram.msg_to_admin('❌ StatusCode is ' + str(r.status_code) + ':\n' + url)
            return True
    except requests.ConnectionError:
        print('Failed to connect: ' + url)
        telegram.msg_to_admin('❌ Failed to connect:\n' + url)
        return False


def read_article_feed(feed_url):
    if not is_url_ok(feed_url):
        return
    try:
        feed = feedparser.parse(feed_url)
        print('Count is ' + str(len(feed['entries'])))
        first_crawl = should_published(feed_url)
        for article in feed['entries']:
            title = article['title']
            link = article['link']

            if 'published' in article:
                date = article['published']
            else:
                date = article['updated']

            if 'feedproxy.google.com' in link:
                link = get_redirect_url(link)

            if not is_article_in_db(link):
                add_article_to_db(title, link, date, first_crawl)
    except():
        print()
        telegram.msg_to_admin('❌ Failed to parse:\n' + feed_url)


def get_redirect_url(url):
    return requests.get(url).url


def is_article_in_db(url):
    query = {'link': url}
    if db.feeds.count_documents(query) == 0:
        return False
    else:
        return True


def should_published(url):
    query = {'link': url}
    if db.urls.count_documents(query) == 0:
        new_url = {'link': url}
        x = db.urls.insert_one(new_url)
        return True
    else:
        return False


def add_article_to_db(title, link, date, is_pub):
    article = {'title': title, 'link': link, 'date': date, 'is_pub': is_pub}
    x = db.feeds.insert_one(article)
    print(x.inserted_id)


if __name__ == '__main__':
    lines = get_feeds_url()
    print('Feeds count: ' + str(len(lines)))
    index = 0
    for line in lines:
        if line.startswith('#'):
            continue
        index += 1
        print('Processing feed #' + str(index) + ' : ' + line)
        read_article_feed(line)

    db.mark_as_read_all()