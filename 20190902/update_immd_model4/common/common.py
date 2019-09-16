import datetime
import csv

words = ['WV', 'WV-A', 'PU', 'WX-A', 'WX', 'UR', 'FE', 'DISQ', 'TNP', 'DNF', '', 'WXNR']


def toDateTime(time_str):  # time_str: %Y-%m-%d %H:%M:%S
    return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

def toDoubleDigitStr(interger):
    v_char=str(interger)
    while len(v_char) < 2:
        v_char='0'+v_char
    return v_char


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


def GetTotalSeconds(time_text):
    seconds = 0
    array_time = []
    array1 = time_text.split('.')
    for item1 in array1:
        array2 = item1.split(':')
        for item2 in array2:
            array_time.append(item2)
    if len(array_time) == 3:
        seconds = int(array_time[0]) * 60 + int(array_time[1]) + int(array_time[2]) / 100
    elif len(array_time) == 2:
        seconds = int(array_time[0]) + int(array_time[1]) / 100
    elif len(array_time) == 1:
        seconds = int(array_time[0]) / 100
    return seconds
