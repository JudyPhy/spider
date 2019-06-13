import datetime
import csv

words = ['WV', 'WV-A', 'PU', 'WX-A', 'WX', 'UR', 'FE', 'DISQ', 'TNP', 'DNF', '']


def toDateTime(time_str):  # time_str: %Y-%m-%d %H:%M:%S
    return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


def toDoubleDigitStr(interger):
    v_char=str(interger)
    while len(v_char) < 2:
        v_char='0'+v_char
    return v_char

def toThreeDigitStr(integer):
    v_char = str(integer)
    while len(v_char) < 3:
        v_char = '0' + v_char
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


def bin_to_str(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in str(s, encoding = "utf-8").split(' ')]])
