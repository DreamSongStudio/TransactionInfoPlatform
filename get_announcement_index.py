import random
import requests
import time
import re

from bs4 import BeautifulSoup
from get_announcement_detail import get_announcement_detail
from models.Constant import StopType
from utils.Common import GLOBAL_URI, HEADERS
from utils.FormatDate import get_x_day_ago_zero_timestamp


def get_announcement_index(module, stopUrl):
    """
    解析对应url板块下的公告目录，并翻页
    用子线程去解析对应的detail
    直到解析到库中该类最新的{项目编号-标题-时间}为止
    :param module: DataModule
    :param stopFlag: 模块名
    :return:
        detailIndex: [{announcement_info1}, {announcement_info2}]
        detailMap: {%url: {announcement_detail}, }
    """
    detailIndex = []
    detailMap = {}
    # 停止标识
    if stopUrl == '':
        # 说明找不到上一条记录，为防止频率太高而被ban，这里限制为只爬取近7天的数据
        # 对初次运行数据获取的场景也适用
        stopType = StopType.DATE.value
        stopDate = get_x_day_ago_zero_timestamp(1)
    else:
        stopType = StopType.URL.value
        stopDate = 0
    # stopUrl = '/jyywjsgcfwjzzbgg/961987.jhtml'
    checkStopUrl = ''
    checkStopDate = 9999999999
    curPage = 1
    print(f'检查模式：{stopType}，时间点：{stopDate}，URL点：{stopUrl}')
    while not check_loop_stop(stopType, stopUrl, stopDate, checkStopUrl, checkStopDate):
        # 页号

        curPageStr = ''
        if curPage > 1:
            curPageStr = f'_{curPage}'
        print(f'正在解析第{curPage}页: {GLOBAL_URI}/{module["name"]}/index{curPageStr}.jhtml')
        reqIndex = requests.get(f'{GLOBAL_URI}/{module["name"]}/index{curPageStr}.jhtml', HEADERS)
        soup = BeautifulSoup(reqIndex.text, 'lxml')
        # 获取目录页中的数据列表
        tb = soup.tbody
        for item in tb.children:
            _a = item.find('a')
            # print(_a)
            if type(_a) != int:
                # 解析 [项目编号，项目名称，发布时间]
                r = re.search('\\n(\[.*?\])\\n(.*?)\\n(\d{4}-\d{1,2}-\d{1,2})\\n', item.text.replace(' ', ''))
                textMatchResult = r.groups()
                projectNo = textMatchResult[0].replace('[', '').replace(']', '')
                release_timestamp = time.mktime(time.strptime(textMatchResult[2], '%Y-%m-%d'))
                # 如果遍历到停止点则跳出
                checkStopUrl = _a['href']
                checkStopDate = release_timestamp
                if check_loop_stop(stopType, stopUrl, stopDate, checkStopUrl, checkStopDate):
                    break

                detailIndex.append({'url': _a['href'],
                                    'module': module['code'],
                                    'project_no': projectNo,
                                    'release_date': textMatchResult[2],
                                    'release_timestamp': release_timestamp,
                                    'title': textMatchResult[1],
                                    })
                print(textMatchResult[1])
                # 暂时跳过”补充公告“和“暂停公告”的详情解析
                if "补充公告" in textMatchResult[1] \
                        or "暂停公告" in textMatchResult[1] \
                        or "延期公告" in textMatchResult[1] \
                        or "失败公告" in textMatchResult[1] \
                        or "终止招投标" in textMatchResult[1] \
                        or "终止公告" in textMatchResult[1]:
                    print(f'跳过')
                    continue
                _detail = get_announcement_detail(f'{GLOBAL_URI}/{_a["href"]}')
                if _detail:
                    detailMap[checkStopUrl] = _detail

                # detail解析之间加一个短期sleep
                time.sleep(random.randint(1, 3))

        curPage += 1
    print('此次获取新数据：')
    for i in detailIndex:
        print(i)
        if i['url'] in detailMap:
            print(detailMap[i['url']])
        print('----------------')

    return detailIndex, detailMap


def check_loop_stop(stop_type, url_ed, date_ed, url_flag, date_flag):
    """
    根据停止类型不同，进行判断爬虫循环是否停止
    :param stop_type:   停止类型
    :param url_ed:      停止URL
    :param date_ed:     停止时间戳
    :param url_flag:    当前URL
    :param date_flag:   当前时间戳
    :return:
    """
    if stop_type == StopType.URL.value:
        return url_ed == url_flag
    else:
        return date_ed > date_flag


