## RSSBlog-Source

本仓库作为[RSSBlog](https://github.com/moretti815/rssblog)的资源仓库, 负责rss数据的拉取与整理. 本站实例[rss.2005815.xyz](https://rss.2005815.xyz/).

## USAGE
```
python3 action.py
```

## BRANCH

- master: 代码逻辑
- public: 源数据

数据base url:
```
SOURCE_BASE = "https://raw.githubusercontent.com/Moretti815/rssblog-source/public/"
```
国内可以使用gitee备份加速:
```
SOURCE_BASE = "https://gitee.com/Moretti815/rssblog-source/raw/public/"
```

## FEATURE LIST

- 定时拉取订阅;
- 定时合并订阅;
- 按照时间年月分类;
- 按照用户分类;
- 保留数据来源;
- 提供RSS订阅;
- 自动验证数据质量; ([详细说明](VALIDATION.md))

## TODOLIST

- [ ] 保存博文原始数据
