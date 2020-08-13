import datetime
import csv

POSTER_INFO_TABLE = 'posterinfo'

MEDIA_PLAY_SRC_TABLE = 'media_src'

MEDIA_META_TABLE = 'media_meta'

def toText(orig):
    strs=orig.split(':')
    if len(strs)>1:
        return strs[1].replace(' ','')
    else:
        return orig.replace(' ','')


def log(msg):
    print(msg)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file = open('log.csv', 'a+', newline='')
    writer = csv.writer(file)
    writer.writerow([msg, now])
    file.close()