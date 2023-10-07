import time

def parse_date(dateStr:str, split=''):
    # print(f'解析字符串：【{dateStr}】，分隔符：【{split}】')
    # 把中文年月日时分替换
    dateList = dateStr.split(split)
    parseRes = []
    for _date in dateList:
        parseRes.append(time.mktime(time.strptime(_date, "%Y年%m月%d日 %H时%M分")))
    return parseRes
