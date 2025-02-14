---
title: "看起来有点用但实际用处有限的ai测试工具coTestPilot.ai"
date: 2025-01-24T09:23:53+08:00
draft: false
---

最近看到一款新发布的 AI 自动化测试工具 coTestPilot.ai，项目主页在[这里](https://github.com/jarbon/coTestPilot/tree/main)。

这是由 Checkie.AI 的测试专家开发的开源扩展，为自动化测试带来了额外的 AI 功能。该项目旨在通过简单集成现有的 Playwright 和 Selenium 测试，使每个自动化工程师都能享受到 AI 给测试带来的便捷。

## 什么是 coTestPilot？

coTestPilot 是 checkie.ai 和 testers.ai 上可用的 AI 测试 agent 的轻量级版本。它通过利用 GPT-4 Vision 分析网页，为 Playwright 和 Selenium 扩展了自动化测试和缺陷检测的 AI 能力，以识别潜在问题、不一致和可用性问题。

最棒的是，只需添加一个函数调用，就可以为现有的测试自动化添加 AI 驱动的检查。

## 主要特点

- 多样化测试角色：内置多个测试 agent 配置文件，包括 UI/UX 专家、无障碍专家、安全测试人员等
- 可定制检查：轻松添加自定义测试规则和专门的提示
- 全面分析：识别视觉错误、内容不一致和功能问题
- 详细报告：生成包含屏幕截图和详细问题描述的 HTML 报告
- 速率限制和重试逻辑：内置 API 速率限制保护

## 为什么使用 AI 测试 agent？

传统的自动化测试擅长检查特定的预定义场景，但常常会忽略人工测试人员会立即发现的意外问题。coTestPilot 通过为自动化测试套件添加一个 AI 驱动的"额外视角"来解决这个问题。
AI agent 可以识别如下问题：

- 元素错位和视觉缺陷
- 内容不一致和拼写错误
- 无障碍问题
- 基本安全问题
- 性能预警
- 用户体验问题

## 入门指南

以 selenium 的版本为例。

```
git clone https://github.com/jarbon/coTestPilot/tree/main/Selenium/4/py/selenium_cotestpilot

export OPENAI_API_KEY='your-api-key'

pip install selenium
pip install webdriver-manager  # For easy driver management
```

把下载下来的一整串 selenium_cotestpilot 重命名成`selenium_cotestpilot`，然后新建 1 个文件`se_test.py`

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium_cotestpilot  # import checks

# Configure logging and settings
configure_logging(
    level="DEBUG",
    console_verbosity=LogLevel.VERBOSE,
    config={
        'api_rate_limit': 0.25,        # API calls per second
        'screenshot_retention_days': 7,  # Screenshot retention period
        'max_retries': 5                # API call retry attempts
    }
)

# Initialize Selenium and navigate to a page
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://example.com')

# Basic AI check with additional options
result = driver.ai_check(
    console_verbosity=LogLevel.BASIC,  # Control logging for this check
    save_to_file=True,                 # Save results to JSON file
    output_dir="ai_check_results"      # Directory for results
)
print(f"Found {len(result.bugs)} issues")

# Generate HTML report
report_path = driver.ai_report(output_dir="ai_check_results")
print(f"Report generated at: {report_path}")
```

## 测试报告

测试报告如下所示。

![](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*oPuZeWK0U_zYcvwZyr0soQ.png)

## 支持的测试 agent

下面是所有支持的测试角色列表。

```json
{
  "testers": [
    {
      "name": "Jason",
      "biography": "Democratizing quality at scale. Likes to test all the basic aspects of an app, but do it at scale.",
      "matches": ["AI", "Quality", "Search", "Browser"],
      "interests": "AI, Testing, Automation, Quality, Scale, Basic Testing,Innovation and testing browsers and search engines."
    },
    {
      "name": "Aiden",
      "biography": "Aiden has a keen eye for UI inconsistencies and visual bugs across different devices and screen sizes. Aiden is also a certified scuba diver and enjoys exploring underwater landscapes during his travels.",
      "matches": [
        "UI Testing",
        "Visual Regression Testing",
        "Responsive Design Testing",
        "Cross-Device Testing"
      ],
      "interests": "Responsive Design Testing, Cross-Device Compatibility, Visual Regression Testing"
    },
    {
      "name": "Marcus",
      "biography": "Marcus is passionate about brand consistency and visual design in software products. He's also a talented painter, and his art often explores themes of identity and culture.",
      "matches": [
        "Brand Consistency",
        "Visual Design",
        "UI Testing",
        "Brand Testing"
      ],
      "interests": "UI Design Testing, Brand Guidelines Testing, Visual Consistency Testing"
    },
    {
      "name": "Adeela",
      "biography": "Adeela specializes in responsive mobile web testing across various devices and operating systems.",
      "matches": ["Mobile", "Cross-platform", "Devices", "Operating systems"],
      "interests": "Cross-platform compatibility, mobile UX, app store guidelines"
    },
    {
      "name": "Sophia",
      "biography": "Sophia is a content specialist who ensures that every word in an app is consistent and free from errors. With her sharp eye for detail, she loves refining documentation to make it clear and accessible for global audiences.",
      "matches": [
        "Content",
        "Inconsistency",
        "Spelling",
        "Grammar",
        "Formatting",
        "Clarity"
      ],
      "interests": "Technical writing, localization, style guides, translation"
    },
    {
      "name": "Alejandro",
      "biography": "Alejandro is an accessibility specialist who works tirelessly to ensure digital experiences are inclusive for everyone, particularly for users with disabilities. He's passionate about ensuring all users feel represented in the digital world.",
      "matches": ["Accessibility", "Inclusive", "User Advocacy"],
      "interests": "Inclusive design, assistive technologies, digital rights for the disabled"
    },
    {
      "name": "Isabella",
      "biography": "Isabella focuses on usability testing, ensuring that products are intuitive and easy to use for all types of users. She enjoys cooking and often hosts dinners for her family and friends.",
      "matches": ["Usability", "Intuitive Design", "User Research"],
      "interests": "User Research, Accessibility Testing, Cognitive Load Analysis"
    },
    {
      "name": "Pete",
      "biography": "Pete is passionate about privacy protection and compliance with data protection regulations. In his free time, he loves to go on long motorcycle road trips.",
      "matches": [
        "Security Testing",
        "Privacy Testing",
        "GDPR Compliance",
        "Data Protection"
      ],
      "interests": "GDPR Compliance, Data Anonymization, Privacy by Design"
    },
    {
      "name": "Zachary",
      "biography": "Zachary, known for his unconventional testing methods, loves pushing systems to their limits with bizarre and creative user actions. His outside-the-box thinking often uncovers bugs in the most unexpected places.",
      "matches": [
        "Boundary Testing",
        "Edge Cases",
        "Creative",
        "Unexpected",
        "Chaos Engineering",
        "Unconventional"
      ],
      "interests": "Chaos Engineering, fuzz testing, edge case exploration"
    },
    {
      "name": "Zoe",
      "biography": "Zoe is a meticulous tester who takes pride in uncovering elusive bugs that often go unnoticed. Her sharp attention to detail and methodical approach make her a sought-after bug hunter in high-stakes projects.",
      "matches": ["Elusive Bugs", "Attention to Detail", "Thorough"],
      "interests": "Bug tracking, root cause analysis, memory leaks"
    },
    {
      "name": "Emma",
      "biography": "Emma is an expert in form validation and user input handling. Her sharp eye for detail ensures that even the most subtle data entry issues are caught and resolved before they impact users.",
      "matches": [
        "Form Validation",
        "Input Handling",
        "Data Entry Testing",
        "UX Issues"
      ],
      "interests": "Input Validation, Accessibility Testing, UX Writing, Usability Testing"
    }
  ]
}
```

## 实现原理

看了一眼代码，实现其实非常直接。

所有的实现都在`__init__.py`里，所以上面的代码示例里，只需要`import selenium_cotestpilot`就可以加载所有的实现了。

代码核心的方法是`check`函数，没什么黑魔法，其实就是拿到了当前页面 body 里的 text，然后定义了一个提示词，让不同的测试人员对这个 页面上所有的文本 进行测试。

这些测试人员其实就是上文讲的测试 agent，是角色化的，每个人都有自己的拿手本领。

比如 Emma 这个角色偏重表单的校验。

提示词如下所示

```
f"""Please analyze this webpage for any errors, issues, or problems.

IMPORTANT: Only return high-confidence issues. It is perfectly acceptable to return no issues if none are found with high confidence.
For each issue found, include a confidence score between 0 and 1, where:
- 1.0 means absolutely certain this is an issue
- 0.8-0.9 means very confident
- 0.7-0.8 means reasonably confident
- Below 0.7 should not be reported

Severity levels (0-3):
0 = Cosmetic: Minor visual or text issues that don't impact functionality or understanding
1 = Low: Issues that cause minor inconvenience but don't prevent core functionality
2 = Medium: Issues that significantly impact user experience or partially break functionality
3 = High: Critical issues that prevent core functionality or severely impact user experience or the business.

Page URL: {url}
Page Text Content:
{page_text}

You are {tester['name']}, and this is your expertise and background:
{tester['biography']}

Please identify any:
1. Visual errors or layout issues
2. Content errors or inconsistencies
3. Functionality problems that are visible
4. Any other issues that might affect user experience

Output format: {output}

Example format:
[
    {{
        "title": "Broken image link",
        "severity": "high",
        "description": "Image on homepage fails to load",
        "why_fix": "Impacts user experience and site professionalism",
        "how_to_fix": "Update image source URL or replace missing image",
        "confidence": 0.95,
        "related_context_if_any": "The image is a logo and its url is 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_light_color_272x92dp.png' and is used in the header"
    }}
]

return only the JSON array, no other text or comments.
```

大家有兴趣可以学习一下提示词，还是有一些工程化的实践的。

## 总结

- 该项目我运行不起来，因为没有 gpt4 的 key
- 代码运行时需要把页面的文本拿到，所以页面越复杂，费用越高
- 项目本质就是拿到页面上所有的文本，最后调用 gpt4 传入提示词，让 gpt4 返回推理的结果，效果应该不会太稳定
- 项目本身没有增加任何的断言，只是引入了专家建议，所以对功能测试帮助不大，不过也许能发现一些低级错误

总之个人观点: **这是一款看起来有点用，但实际用处有限的 ai 测试工具**。
