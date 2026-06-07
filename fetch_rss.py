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


def is_rss_url(url):
    """判断是否是直接的 RSS URL 而不是链接"""
    if not isinstance(url, str):
        return False
    url_lower = url.lower()
    return url.startswith('http') and any(x in url_lower for x in ['.xml', 'rss', 'feed', 'atom'])


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
            # 判断 link 是否是直接的 RSS URL
            if is_rss_url(link):
                # 直接是 RSS 地址
                rss_list = [link]
                print(f"Direct RSS: {link}")
            else:
                # 是包含 RSS 列表的链接
                rss_list = json.loads(requests.get(link, verify=False).text)
                # 如果返回的是字符串（单个 RSS），转换为列表
                if isinstance(rss_list, str):
                    rss_list = [rss_list]
                for r in rss_list:
                    r = r.strip("/")
                    print(r)
        except Exception as e:
            print(f"Error fetching {link}: {e}")
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
