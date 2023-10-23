# 介绍

        可以快速获取并快捷展示招投标交易信息的软件，期望降低相关人员不停翻找材料的负担，以提升效率

        初步定为使用python3+PyQT5进行开发，基于爬虫的数据获取，用SQLite作为数据库进行本地存储。

# 环境

Python 3.9

- `./requirement.txt`

SQLite3

# 功能

## 主要信息展示页

表头：项目编号，项目名称，最高限价，发布时间，监管机构，

搜索框：监管部门，年份时间，限价

内容搜索：如业绩超过xxx亿，如有5A要求

## 数据获取

软件启动后，有两个方式可以获取数据，并落入本地数据库中存储

1. 通过界面上的“更新数据”按钮手动拉取

2. 每隔一定时间自动拉取进行增量更新

每次拉取新数据时，以当前库中该类最新的{项目编号-标题-时间}为停止点

**注：当前仅开发房屋建筑类信息**

# 表

## announcement_info

项目编号 project_no

项目名称 title

发布时间 release_date

链接地址 url

是否存在补充公告 have_supplementary

模块 module

## announcement_detail

审查方式 audit_type - string

项目所在区域 project_region - string

投标登记时间

- bid_registration_time_start - datetime
- bid_registration_time_end - datetime

投标登记方式 bid_registration_type - string

是否允许联合体投标登记 allow_combination_registration - tinyint

保证金金额 earnest_money - decimal

最高投标限价 bid_amount_max - decimal

开标时间

- bid_start_time_start
- bid_start_time_end

开标地点 bid_start_address

投标文件递交时间

- bid_file_submit_time_start
- bid_file_submit_time_end

招标人 bid_company - string

招标联系人 bid_representative

联系方式 bid_company_contact

招标代理 bid_proxy_company - string

招标代理人 bid_proxy_representative

代理联系方式 bid_proxy_representative_contact

招标监督机构 bid_monitor_org - string
