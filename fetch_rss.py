# coding=UTF-8

import os
import json
import time
import requests
import feedparser
import pandas
from fetch_utils import *

requests.packages.urllib3.disable_warnings()
fetch_list_source = "https://gist.githubusercontent.com/moretti815/bad8611ab42af8ba0391a881f12721ab/raw/addition.json"
fetch_list = json.loads(requests.get(fetch_list_source, verify=False).text)

# 所有的rss源
rss = []
# 根据不同用户得到的rss源
rss_user = {}
# 按rss提供者分类的rss
rss_fetch_source_dir = "./__tmp__/source/"
# 举例member
rss_fetch_member_dir = "./__tmp__/member/"
# 按用户分类的rss
rss_fetch_user_dir = "./__tmp__/user/"
# 所有的rss
rss_fetch_all_dir = "./__tmp__/all/"
# 按时间年月分类的rss
rss_fetch_date_dir = "./__tmp__/date/"


def fetch():
    global rss
    # 支持字典格式 {user: link} 或列表格式 [link1, link2, ...]
    if isinstance(fetch_list, dict):
        items = fetch_list.items()
    elif isinstance(fetch_list, list):
        items = enumerate(fetch_list)
    else:
        print(f"Error: fetch_list has unsupported type: {type(fetch_list)}")
        return

    for key, link in items:
        rss_list = []
        try:
            rss_list = json.loads(requests.get(link, verify=False).text)
            for r in rss_list:
                r = r.strip("/")
                print(r)
        except:
            pass
        rss = rss + rss_list
        rss_user[str(key)] = rss_list

    # 所有源根据url去重
    rss = list({r: r for r in rss}.values())
    # 个人源不去重, 依赖于个人维护
    # for test
    # rss = ["https://xxxx/feed/",]
    # rss_user["test"] = rss

    fetch_source(rss_fetch_source_dir, rss)
    combine_source(rss_fetch_all_dir, rss_fetch_source_dir)
    combine_member(rss_fetch_member_dir, rss_fetch_all_dir)
    split_date(rss_fetch_date_dir, rss_fetch_all_dir)
    split_user(rss_fetch_user_dir, rss_user, rss_fetch_source_dir)
