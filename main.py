import requests
import time
import re
from bs4 import BeautifulSoup

from get_announcement_detail import get_announcement_detail
from get_announcement_index import get_announcement_index
from utils.Common import HOUSE_BUILDING, MUNICIPAL_ENGINEERING
from utils.FormatDate import parse_date

# 房屋建筑
get_announcement_index(MUNICIPAL_ENGINEERING)

# 详情
du1 = 'http://www.gzggzy.cn/jyywjsgcfwjzzbgg/959057.jhtml'
# get_announcement_detail(du1)


