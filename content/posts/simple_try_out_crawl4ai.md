---
title: "快速体验近期最火的AI爬虫项目-Crawl4AI"
date: 2024-10-17T23:02:15+08:00
draft: false
---

[Crawl4AI](https://github.com/unclecode/crawl4ai)应该是近期最火的 AI 爬虫项目了。

这个项目吸引我的点有 2 个：

- 引入了 AI
- 底层使用的是[playwright](https://playwright.dev/)

## 核心特性

官方的介绍是这样的。

- 🆓 完全免费和开源
- 🚀 性能极快，超越许多付费服务
- 🤖 适合大语言模型的输出格式（JSON、清理过的 HTML、markdown）
- 🌍 支持同时爬取多个 URL
- 🎨 提取并返回所有媒体标签（图片、音频和视频）
- 🔗 提取所有外部和内部链接
- 📚 从页面提取元数据
- 🔄 用于身份验证、头部和爬取前页面修改的自定义钩子
- 🕵️ 用户代理自定义
- 🖼️ 对页面进行截图
- 📜 爬取前执行多个自定义 JavaScript
- 📊 使用 JsonCssExtractionStrategy 生成结构化输出，无需大语言模型
- 📚 多种切片策略：基于主题、正则表达式、句子等
- 🧠 高级提取策略：余弦聚类、大语言模型等
- 🎯 支持 CSS 选择器以精确提取数据
- 📝 传递指令/关键词以优化提取
- 🔒 支持代理以增强隐私和访问
- 🔄 会话管理，适用于复杂的多页面爬取场景
- 🌐 异步架构，提高性能和可扩展性

用的一手好 emoji👍。

这里面一些传统爬虫所不支持的功能基本上来自于 playwright，比如截图之类的。

比较有意思是引入了切片策略和使用大预言模型来处理爬取的内容。

## 安装

Crawl4AI 的安装相对比较复杂，不过如果不需要深入体验本地大模型的话，使用最基本的安装方式就可以了。

基本上是 2 条命令。

```
pip install crawl4ai
python -m playwright install chromium
```

这里为了节约时间和空间，只安装了 playwright 的 chrome 浏览器，一般情况下够用了。

## 爬豆瓣上评分最高的 250 本书

写了个获取豆瓣评分最高的 250 本图书的爬虫。

这个爬虫跟大语言模型没有半毛钱关系。

大概的过程就是访问https://book.douban.com/top250这个页面以及后面的9个分页，把每一页的25本图书都爬下来。

拿官方的例子随手改了改，代码如下。

```python
import asyncio
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from pprint import pprint as pp

async def extract_books():
    schema = {
        "name": "Douban Book 250",
        "baseSelector": "tr.item",
        "type": "list",
        "fields": [
            {
                "name": "title",
                "type": "text",
                "selector": ".pl2 > a",
            },
            {
                "name": "url",
                "type": "attribute",
                "selector": ".pl2 > a",
                "attribute": "href",
            },
            {
                "name": "info",
                "type": "text",
                "selector": ".pl",
            },
            {
                "name": "rate",
                "type": "text",
                "selector": ".rating_nums",
            },
            {
                "name": "quote",
                "type": "text",
                "selector": "span.inq",
            },
        ],
    }

    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    async with AsyncWebCrawler(verbose=True) as crawler:
        for i in range(10):
            result = await crawler.arun(
                url = f"https://book.douban.com/top250?start={i * 25}",
                extraction_strategy=extraction_strategy,
                bypass_cache=True,
            )
            assert result.success, "Failed to crawl the page"

            books = json.loads(result.extracted_content)
            pp(books)
            print(f"Successfully extracted {len(books)} books")

if __name__ == "__main__":
    asyncio.run(extract_books())
```

部分结果如下

```
[{'info': '[清] 曹雪芹 著 / 人民文学出版社 / 1996-12 / 59.70元',
  'quote': '都云作者痴，谁解其中味？',
  'rate': '9.6',
  'title': '红楼梦',
  'url': 'https://book.douban.com/subject/1007305/'},
 {'info': '余华 / 作家出版社 / 2012-8 / 20.00元',
  'quote': '生的苦难与伟大',
  'rate': '9.4',
  'title': '活着',
  'url': 'https://book.douban.com/subject/4913064/'},
 {'info': '[英] 乔治·奥威尔 / 刘绍铭 / 北京十月文艺出版社 / 2010-4-1 / 28.00',
  'quote': '栗树荫下，我出卖你，你出卖我',
  'rate': '9.4',
  'title': '1984',
  'url': 'https://book.douban.com/subject/4820710/'},
 {'info': 'J.K.罗琳 (J.K.Rowling) / 苏农 / 人民文学出版社 / 2008-12-1 / 498.00元',
  'quote': '从9¾站台开始的旅程',
  'rate': '9.7',
  'title': '哈利·波特',
  'url': 'https://book.douban.com/subject/24531956/'},
 {'info': '刘慈欣 / 重庆出版社 / 2012-1 / 168.00元',
  'quote': '地球往事三部曲',
  'rate': '9.5',
  'title': '三体全集: 地球往事三部曲',
  'url': 'https://book.douban.com/subject/6518605/'},
 {'info': '[哥伦比亚] 加西亚·马尔克斯 / 范晔 / 南海出版公司 / 2011-6 / 39.50元',
  'quote': '魔幻现实主义文学代表作',
  'rate': '9.3',
  'title': '百年孤独',
  'url': 'https://book.douban.com/subject/6082808/'},
 {'info': '[美国] 玛格丽特·米切尔 / 李美华 / 译林出版社 / 2000-9 / 40.00元',
  'quote': '革命时期的爱情，随风而逝',
  'rate': '9.3',
  'title': '飘',
  'url': 'https://book.douban.com/subject/1068920/'},
 {'info': '[英] 乔治·奥威尔 / 荣如德 / 上海译文出版社 / 2007-3 / 10.00元',
  'quote': '太阳底下并无新事',
  'rate': '9.3',
  'title': '动物农场',
  'url': 'https://book.douban.com/subject/2035179/'},
 {'info': '林奕含 / 北京联合出版公司 / 2018-2 / 45.00元',
  'quote': '向死而生的文学绝唱',
  'rate': '9.2',
  'title': '房思琪的初恋乐园',
  'url': 'https://book.douban.com/subject/27614904/'},
 {'info': '[明] 罗贯中 / 人民文学出版社 / 1998-05 / 39.50元',
  'quote': '是非成败转头空',
  'rate': '9.3',
  'title': '三国演义（全二册）',
  'url': 'https://book.douban.com/subject/1019568/'},
 {'info': '[英] 阿·柯南道尔 / 丁钟华 等 / 群众出版社 / 1981-8 / 53.00元/68.00元',
  'quote': '名侦探的代名词',
  'rate': '9.3',
  'title': '福尔摩斯探案全集（上中下）',
  'url': 'https://book.douban.com/subject/1040211/'},
 {'info': '[日] 东野圭吾 / 刘姿君 / 南海出版公司 / 2013-1-1 / 39.50元',
  'quote': '一宗离奇命案牵出跨度近20年步步惊心的故事',
  'rate': '9.2',
  'title': '白夜行',
  'url': 'https://book.douban.com/subject/10554308/'},
 {'info': '[法] 圣埃克苏佩里 / 马振骋 / 人民文学出版社 / 2003-8 / 22.00元',
  'quote': '献给长成了大人的孩子们',
  'rate': '9.1',
  'title': '小王子',
  'url': 'https://book.douban.com/subject/1084336/'},
 {'info': '（丹麦）安徒生 / 叶君健 / 人民文学出版社 / 1997-08 / 25.00元',
  'quote': '为了争取未来的一代',
  'rate': '9.3',
  'title': '安徒生童话故事集',
  'url': 'https://book.douban.com/subject/1046209/'},
 {'info': '鲁迅 / 人民文学出版社 / 1973-3 / 0.36元',
  'quote': '新文学的第一声呐喊',
  'rate': '9.2',
  'title': '呐喊',
  'url': 'https://book.douban.com/subject/1449351/'},
 {'info': '金庸 / 生活·读书·新知三联书店 / 1994-5 / 96.00元',
  'quote': '有情皆孽，无人不冤',
  'rate': '9.2',
  'title': '天龙八部',
  'url': 'https://book.douban.com/subject/1255625/'},
 {'info': '三毛 / 哈尔滨出版社 / 2003-8 / 15.80元',
  'quote': '游荡的自由灵魂',
  'rate': '9.2',
  'title': '撒哈拉的故事',
  'url': 'https://book.douban.com/subject/1060068/'},

...
...
]
```

## 总结

写这个爬虫大概花了半小时时间，所以这个库上手还是不太困难的。

然而最基本的使用场景里，ai 完全没有出场的机会。

后面有时间的话体验再体验一下完全使用 ai 来抓取网页内容的功能吧。

这次试用我觉得亮点如下：

- 使用 playwright，极大的提升了爬虫的可用性和使用场景
- 默认使用异步的方式使得爬虫的性能非常不错
- 现在一些站点的前端页面会做 css 混淆，传统的基于 css 选择器的爬虫鞭长莫及，引入 ai 进行内容的爬取非常有必要

不足的地方：

- 官方文档关于 ai 使用方法的那几篇，代码格式是乱的，搞得我不好 copy，所以下次再体验吧
- `JsonCssExtractionStrategy`的 schema 没有完整的规格说明，只能靠猜
- 代码库里跟 llm 相关的例子太少
