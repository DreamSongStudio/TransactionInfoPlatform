import requests
import re
from bs4 import BeautifulSoup

from utils.FormatDate import parse_date


def get_announcement_detail(url):
    """
    解析正文内容，并将数据存入库中
    :param url:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    reqDetail = requests.get(url, headers)
    print(f'*** 正在解析：{url}')
    pageDetail = BeautifulSoup(reqDetail.text, 'lxml')
    pageDetail.find_all()

    # 正文部分匹配正则
    contentReString = '项目名称：(.*?)\\n' \
                     '项目编号：(.*?)\\n' \
                     '本项目采用资格审查方式：(.*?)\\n' \
                     '项目所在区域：(.*?)\\n' \
                     '投标登记时间：(.*?)\\n' \
                     '投标登记方式：(.*?)\\n' \
                     '是否允许联合体投标登记：(.*?)\\n' \
                     '保证金金额\(万元\)：(.*?)\\n' \
                     '最高投标限价\(万元\)：(.*?)\\n' \
                     '(.|\\n)*?' \
                     '开标时间：(.*?)\\n' \
                     '开标地点：(.*?)\\n' \
                     '投标文件递交时间：(.*?)\\n' \
                     '(.|\\n)*?' \
                     '公告发布时间：(.*?)\\n'

    # 正文
    contentsCompoment = pageDetail.select('div[class="gg-box"]')
    textPart = contentsCompoment[0].find_all('div',{'class':re.compile('gg-contant*')})
    # 由三部分组成
    # 1：正文部分
    # 2：公司、监督信息
    # 3：备注
    content = textPart[0]
    company = textPart[1]
    remark = textPart[2]

    # 正文解析
    parseContent = re.search(contentReString, content.text)
    if parseContent:
        _reGroups = parseContent.groups()
        registration_time = parse_date(_reGroups[4], '~')
        bid_start_time = parse_date(_reGroups[10], ' - ')
        bid_file_submit_time = parse_date(_reGroups[12], ' - ')
        details = {
            "audit_type": _reGroups[2],
            "project_region": _reGroups[3],
            "bid_registration_time_start": registration_time[0],
            "bid_registration_time_end": registration_time[1],
            "bid_registration_type": _reGroups[5],
            "allow_combination_registration": _reGroups[6],
            "earnest_money": _reGroups[7],
            "bid_amount_max": _reGroups[8],
            "bid_start_time_start": bid_start_time[0],
            "bid_start_time_end": bid_start_time[1],
            "bid_start_address": _reGroups[11],
            "bid_file_submit_time_start": bid_file_submit_time[0],
            "bid_file_submit_time_end": bid_file_submit_time[1],
        }

        # 公司信息解析
        parseCompany = [i for i in company.text.split('\n') if i]
        details['bid_company'] = parseCompany[0].split('：')[1]
        details['bid_representative'] = parseCompany[2].split('：')[1]
        details['bid_company_contact'] = parseCompany[4].split('：')[1]
        details['bid_proxy_company'] = parseCompany[1].split('：')[1]
        details['bid_proxy_representative'] = parseCompany[3].split('：')[1]
        details['bid_proxy_representative_contact'] = parseCompany[5].split('：')[1]
        details['bid_monitor_org'] = parseCompany[6].split('：')[1]
        details['bid_monitor_org_contact'] = parseCompany[7].split('：')[1]

        # todo 入库保存
        return details
