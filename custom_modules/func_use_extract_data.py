import pandas as pd
import re

import custom_modules.func_analysis as analysis


def startsWithDateTime(s):
    pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4})(,)? ([0-9])|([0-9]):([0-9][0-9]) '
    result = re.match(pattern, s)
    if result:
        return True
    return False


# used to verify the string(s) contains 'Author' or not with the help of regular expressions.
def startsWithAuthor(s):
    pattern = '^([\w()\[\]-]+):|([\w]+[\s]+([\w()\[\]-]+)):'
    result = re.match(pattern, s)
    if result:
        return True
    return False


#  Use to extract the date, time, author and message from line.
def getDataPoint(line):
    splitLine = line.split(' - ') 
    dateTime = splitLine[0] 
    if ',' not in dateTime:
        dateTime = dateTime.replace(' ', ', ', 1)
    date, time = dateTime.split(', ') 
    if "am" in time:
        time = time.replace("am", "")
    elif "pm" in time:
        time = time.replace("pm", "")
        time = time.split(':') 
        time[0] = str(int(time[0]) + 12)
        time = ':'.join(time)
    message = ' '.join(splitLine[1:]) 
    if startsWithAuthor(message): # True
        splitMessage = message.split(': ') 
        author = splitMessage[0]
        message = ' '.join(splitMessage[1:]) 
    else:
        author = None
    return date, time, author, message


#  used to return the extracted data from txt file.
def read_data(file_contents, date_format):
    date_formats_dict = {'mm/dd/yyyy': '%m/%d/%Y', 'mm/dd/yy': '%m/%d/%y',
                         'dd/mm/yyyy': '%d/%m/%Y', 'dd/mm/yy': '%d/%m/%y',
                         'yyyy/mm/dd': '%Y/%m/%d', 'yy/mm/dd': '%y/%m/%d'}
    data = []
    messageData = [] 
    date, time, author = None, None, None 
    for line in file_contents:
        line = line.strip() 
        if startsWithDateTime(line): 
            if len(messageData) > 0:
                data.append([date, time, author, ' '.join(messageData)]) 
            messageData.clear() 
            date, time, author, message = getDataPoint(line) 
            messageData.append(message) 
        else:
            messageData.append(line)
    df = pd.DataFrame(data, columns=['Date', 'Time', 'Author', 'Message'])
    df["Date"] = pd.to_datetime(df["Date"], format=date_formats_dict[date_format])
    df['emoji'] = df["Message"].apply(analysis.extract_emojis)
    
    return df