import time
import datetime


def parse_date(dateStr:str, split=''):
    # print(f'解析字符串：【{dateStr}】，分隔符：【{split}】')
    # 把中文年月日时分替换
    dateList = dateStr.split(split)
    parseRes = []
    for _date in dateList:
        parseRes.append(time.mktime(time.strptime(_date, "%Y年%m月%d日 %H时%M分")))
    return parseRes


def get_x_day_ago_zero_timestamp(days):
    """
    获取days天之前0点的时间戳
    :param days:
    :return:
    """
    # 先获得时间数组格式的日期
    threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=days))
    # 转换为其他字符串格式
    otherStyleTime = threeDayAgo.strftime("%Y-%m-%d")
    # 转换为时间戳
    timeStamp = time.mktime(time.strptime(otherStyleTime, '%Y-%m-%d'))
    return timeStamp
