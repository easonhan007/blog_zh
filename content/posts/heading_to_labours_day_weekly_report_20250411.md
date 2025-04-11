---
title: "测试周刊-憧憬五一的第一周"
date: 2025-04-11T09:16:18+08:00
draft: false
---

清明过后似乎会更加期待劳动节一些。

今年五一放五天假，时间是充裕的，但想到各大景点的人山人海，可能最终还是会选择躲在家里吧。

看看书，在附近活动活动，陪陪家人，安静的时光就足够了吧。

## AI 工具

最近在读一本关于二战时期太平洋战争的书，里面一些细节很有意思。

比如美军在珍珠港被空袭之后大概一年的时间里，一直在边打仗边学习。

因为美军中大部分将军和士兵都没有经历过真正的战争。

因此战争初期配合失误和自身混乱的情况时有发生。

感觉跟最近的 AI 热潮很像，大部分人都没有既往的经验，只能边用边学。

在实战中创新。

这两周跟 AI 相关的测试动态里，最让人眼前一亮的就是 playwright 发布了官方的 MCP 支持。

github 地址在这里:https://github.com/microsoft/playwright-mcp。

目前 7k+的 star，热度还是很高的。

看一下官方介绍。

基于 Playwright 实现浏览器自动化的 MCP。该服务器使大语言模型(LLM)能够通过结构化的可访问性快照与网页交互，无需依赖截图或视觉模型。

核心优势

​- 快速轻量 ​​：采用 Playwright 的无障碍访问树技术，非像素级输入
​- 适配 LLM​​：无需视觉模型，完全基于结构化数据操作

- 确定性操作 ​​：避免基于截图方法常见的歧义问题

应用场景

- 网页导航与表单填写(自动化操作)
- 结构化内容数据提取(爬虫)
- LLM 驱动的自动化测试(自动化测试)
- 智能体的通用浏览器交互接口(通用操作)

既然做 UI 自动化又难又花时间，那么不如让大语言模型帮助我们去实现吧。

目前已经看到有人使用 Playwright + Cursor + MCP Server 跑通了自动化测试的流程。

具体效果在这里：https://www.youtube.com/watch?v=cNh3_r6UjKk

## AI 测试策略

https://testingtitbits.com/ai-usage-for-testers-quadrants-model/ 这篇文章里作者讨论了 AI 的测试策略。

作者把测试工作分成了 4 个象限。

### 1. 自动化专区（高概率-低影响）

​​AI 的主战场 ​​：处理重复性、低风险的基础工作，释放测试人员精力

🔹 邮件撰写
🔹 根据流程图草拟测试用例
🔹 生成样板代码
🔹 流程文档记录
💡 ​​ 使用策略 ​​：让 AI 完成基础框架，人工优化提升效率
⚠️ ​​ 注意事项 ​​：AI 生成内容可能缺乏语境，需人工校准润色

### 2. 格式辅助区（低概率-低影响）

​​AI 的辅助领域 ​​：结构化数据处理，提升工作效率而非创造价值

🔹 报告格式标准化
🔹 文档结构调整
🔹 文件格式转换
🔹 数据归类整理
💡 ​​ 使用策略 ​​：利用 AI 批量处理格式化工作
⚠️ ​​ 注意事项 ​​：注意数据转换可能存在的格式错位

### 3. 精准操作区（高概率-高影响）

​​ 人机协作区 ​​：直接影响软件质量的关键环节

🔹 根据逻辑生成测试脚本
🔹 构建复杂正则表达式
🔹 生成结构化测试数据
🔹 代码重构优化
💡 ​​ 使用策略 ​​：AI 提供方案建议，人工严格验证
⚠️ ​​ 注意事项 ​​：警惕 AI 生成的测试逻辑漏洞，数据缺乏实际业务特征

### 4. 创新思维区（低概率-高影响）

​​ 人类专属领域 ​​：需要战略思维和创造力的核心工作

🔹 制定测试策略
🔹 解决独特测试难题
🔹 设计测试架构
🔹 开展回顾分析
💡 ​​ 使用策略 ​​：将 AI 作为数据分析助手，决策权保留给人类
⚠️ ​​ 注意事项 ​​：AI 无法预测边界情况，缺乏业务直觉

总结起来就是脏活累活给 AI 干，其他创新性和精细化的事情交给人类专家。

所以以后就是探索性测试(老司机测试)的天下了？

## 测试框架

### 页面对象模型的渐进式构建与优化：分步迭代方法论(英文)

https://www.ontestautomation.com/building-and-improving-page-objects-one-step-at-a-time

这篇文章里作者讨论了如何逐步的进行页面对象的重构工作。

最终的效果是这样的。

```javascript
export class ExtendedReportPage extends ReportBasePage {

    readonly page: Page;
    readonly radioSelect: Locator;
    readonly reportFormFieldAdditionalInfo: ReportFormField;

    constructor(page: Page) {
        super(page);
        this.page = page;
        this.radioSelect = page.getByLabel('Extended report');
        this.reportFormFieldAdditionalInfo = new ReportFormField(this.page, 'additionalInfo');
    }

    async create(title: string, summary: string, additionalInfo: string, roles: string[]) {
        await this.reportFormFieldTitle.complete(title, roles);
        await this.reportFormFieldSummary.complete(summary, roles);
        await this.reportFormFieldAdditionalInfo.complete(additionalInfo, roles);
        await this.buttonSaveReport.click();
    }
}
```

### ​ 并行测试执行的扩展策略 ​(英文)

https://medium.com/@evgeniy.otsevich/scaling-strategies-for-parallel-test-execution-6f15cf2d5e6d

这篇文章讨论了水平扩展,垂直扩展和混合扩展的策略，另外还介绍了常用的测试框架：selenium/playwright/cypress 的并行执行策略。

## 测试工具

### OS 视觉回归测试：快照测试（Snapshot Testing）实现指南 (英文)

https://javios.eu/test/snapshot-test-on-ios/

这篇文章讨论了如何使用截图对比的方式进行 ios 应用的回归测试。

## 言论

> 关于测试与监控的关系: 将昂贵的测试替换为监控可以让组织加快开发速度，但每个组织都需要在速度与确保（或尽可能确保）发布到生产环境前系统正常运行之间找到平衡点。这种平衡很大程度上取决于所涉及的系统特性。例如，Facebook 的开发团队能够放弃某些测试，因为他们建立了良好的反馈机制，能及时获知生产环境中的故障，并能快速发布修复程序。即使出现问题（比如用户无法查看照片或错过朋友生日提醒），后果也并不严重。另一个极端是医疗设备编程公司，这类系统容错率极低且反馈周期漫长，因此必须在使用前尽最大努力确保设备运行无误。大多数系统则介于这两个极端之间。 by Rouan Wilsenach
