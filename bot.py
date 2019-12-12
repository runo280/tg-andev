# -*- coding: utf-8 -*-

import db
import telegram

if __name__ == '__main__':

    unpublished_query = {'is_pub': False}
    set_published_query = {'$set': {'is_pub': True}}
    for x in db.feeds.find(unpublished_query):
        title = x['title']
        link = x['link']
        date = x['date']
        telegram.send_article(title, link, date)
        db.feeds.update_one({'link': link}, set_published_query)
