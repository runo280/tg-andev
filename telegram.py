import os

import requests

bot_token = os.environ['bot_token']
channel_id = os.environ['channel_id']
admin_id = os.environ['chat_id']
footer = os.environ['footer']


def msg_to_admin(args):
    text_caps = ''.join(args)
    requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(bot_token, 'sendMessage'),
        data={'chat_id': admin_id, 'text': text_caps}
    )


def send_article(title, link, date):
    message = '<a href="{link}">{title}</a>\n\n<pre>{date}</pre>\n\n{footer}' \
        .format(title=title, link=link, date=date,
                footer=footer)
    return requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(bot_token, 'sendMessage'),
        data={'chat_id': channel_id, 'text': message, 'parse_mode': 'HTML'}
    )
