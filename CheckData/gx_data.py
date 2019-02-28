import urllib.request
import urllib.parse
import json


class Rank:
    year = 0
    month = 0
    day = 0
    count = 0
    race = 0
    name = ''
    site = ''
    cls = 0
    distance = 0
    bonus = 0
    going = ''
    course = ''

    horse_no = 0
    pic = 0
    actual_wt = 0
    declar_horse_wt = 0
    draw = 0
    lbw = ''
    position = ''
    finish_time = ''
    win_odds = 0.0
    place = 0.0

    current_rating = 0
    season_stakes = 0
    total_stakes = 0

    horse_name = ''
    horse_age = 0
    horse_star_0 = 0
    horse_star_1 = 0
    horse_star_2 = 0
    horse_star_3 = 0
    horse_total = 0

    jockey_name = ''
    jockey_age = 0
    jockey_star_0 = 0
    jockey_star_1 = 0
    jockey_star_2 = 0
    jockey_star_3 = 0
    jockey_total = 0

    trainer_name = ''
    trainer_age = 0
    trainer_star_0 = 0
    trainer_star_1 = 0
    trainer_star_2 = 0
    trainer_star_3 = 0
    trainer_total = 0

    race_id = 0
    detailed_id = 0
    # 距离上次参赛的间隔时间，单位天
    rest = 0
    # 负磅的变化值
    act = 0
    # 体重变化值
    dct = 0

    starts0 = 0
    starts1 = 0
    starts2 = 0
    starts3 = 0

    pass


class Arrange:
    year = 0
    month = 0
    day = 0
    site = ''
    count = 0
    race = 0
    cls = 0
    distance = 0
    name = ''
    bonus = 0
    going = ''
    course = ''

    pic = 0
    horse_no = 0
    actual_wt = 0
    declar_horse_wt = 0
    draw = 0
    lbw = ''
    position = ''
    finish_time = ''
    win_odds = 0.0
    place = 0.0
    # horse
    current_rating = 0
    starts0 = 0
    starts1 = 0
    starts2 = 0
    starts3 = 0
    season_stakes = 0
    total_stakes = 0
    #
    horse_name = ''
    jockey_name = ''
    trainer_name = ''
    race_id = 0
    detailed_id = 0
    #
    # 距离上次参赛的间隔时间，单位天
    rest = 0
    # 负磅的变化值
    act = 0
    # 体重变化值
    dct = 0

    def __lt__(self, other):
        if self.year > other.year:
            return False
        else:
            if self.year == other.year:
                if self.month > other.month:
                    return False
                else:
                    if self.month == other.month:
                        if self.day > other.day:
                            return False
                        else:
                            if self.day == other.day:
                                if self.race > other.race:
                                    return False
                                else:
                                    if self.race == other.race:
                                        if self.pic > other.pic:
                                            return False
        return True

    pass


def format_data(source, target):
    for i in source:
        if type(source[i]) is bytes:
            setattr(target, i, source[i].decode('utf8'))
        else:
            setattr(target, i, source[i])
    pass


def query(year_min, year_max):
    url = 'http://spider.local:12345/history?min={0}&max={1}'.format(year_min, year_max)
    f = urllib.request.urlopen(url)
    response = json.loads(f.read().decode('utf-8'))
    result = []
    for single in response:
        arrange = Arrange()
        format_data(single, arrange)
        result.append(arrange)
    result.sort()
    return result
    pass

# 2016-1-1    2018-12-12
def query_rank(time_min, time_max):
    url = 'http://spider.local:12345/new_history?min={0}&max={1}'.format(time_min, time_max)
    f = urllib.request.urlopen(url)
    response = json.loads(f.read().decode('utf-8'))
    result = []
    for single in response:
        rank = Rank()
        format_data(single, rank)
        result.append(rank)
    return result
    pass


def new_odds(time_want):
    url = 'http://spider.local:12345/future?time={0}'.format(time_want)
    f = urllib.request.urlopen(url)
    response = json.loads(f.read().decode('utf-8'))
    result = []
    for single in response:
        arrange = Arrange()
        format_data(single, arrange)
        result.append(arrange)
    result.sort()
    return result
    pass


def new_rank(time_want):
    url = 'http://spider.local:12345/new_future?time={0}'.format(time_want)
    f = urllib.request.urlopen(url)
    response = json.loads(f.read().decode('utf-8'))
    result = []
    for single in response:
        rank = Rank()
        format_data(single, rank)
        result.append(rank)
    return result
    pass


def send_result(val):
    import base64
    base64_encrypt = base64.b64encode(val.encode('utf-8'))
    val = str(base64_encrypt, 'utf-8')
    url = 'http://spider.local:12345/result?val={0}'.format(val)
    f = urllib.request.urlopen(url)
    response = json.loads(f.read().decode('utf-8'))
    print(response)


if __name__ == '__main__':
    print(len(new_odds()))
    # print(len(new_rank()))
    # print(len(query(2018, 2018)))
    print(len(query_rank(2018, 2018)))
