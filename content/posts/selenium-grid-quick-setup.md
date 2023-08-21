---
title: "Selenium Grid Quick Setup"
date: 2023-08-21T17:13:22+08:00
draft: false
---

今天在看selenium grid文档的时候，发现selenium grid4的设计还是不错的，想顺手体验一下，于是就发现了[docker-selenium](https://github.com/SeleniumHQ/docker-selenium)项目，可以快速的设置好selenium grid环境，非常简单方便。

然而后面准备用python去写个简单例子的时候，发现很难找到python代码的例子，好不容易找到1个却发现跑不起来，于是简单的看了下源码，找到了正确的打开方式，这里简单分享一下。


### selenium grid的使用场景

在我看来grid的使用场景有两个

- 在不同的浏览器上并行跑用例，这比挨个在不同浏览器上跑要省不少时间
- 启动多个节点在同一个浏览器上并行跑用例，同样也是节约了执行时间


### 快速安装好selenium grid环境

Selenium grid有多种模式，比如Standalone, Hub and Node，对于初次体验来说无脑用Standalone是不会有问题的。

传统的方式是使用java来运行jar包安装，不过docker selenium提供了更简单的方式，直接用docker跑镜像就好了。 比如下面的命令就启动了1个firefox的远程节点。

```
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-firefox:4.11.0-20230801
```

这里暴露了2个端口

- 4444: hub的端口，直接访问可以看到所有节点的信息
- 7900: vnc的端口，访问http://localhost:7900/?autoconnect=1&resize=scale&password=secret就可以看到远程节点上的浏览器运行情况，非常方便了

### 连接远程节点进行测试

代码很简单，我的运行环境是
- python: 3.10.2
- selenium: 4.11.2
- selenium gird: selenium/standalone-firefox:4.11.0-20230801

```python
from selenium  import webdriver 
from selenium.webdriver.firefox.options import Options
import time

ff_option = Options()

dr = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
	options=ff_option
)

dr.get('https://google.com')

time.sleep(5)

dr.quit()


```
这里需要注意的是启动链接remote节点的时候需要传入`ff_option`，之前的版本的代码里需要传入类似于` desired_capabilities={'browserName': 'firefox', 'javascriptEnabled': True})`的参数，在某个版本的selenium里这个参数被废弃掉了，需要用浏览器的option来替代。

在脚本运行的时候用浏览器访问http://localhost:7900/?autoconnect=1&resize=scale&password=secret可以看到脚本的执行过程，挺有意思的。

### 总结

selenium grid的热度应该不高，所以实践分享和代码都不是很多。不过如果有同学需要做sass服务，提供远程执行selenium测试用例的测试平台的话，selenium grid是一个非常不错的开箱即用的选择。特别是selenium grid的Distribute的实现十分的工程化，可以配置的东西很多，而且对外提供了一系列的接口，二次开发的潜力还是巨大的。




