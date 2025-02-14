---
title: "实用页面事务模式来进行自动化测试"
date: 2025-02-14T16:10:08+08:00
draft: true
---

## 写在前面

在进行 ui 自动化测试的时候，除了 page object 设计模式之外，最近有看到一种新的组织代码方式。

这种设计模式称为 Page Transactions，我暂时翻译为页面事务模式。

## 模式

**Guará** 是设计模式 **页面事务** 的 Python 实现。它更像是一种编程模式而非工具。作为一种模式，支持 selenium 及其他的测试框架。

该模式的目的是简化测试自动化。它的灵感来自页面对象（Page Objects）、应用操作（App Actions）和剧本模式（Screenplay）。页面事务专注于用户可以在应用程序上执行的操作（事务），例如登录、注销或提交表单。

这一倡议的诞生是为了提高自动化测试代码的可读性、可维护性和灵活性，而无需新的自动化工具或构建人类可读语句所需的许多抽象。另一个关注点是避免将框架绑定到特定的自动化工具（如 Selenium），让测试人员可以自由选择他们喜欢的工具。使用 Guará 与 Helium、Dogtail、PRA Python、Playwright 或任何你喜欢的工具时，不需要新的插件或新知识。

**值得再次强调：**

> Guará 是设计模式页面事务的 Python 实现。它更像是一种编程模式而非工具。

Guará 利用 **命令模式（GoF）** 将用户交互（如按下按钮或填写文本）分组为事务。尽管我称它为框架，但它并不是一个新工具。

它不专注于按钮、复选框或文本区域等 UI 元素，而是强调 **用户旅程**。复杂性被抽象到这些事务中，使测试语句感觉像普通英语。测试人员还可以灵活地扩展断言，使用框架未提供的自定义断言。

## 框架实战

这个简单的实现模拟了用户在网页上切换语言的操作：

```python
from selenium import webdriver
from guara.transaction import Application
from guara import it, setup
import home

def test_language_switch():
    app = Application(webdriver.Chrome())

    # 打开应用程序
    app.at(setup.OpenApp, url="https://example.com/")

    # 更改语言并断言
    app.at(home.ChangeToPortuguese).asserts(it.IsEqualTo, "Conteúdo em Português")
    app.at(home.ChangeToEnglish).asserts(it.IsEqualTo, "Content in English")

    # 关闭应用程序
    app.at(setup.CloseApp)
```

每个用户事务都被分组到自己的类中（例如 **ChangeToPortuguese**），该类继承自 **AbstractTransaction**。测试人员只需重写 **do** 方法，框架就会完成其余工作。

```python
from guara.transaction import AbstractTransaction

class ChangeToPortuguese(AbstractTransaction):
    def do(self, **kwargs):
        self._driver.find_element(By.CSS_SELECTOR, ".btn-pt").click()
        return self._driver.find_element(By.CSS_SELECTOR, ".content").text
```

测试人员可以在运行测试后查看日志中的事务和断言：

```
test_demo.py::test_language_switch
2025-01-24 21:07:10 INFO Transaction: setup.OpenApp
2025-01-24 21:07:10 INFO  url: https://example.com/
2025-01-24 21:07:14 INFO Transaction: home.ChangeToPortuguese
2025-01-24 21:07:14 INFO Assertion: IsEqualTo
2025-01-24 21:07:14 INFO  Actual Data: Conteúdo em Português
2025-01-24 21:07:14 INFO  Expected: Conteúdo em Português
2025-01-24 21:07:14 INFO Transaction: home.ChangeToEnglish
2025-01-24 21:07:14 INFO Assertion: IsEqualTo
2025-01-24 21:07:14 INFO  Actual Data: Content in English
2025-01-24 21:07:14 INFO  Expected: Content in English
2025-01-24 21:07:14 INFO Transaction: setup.CloseApp
```

测试人员还可以使用诸如 setup 和 tear down 的夹具来启动和结束测试。请记住，它不是一个新工具，因此你可以毫无问题地使用 pytest 或 unittesting 功能。

## 为什么使用 Guará？

每个类代表一个完整的用户事务，提高了代码的可重用性。此外，代码是用普通英语编写的，使非技术协作者更容易审查和贡献。

测试人员可以创建和共享自定义断言。此外，Guará 可以与任何非 Selenium 工具集成。

页面事务可以自动化 REST API、单元测试、桌面和移动测试。作为命令模式的副作用，该框架甚至可以用于产品开发。

## 使用 Guará

设置 Guará 非常简单：

1. 使用以下命令安装 Guará：

```bash
pip install guara
```

2. 使用 **AbstractTransaction** 类构建你的事务。

3. 使用 **Application** 运行器及其方法 **at** 和 **asserts** 调用事务。

4. 使用 Pytest 执行测试并生成详细日志：

```bash
python -m pytest -o log_cli=1 --log-cli-level=INFO
```

更多示例，请查看 [教程](https://github.com/douglasdcm/guara/blob/main/docs/TUTORIAL.md)。

## 结论

**Guará** 是一种新的方式，测试人员可以组织他们的代码，使其易于阅读、维护并与任何自动化驱动程序集成。它提高了测试人员与非技术成员之间的协作。测试人员还可以通过构建和共享新的断言来扩展它。

[立即尝试 Guará！](https://github.com/douglasdcm/guara/tree/main)
