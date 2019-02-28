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

