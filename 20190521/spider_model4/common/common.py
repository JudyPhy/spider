import datetime
import csv


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


def toMonth(text_month):
    if text_month == 'January':
        return 1
    elif text_month == 'February':
        return 2
    elif text_month == 'March':
        return 3
    elif text_month == 'April':
        return 4
    elif text_month == 'May':
        return 5
    elif text_month == 'June':
        return 6
    elif text_month == 'July':
        return 7
    elif text_month == 'September':
        return 9
    elif text_month == 'October':
        return 10
    elif text_month == 'November':
        return 11
    elif text_month == 'December':
        return 12
    return 0