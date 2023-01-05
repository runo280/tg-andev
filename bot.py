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
        send = telegram.send_article(title, link, date)
        result = send.json()
        if result['ok'] is True:
            print('ok')
            db.feeds.update_one({'link': link}, set_published_query)
        else:
            print('failed to publish')
            telegram.msg_to_admin('🚫 failed to publish: ' + ':\n' + link)
