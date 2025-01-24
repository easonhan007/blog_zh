---
title: "第二春？令人惊喜的selenium项目selenium base"
date: 2024-12-27T09:18:08+08:00
draft: false
---

最近发现 github 月热门项目里有个老面孔 selenium base 在短期内获得了比较大的关注。

这个项目存在的时间应该有好多年了，我记得当初似乎也写过文章去介绍。

本以为这就是一个普通的结合 pytest 和 selenium 封装的测试框架，不料几年过去项目的发展似乎渐入佳境。

这次最让我眼前一亮的功能是 selenim base 支持**绕过 Cloudflare 的访问校验**。

## 新的爬虫利器？

用 selenium 写过爬虫的同学可能都会对 Cloudflare 的访问校验感到头痛。

简单来说，在你访问目标站点的时候，cloudflare 会自动校验此次访问是不是来自不明的 ip 或者设备，如果是用脚本去访问该站点的话，cloudflare 会直接进行拦截，不展示网页的内容。

不过 selenium base 却用几行代码打破了这一桎梏。

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.activate_cdp_mode(url)
    sb.uc_gui_click_captcha()
    sb.sleep(2)
```

用什么工具写爬虫其实无关紧要，爬虫进入深水区的时候往往需要跟反爬策略做各种对抗。

由于 selenium 本身使用了真实的浏览器进行网页访问，自带光环，可以绕过很多的反爬策略。

但是 cloudflare 的前置拦截却一直没有稳定的解决方案，selenium base 提供了绕过校验的便利，看上去非常利好爬虫的发挥。

## 其他有意思的特性

### 支持录制

文档在这里。https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/recorder_mode.md

因为 selenium base 暴露出来的 api 比较有限，所以录制出的代码可用性相对较高。

### 可以把用例转换成 markdown 的表格模式

这里的路子跟 robot framework 是反着来的。

把代码转成了更容易阅读的表格，对用例评审来说还是很有用的。

https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/case_plans.md

### 智能等待

selenium base 的 api 很多都是操作类型的，比如 click,type 之类，在进行操作时 selenium base 会进行智能等待，从而提升用例的稳定性。

### 自带测试报告

selenium base 的测试报告似乎是基于 pytest 的，比 playwright 的 test runner 要简陋很多，但支持错误自动截图，还是挺实用的。

https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/ReadMe.md

### 支持共享 session

也就是说不用每个用例都重新打开一次浏览器，重新登陆一遍了。

### 支持并行运行用例的能力

跟 playwright 站在同一起跑线上了。

### 支持口语化的用例编写方式。

这个直接上代码，有点搞。

这是中文的。

```python
# Chinese Translation
from seleniumbase.translate.chinese import 硒测试用例

class 我的测试类(硒测试用例):
    def test_例子1(self):
        self.开启("https://zh.wikipedia.org/wiki/")
        self.断言标题("维基百科，自由的百科全书")
        self.断言元素('a[title="Wikipedia:关于"]')
        self.如果可见请单击('button[aria-label="关闭"]')
        self.如果可见请单击('button[aria-label="關閉"]')
        self.断言元素('span:contains("创建账号")')
        self.断言元素('span:contains("登录")')
        self.输入文本('input[name="search"]', "舞龍")
        self.单击('button:contains("搜索")')
        self.断言文本("舞龍", "#firstHeading")
        self.断言元素('img[src*="Chinese_draak.jpg"]')
```

这是日语的。

```python
# Japanese Translation
from seleniumbase.translate.japanese import セレニウムテストケース

class 私のテストクラス(セレニウムテストケース):
    def test_例1(self):
        self.を開く("https://ja.wikipedia.org/wiki/")
        self.テキストを確認する("ウィキペディア")
        self.要素を確認する('[title*="ウィキペディアへようこそ"]')
        self.JS入力('input[name="search"]', "アニメ")
        self.クリックして("#searchform button")
        self.テキストを確認する("アニメ", "#firstHeading")
        self.JS入力('input[name="search"]', "寿司")
        self.クリックして("#searchform button")
        self.テキストを確認する("寿司", "#firstHeading")
        self.要素を確認する('img[src*="Various_sushi"]')
```

这个不评论了，见仁见智吧。

### 支持创建各种交互式的表格

https://github.com/seleniumbase/SeleniumBase/blob/master/examples/chart_maker/ReadMe.md。

汇报利器，不会用 js 写前端图表的同学可以玩玩。

### 支持写 ppt？

https://github.com/seleniumbase/SeleniumBase/blob/master/examples/presenter/ReadMe.md

我没看明白，但似乎真的是支持用代码去写 ppt...

感觉 selenium base 开发团队的汇报欲和求生欲很强，很多功能都是为了呈现自动化测试的工作成果。

我只能说，路走宽了。

### 支持在网页上展示各种帮助信息

还是直接看代码吧，又是一个演示功能。

```python
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)

class MyTourClass(BaseCase):

    def test_google_tour(self):
        self.open('https://google.com/ncr')
        self.wait_for_element('input[title="Search"]')
        self.hide_elements("iframe")

        self.create_tour(theme="dark")
        self.add_tour_step("Welcome to Google!", title="SeleniumBase Tours")
        self.add_tour_step("Type in your query here.", '[title="Search"]')
        self.play_tour()

        self.highlight_type('input[title="Search"]', "Google")
        self.wait_for_element('[role="listbox"]')  # Wait for autocomplete

        self.create_tour(theme="light")
        self.add_tour_step("Then click to search.", '[value="Google Search"]')
        self.add_tour_step("Or press [ENTER] after entry.", '[title="Search"]')
        self.play_tour()
```

这对录教程来说非常友好。

https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/ReadMe.md

### 有个 GUI 的用例执行器

ui 走的是实用风格，够用吧。

## 总结

selenium base 是一个实用且有脑洞的项目，有兴趣的同学可以拿来玩玩。
