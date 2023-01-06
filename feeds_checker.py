from rss import *

if __name__ == '__main__':
    lines = get_feeds_url()
    index = 0
    for line in lines:
        if line.startswith('#'):
            continue
        index += 1
        print('Processing feed #' + str(index) + ' : ' + line)
        is_url_ok(line, True)
