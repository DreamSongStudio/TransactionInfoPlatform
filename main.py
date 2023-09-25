import requests
import re
from bs4 import BeautifulSoup


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

prefix = 'http://www.gzggzy.cn'
# 房屋建筑
u1 = '/jyywjsgcfwjzzbgg/index.jhtml'

# 目录页
reqIndex = requests.get(f'{prefix}{u1}', headers)
soup = BeautifulSoup(reqIndex.text, 'lxml')
# print(soup)
# 获取目录页中的数据列表
dataList = soup.select('a[class="title"]')
tb = soup.tbody
detailIndex = []
for item in tb.children:
    # print(item.td)
    # print(type(item))
    _a = item.find('a')
    # print(_a)
    if type(_a) != int:
        # 解析 项目编号，项目名称，发布时间
        r = re.search('\\n(\[.*?\])\\n(.*?)\\n(\d{4}-\d{1,2}-\d{1,2})\\n', item.text.replace(' ', ''))
        textMatchResult = r.groups()
        print(textMatchResult)
        detailIndex.append({'url': _a['href'],
                            'projectNo': textMatchResult[0],
                            'releaseDate': textMatchResult[2],
                            'title': textMatchResult[1],
                            })
    print('-------------------------')


# 详情
du1 = 'http://www.gzggzy.cn/jyywjsgcfwjzzbgg/959057.jhtml'
reqDetail = requests.get(du1, headers)
soupDetail = BeautifulSoup(reqDetail.text, 'lxml')
