---
title: "Selenium Manager使用指南"
date: 2023-04-25T11:54:30+08:00
draft: false
---

Selenium社区最近发布了Selenium Manager工具，主要是解决每隔一段时间就要重新去下载driver的痛点。当然了，这也是我痛点。因为chrome浏览器会自动更新的关系，之前我都是关掉自动更新从而回避去下载新driver的问题，不过因为用户的版本大多都是较新的，所以测试浏览器每隔一段时间还是要更新一下才比较好。我自己试用了一下，感觉还是很不错的，非常有意思的一个点是sm竟然是rust开发的，在我的印象里这种对性能和稳定性要求不是特别高的命令行用go开发和维护的话效率可能会更高一点。下面是官方blog的翻译以及我自己的一点点体验。

大多数人使用 Selenium 的第一次经验都会出现这样的错误消息：

```
java.lang.IllegalStateException: The path to the driver executable must be set by the webdriver.chrome.driver system property; for more information, see https://chromedriver.chromium.org/. The latest version can be downloaded from https://chromedriver.chromium.org/downloads
```

然后他们不得不在网上搜索有关如何处理他们下载的驱动程序的说明。

### Selenium：现在已经内置了驱动程序！

Selenium 项目希望改善用户体验，其中一项首要任务是帮助所有用户简化他们设置环境的方式。多年来，配置浏览器驱动程序一直是用户需要执行的任务，以便运行 Selenium。

设置一次浏览器驱动程序并不那么复杂，但随着浏览器发布周期缩短，现在每4-6周就有一个新的 Chrome/Firefox/Edge 版本，使得保持浏览器驱动程序与浏览器版本同步的任务变得不那么容易了。

Selenium Manager 是一个新的工具，可帮助轻松获得运行 Selenium 所需的工作环境。如果 Chrome、Firefox 或 Edge 不在 PATH 中，Selenium Manager Beta 1 将配置它们的浏览器驱动程序。

要使用 Selenium 4.6 进行 Selenium 测试，只需安装 Chrome、Firefox 或 Edge 即可。如果您已经安装了浏览器驱动程序，则会忽略此功能。如果您想帮助我们测试它，请删除您的驱动程序或删除第三方驱动程序管理器，然后事情应该仍然“正常工作”。如果不行，请提交错误报告。

Selenium Manager 的未来版本甚至会下载浏览器（如果有必要）。

### 受开源和 Selenium 社区启发

Selenium Manager 不是完全新的解决方案。多年来， Selenium 生态系统中出现了几个第三方项目，例如：Java 的 WebDriverManager、Python 的 webdriver-manager、Ruby 的 webdrivers 和 C# 的 WebDriverManager.Net。

所有这些项目都作为灵感，并清楚地表明社区需要在 Selenium 中内置此功能。此外，2021年1月进行的一项调查显示，大多数 Selenium 用户希望摆脱驱动程序管理问题。此外，驱动程序安装页面是 Selenium 文档中访问最多的页面。

### 详细介绍 Selenium Manager

Selenium Manager是一个命令行工具，用Rust语言开发，可在多个平台上运行。在其beta 1版本中，如果未检测到浏览器驱动程序或未使用第三方驱动程序管理器，则Selenium Manager将被Selenium绑定透明地调用。你也可以不使用Selenium绑定使用Selenium Manager。目前，二进制文件可以直接在Selenium的代码库中找到。运行以下命令以检查不同的参数和选项：

```
$ ./selenium-manager --help
```

下面是一个快速的示例，演示如何配置ChromeDriver：

```
$ ./selenium-manager --browser chrome
INFO /home/boni/.cache/selenium/chromedriver/linux64/106.0.5249.61/chromedriver
```

如果你维护一个基于WebDriver的项目，并希望同时使用Selenium Manager，请加入我们的社区频道，我们将乐意提供帮助。如果你有兴趣进行贡献，请查看项目的README以获取详细的说明和信息。

### 未来计划

未来将继续开发Selenium Manager，每个版本将添加新功能并修复错误。然而，你作为Selenium社区的一员，是这个新工具未来成功的关键部分。请通过我们的问题跟踪器报告想法或错误，并通过我们的社区频道加入讨论。期待你的反馈！

Happy testing!

### 简单体验

下载地址: https://github.com/SeleniumHQ/selenium/tree/trunk/common/manager

selenium manager是命令行工具，所以必须在命令行中使用，下面是帮助选项。

```
selenium-manager -h
selenium-manager 1.0.0-M3
Selenium Manager is a CLI tool that automatically manages the browser/driver infrastructure required by Selenium.


Usage: selenium-manager [OPTIONS]
Options:
  -b, --browser <BROWSER>
          Browser name (chrome, firefox, edge, iexplorer, safari, or safaritp)
  -d, --driver <DRIVER>
          Driver name (chromedriver, geckodriver, msedgedriver, IEDriverServer, or safaridriver)
  -v, --driver-version <DRIVER_VERSION>
          Driver version (e.g., 106.0.5249.61, 0.31.0, etc.)
  -B, --browser-version <BROWSER_VERSION>
          Major browser version (e.g., 105, 106, etc. Also: beta, dev, canary -or nightly- is accepted)
  -P, --browser-path <BROWSER_PATH>
          Browser path (absolute) for browser version detection (e.g., /usr/bin/google-chrome, "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome", "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
  -O, --output <OUTPUT>
          Output type: LOGGER (using INFO, WARN, etc.), JSON (custom JSON notation), or SHELL (Unix-like) [default: LOGGER]
  -p, --proxy <PROXY>
          HTTP proxy for network connection (e.g., https://myproxy.net:8080)
  -t, --timeout <TIMEOUT>
          Timeout for network requests (in seconds) [default: 120]
  -D, --debug
          Display DEBUG messages
  -T, --trace
          Display TRACE messages
  -c, --clear-cache
          Clear driver cache
      --driver-ttl <DRIVER_TTL>
          Set default driver ttl [default: 86400]
      --browser-ttl <BROWSER_TTL>
          Set default browser ttl [default: 0]
      --clear-metadata
          Clear metadata file
  -h, --help
          Print help
  -V, --version
          Print version

```

一般用法，指定浏览器路径以及driver类型，自动下载并配置driver。我也试过用浏览器的版本号来制定，不过似乎运行不起来。

另外这个工具跟ruby的webdrivers扩展有冲突，大家可以二选一就好了。

```
# windows可以用这个路径: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" 
./selenium-manager -d chromedriver -P /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome 
```