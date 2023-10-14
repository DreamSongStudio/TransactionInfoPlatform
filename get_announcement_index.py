import requests
import time
import re
from bs4 import BeautifulSoup

from get_announcement_detail import get_announcement_detail
from utils.Common import GLOBAL_URI, HEADERS


def get_announcement_index(module):
    """
    解析对应url板块下的公告目录，并翻页
    用子线程去解析对应的detail
    直到解析到库中该类最新的{项目编号-标题-时间}为止
    :param module: 模块名
    :return:
        detailIndex: [{announcement_info1}, {announcement_info2}]
        detailMap: {%projectNo-%title-%release_date: {announcement_detail}, }
    """
    detailIndex = []
    detailMap = {}
    # 停止标识
    # stopFlag = 'JG2023-5649-鳌头镇棋杆社区美丽圩镇建设项目-2023-09-29'
    # 停止标识改为 url
    stopFlag = '/jyywjsgcfwjzzbgg/961982.jhtml'
    checkStopFlag = ''
    curPage = 1
    while checkStopFlag != stopFlag:
        # 页号

        curPageStr = ''
        if curPage > 1:
            curPageStr = f'_{curPage}'
        print(f'正在解析第{curPage}页: {GLOBAL_URI}/{module}/index{curPageStr}.jhtml')
        reqIndex = requests.get(f'{GLOBAL_URI}/{module}/index{curPageStr}.jhtml', HEADERS)
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
                # 如果遍历到停止点则跳出
                # checkStopFlag = f'{projectNo}-{textMatchResult[1]}-{textMatchResult[2]}'
                checkStopFlag = _a['href']
                if checkStopFlag == stopFlag:
                    break

                detailIndex.append({'url': _a['href'],
                                    'project_no': projectNo,
                                    'release_date': textMatchResult[2],
                                    'release_timestamp': time.mktime(time.strptime(textMatchResult[2], '%Y-%m-%d')),
                                    'title': textMatchResult[1],
                                    })
                # 暂时跳过”补充公告“的详情解析
                if "补充公告" in textMatchResult[1]:
                    print(f'发现补充公告：{textMatchResult[1]}，跳过')
                    continue
                detailMap[checkStopFlag] = get_announcement_detail(f'{GLOBAL_URI}/{_a["href"]}')

        curPage += 1
    print('此次获取新数据：')
    for i in detailIndex:
        print(i)
        print(detailMap[i['url']])
        print('----------------')

    return detailIndex, detailMap

