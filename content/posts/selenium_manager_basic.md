---
title: "Selenium Manager可以用起来了"
date: 2024-02-29T14:28:45+08:00
draft: false
---

前几天随手写了几个headless的selenium爬虫脚本，运行的时候发现本地的chromedriver竟然不需要更新，一时间有点没反应过来，毕竟selenium有个痛点就是**chrome 浏览器自动升级之后需要下载新的chromedrier**， 否则之前的脚本将会报错。当然了，之前也有一些规避的方式，比如

* 关掉chrome的自动升级
* 用firefox，毕竟[geckodriver一年也就更新个2-3个版本](https://github.com/mozilla/geckodriver/releases)
* 用第三方的driver管理工具，比如python有个[webdriver-manager](https://pypi.org/project/webdriver-manager/)

这些方法其实都挺好，都能解决核心问题，特别是python的webdriver-manager，几行代码就可以保持driver永远自动更新，举个例子

```python
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
```

这次不用更新driver是因为使用了官方推出的[selenium manager](https://www.selenium.dev/documentation/selenium_manager/)，之前没留意，不过真到用的时候发现还是比较方便的。对我来说selenium manager最方便的就是初始化环境的功能，比如

- 自动安装浏览器
- 自动安装driver
- 支持多架构多系统
- 可以配置代理，这点很重要
- 自动管理浏览器和driver，其实就是把浏览器和driver放在了系统PATH里

如果我有一个脚本需要在windows和macos的最新版本chrome上跑，那么环境初始化就非常容易了，只需要下面的命令

```
selenium-manager --browser chrome
selenium-manager --driver chromedriver
```

selenium manager会自动探测机器架构和系统，然后下载chrome浏览器和driver，如果遇到下载不畅的情况，直接设置一下代理就可以了。

### 下载

selenium manager让人一头雾水的地方是安装方法，其实selenium manager是不需要安装的，直接下载就好。
selenium manager是用rust写的命令行应用(rust现在势头很盛，比如cloudflare就用rust写了个nginx的平替Pingora)，目前的下载方式还是直接下载二进制文件，下载地址是:https://github.com/SeleniumHQ/selenium_manager_artifacts/releases。该项目更新非常频繁，大家下最新的版本就好。

### 保持driver自动更新
思路很简单，如果是非windows机器的话可以使用crontab。

```
0 5 * * * selenium-manager --driver chromedriver
```

### 总结
之前写过文章去介绍selenium manager的具体用法，大家有兴趣可以往回翻一下。这篇文章主要是感慨一下selenium manager给日常工作带来的便利。之前经常遇到的一段时间过后selenium代码执行报错的问题目前是有了工程化的解决方案了，推荐大家使用。



