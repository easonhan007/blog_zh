---
title: "测试周刊003: 大模型时代测试将会变得更加重要"
date: 2025-05-09T09:36:02+08:00
draft: false
---

五一假期结束了。

这次五一完美的错峰出行。

核心的原因是起的早。

天刚亮就出发，第一波到达景区，人流汹涌的时候就回酒店休息。

世间的喧闹与我无关。

这大概是一种错位竞争吧。

比如，当测试都在千军万马涌入新领域的时候，业务在原有的业务上进行深耕反而会取得一些错位竞争的优势。

## 观点

### 测试将会变得越来越重要

https://filiphric.com/testing-will-become-more-important-not-less

作者认为在 LLM 时代，测试将会变得举足轻重，并给出了几个预测。

1. 测试将更紧密嵌入软件创建过程

- AI 不仅生成应用代码，还将同时生成测试代码
- code review 时也将包括 review 通过的测试
- 运行先前迭代生成的测试可避免回归问题

2. 更多 AI 解决方案将整合自动化测试

- 将出现更多能同时生成代码和测试的 AI 工具
- 已有工具（如 Replay.io 的 Nut.new）能在后台运行测试并将结果反馈给 LLM

3. 人工测试将演变而非消失

- 人工测试将更加精细，专注于新功能测试和 code review
- 回归测试将主要由自动化测试承担
- 测试人员将专注于变更测试，而不是专门写自动化测试用例

4. 良好的测试设计将继续受到高度重视

- 优秀测试工程师的价值不仅在于编写测试代码
- 良好的测试实践、测试数据架构和风险区域识别能力更为关键
- 技术精湛的测试人员将引导和 review AI 生成的测试代码

5. 应用和测试运行时将成为巨大挑战

- 虽然 Playwright 等工具中的追踪查看功能成为标准，但应用运行时信息仍然缺乏
- AI 模型在调试软件方面仍有困难，因为它们缺乏代码实际运行方式的信息
- 可观察性工具可能是让 AI 生成可靠代码的关键

### 优秀的测试工程师应该具备哪些思维方式

https://qualityeng.substack.com/p/the-three-mindsets-of-a-qe

这篇文章探讨了测试工程师(Quality Engineer)应当具备的三种关键思维方式，这些思维方式可以帮助他们从"质量检查员"转变为"质量文化塑造者"：

#### 好奇心：始终保持学习的态度

- 内在驱动的信息寻求行为
- 帮助我们保持开放心态，发现模式、惊喜和可能性
- 使我们能更好地注意到质量如何在系统中产生或劣化

#### 谦逊：认识到我们并不拥有所有答案

- 了解自己知道什么，更重要的是不知道什么
- 承认知识存在差距，并主动寻求信息填补盲点
- 欢迎反馈、提问并承认不确定性，同时保持自信

#### 同理心：我们需要相互支持

- 能够分享他人的感受，不加评判地理解他人视角
- 在团队中创造安全感，让人们可以提出关切、想法、错误和问题
- 与同情不同，同理心是设身处地感受他人的成功和失败

### UI 自动化用例到底要多少才算足够

https://cakehurstryan.com/2025/04/25/you-dont-need-so-many-e2e-tests-or-do-we

根据测试金字塔的观点，ui 自动化用例的数量应该不需要特别多。

这是因为 ui 自动化测试

- 执行比较慢
- 调试困难
- 维护成本高

不过上文提出了一个观点，那就是 ui 自动化用例的多少其实取决于项目的实际情况。

比如下面的情形里，ui 自动化用例是可以酌情增加的。

- 代码不支持小型测试：某些代码结构不易进行单元测试
- 组织结构限制：开发和测试团队分离
- 技能限制：团队缺乏编码能力
- 惯性和习惯：团队已习惯于 E2E 测试方法
- 管理或审计要求：外部条件要求特定测试方式

## 性能测试

### 做好性能测试最关键的点就在于如何获取有效的需求

https://medium.com/@sul0089/your-performance-tests-are-only-as-good-as-your-requirements-ebf3b0d88426

这篇文章的观点跟我之前的想法是基本一致的。

无论测试工具和框架多么先进，如果性能测试需求模糊、过时或与实际使用场景脱节，测试结果就无法反映现实情况，可能导致生产环境中出现性能问题。

下面这些技巧可以帮忙大家梳理清楚性能需求

#### 利用过去 3 年的生产数据 + 增长预测

分析历史使用模式：并发用户数、每秒/分钟事务数、数据吞吐量、API 调用量、峰值使用时的内存/CPU 消耗

将这些指标与业务增长预期对齐（例如：如果黑色星期五流量每年增长 15%，2025 年的测试必须模拟比 2022 年增加 50-55%）

#### 理解峰值负载的特性

区分短暂峰值（如抢购、重大公告）和持续负载（如报税季、课程注册期）

确认一天或一周内是否有多个峰值窗口

不同类型的峰值需要不同类型的性能测试

#### 使用适当的测试类型模拟生产使用情况

- 负载测试：验证系统能否处理预期的日常/每周使用水平
- 压力测试：识别上限及系统在压力下的行为
- 稳定性测试：检查长期性能下降或资源泄漏
- 突发测试：模拟流量的突然、意外激增
- 在许多情况下需要混合测试方法

## 自动化测试

### 使用截图比较的方法来进行移动端的自动化测试

https://www.thegreenreport.blog/articles/mobile-qa-automation-leveraging-visual-screenshot-comparison-for-ui-consistency/mobile-qa-automation-leveraging-visual-screenshot-comparison-for-ui-consistency.html

这个思路其实是非常直接的，就是截取一张基线图片，然后在测试中截图与基线图片进行对比。

两张图差异比较大的话就可以猜测是不是功能出现了异常。

核心代码也不难。

```python

def compare_images(baseline_path, current_path, diff_path):
    if not os.path.exists(baseline_path):
        print(f"No baseline found at {baseline_path}. Creating new baseline.")
        return False

    baseline_img = Image.open(baseline_path).convert('RGB')
    current_img = Image.open(current_path).convert('RGB')

    if baseline_img.size != current_img.size:
        print("Images have different dimensions. Resizing for comparison.")
        current_img = current_img.resize(baseline_img.size)

    diff = ImageChops.difference(baseline_img, current_img)

    if diff.getbbox() is None:
        return True

    diff = diff.convert('RGB')
    for x in range(diff.width):
        for y in range(diff.height):
            r, g, b = diff.getpixel((x, y))
            if r != 0 or g != 0 or b != 0:
                diff.putpixel((x, y), (255, 0, 0))

    diff.save(diff_path)
    return False
```

这个判断方式有点粗糙，只能说可以用，但不一定好用。

后面结合大模型的多模态能力进行更加智能的比对可能效果会更好一点。

## 探索性测试的历史演变

**1970 年代-1980 年代**
探索性测试的根源可以追溯到早期软件开发中常见的临时测试实践。虽然当时还没有正式认可，但许多测试人员自然而然地会在编写的测试用例之外探索软件。

**1990 年代**
"探索性测试"一词由 Cem Kaner 在 1983 年首次提出，但在 1990 年代才真正获得广泛关注。
Bach 和 Bolton 进一步发展了这一概念，引入了基于会话的测试管理（SBTM），为探索性测试提供了结构化框架。

**2000 年代至今**
敏捷方法论的兴起促使探索性测试的应用日益增多。

对快速反馈和适应性的需求与敏捷原则完美契合，使探索性测试成为现代测试策略中不可或缺的组成部分。
