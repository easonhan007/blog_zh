---
title: "测试周刊-AI不应该用来解决本来就不存在的问题"
date: 2025-04-17T16:05:24+08:00
draft: false
---

离五一只有两周了。

最近有朋友买了 cursor 的会员，我驻足观看了一番。

他先描述需求，然后让大模型生成原型，接着又让 LLM 根据原型来生成前后端项目的代码。

整体流程一气呵成，看着非常有科幻感。

不难想象，接下来根据可以工作的前后端代码就可以让大模型来生成 ui 和接口的自动化测试用例。

不久的将来，通过 AI 生成的各种测试代码可能会是开发标准输出的一部分了吧。

## AI 与测试的思考

### 停止过度设计：为什么测试 ID 比人工智能驱动的定位器智能更适合 UI 自动化(英文)

https://testersdigest.blogspot.com/2025/04/stop-overengineering-why-test-ids-beat.html

并不是所有的测试人员都关注 AI。

并不是所有关注 AI 的测试工程师都盲目的拥抱 AI。

这篇文章就反对使用人工智能来解决 UI 自动化测试中的定位问题，而是提倡使用测试 ID（Test IDs）这一更简单有效的方法。

1. **测试 ID 稳定可靠**：测试 ID（如`data-testid="submit-button"`）是可预测的，不会因为开发人员更改 CSS 类、更新布局或重命名元素而失效。

2. **避免不必要的 AI 复杂性**：为什么要让 AI 去"猜测"正确的元素，当我们可以从一开始就通过测试 ID 明确告诉 DOM 要查找什么。AI 应该增强测试策略，而不是清理本可避免的混乱。

3. **效率优于优雅**：在测试中，我们的目标是验证功能而非创造艺术。Test ID 是低耦合、高效率的工具，能直接指向我们关心的元素，且运行更快。

4. **过度工程化难以扩展**：使用 AI 来修复不稳定的测试和适应 UI 变化增加了另一层复杂性，意味着更多不可控的点。如果 AI 模型抽风了，不仅测试会失败，还需要进行 AI 调试。

5. **开发者应参与其中**：添加`data-testid`属性是一项投入小、回报大的工作，是构建可测试软件的一部分。

与其追求 AI 驱动的自我修复测试自动化梦想，不如使用 Test ID 构建一个从一开始就可靠的系统。

💡AI 很棒，但不应该用来解决本不应该存在的问题。

## AI 工具

### n8n

https://n8n.io/

一款原生支持 AI 的自动化工具，感觉跟 RPA 很像，但这款是开源的，可以自己搭私服玩。

很适合做办公自动化的工作。

### 另一款 playwright 的 mcp 实现

https://github.com/executeautomation/mcp-playwright

跟官方出品的那款功能差不多。可以支持 Claude Desktop, Cline 以及 Cursor IDE

![](https://github.com/executeautomation/mcp-playwright/raw/main/image/playwright_claude.png)

## AI 课程

### 微软出品的 ai agent 教程

https://github.com/microsoft/ai-agents-for-beginners

10 节课教你开启构建 AI Agent 所需的一切知识

## 测试工具

### Bruno-另一款 postman 的替代工具

https://github.com/usebruno/bruno

![](https://www.usebruno.com/_next/image?url=%2Fbruno_app%2Fbruno-homepage.png&w=2048&q=75)

很奇怪，每次看到可以替换 postman 的工具我都非常兴奋。

可能是被 postman 弄应激了。

Bruno 有下面一些不错的特性

- 支持 win/mac/linux
- 支持 gui cli 以及 vscode 扩展
- 脚本保存为纯文本的格式，对 git 比较友好
- 支持 js 脚本扩展

之前这款工具的口碑还是不错的，毕竟开源免费。

后来推出了收费订阅功能，pro 版本每人每月 6 美金，Ultimate 版本 11 美金每人每月。

比 postman 还是要便宜的。

免费的版本够用了，而且不用强制注册登录，还是推荐吧。

后来看了一眼 bruno 团队的情况，好吧，是一个印度团队。

另外，热知识。

postman 也是印度团队开发的。

postman 在被收购之前，还是很好用的。

所以，bruno 在被收购之前，免费版本应该是可以快乐使用的吧。

## 观点

### 不仅仅是“手动测试”：重新认识软件测试人员的技能(英文)

https://www.ministryoftesting.com/articles/more-than-just-manual-testing-recognising-the-skills-of-software-testers

在这篇文章里，作者提出了一些很有意思的观点。

1. **“手工测试”一词具有误导性且贬低测试职业**  
   使用“手工测试”容易让人误以为这类测试只是机械执行脚本、技术含量低，从而贬低了测试人员在探索、分析和判断上的深度能力。这种语言强化了“非自动化=低价值”的误解。

2. **测试不该被简化为“手动 vs 自动”的二元对立**  
   测试是一项复杂的认知活动，包含探索、批判性思维和创造力，不应以是否使用自动化工具来定义。自动化是测试工具之一，而非测试的全部。

3. **“手工测试工程师”标签带来职业限制与偏见**  
   该标签会让测试人员在职业发展中被边缘化，比如被认为不具备技术能力、难以晋升、或不符合现代招聘的“全能型”需求，阻碍了多样化技能的发展。

4. **语言塑造认知，应更新测试话语体系**  
   我们应该用更精准的词汇来描述测试类型，例如“探索性测试”“分析性验证”“人机协同测试”等，或干脆就称“testing”，以消除人为制造的技术鄙视链。

5. **推动更协同与尊重的测试文化**  
   测试应被看作人机协作的整体过程，人类的判断力与自动化工具互补，而非彼此竞争。换一种语言，也是在推动更包容、更精准的测试职业文化。

✅ 作者呼吁：

- 停止在职位描述和日常交流中使用“手工测试”这一称谓。
- 教育团队认识到非自动化测试同样关键。
- 重视能力多样性，而不是把“是否会写自动化脚本”作为衡量标准。

总之：**测试是认知性的工作，不是执行性的流程，我们需要用更精准、更有尊重的语言去描述它。**

### 质量常数：思考与行动要具有实验性(英文)

https://testerstories.com/2025/04/the-quality-constant-think-and-act-experimentally/

1. 作者将“光速是时空的中介”类比为测试工作中的核心理念，强调测试的本质是通过实验不断获得洞察与调整方向。
2. 他建议测试人员培养“实验性思维”，通过不断设计小实验、观察反馈、快速纠错来降低错误成本并提升产品质量。
3. 测试不仅是发现错误，更是通过构建证据、分析因果、讲述质量故事，为整个软件开发过程注入信心与洞察力。

## 自动化测试

### 如何测试 grpc 服务(英文)

https://medium.com/@alexshamrai/grpc-testing-intro-writing-the-first-test-ac816fbae19d

面向新手的 grpc 测试教程，例子比较简单，但过程很完整。

包含了正常场景和异常场景的测试用例。

### 自动化测试中使用 Docker 多阶段构建(multi-stage builds)来优化测试环境(英文)

https://www.thegreenreport.blog/articles/docker-multi-stage-builds-the-secret-weapon-for-efficient-qa-automation/docker-multi-stage-builds-the-secret-weapon-for-efficient-qa-automation.html

传统 Docker 测试容器存在一些问题

- 包含不必要的构建工具、依赖、源代码和中间构建产物，导致镜像体积大
- 构建慢
- 网络传输时间长
- 启动慢且消耗更多资源

多阶段构建通过在 Dockerfile 中使用多个 FROM 语句，允许从一个阶段选择性地复制构件到另一个阶段，丢弃不需要的部分。

作者提供了一个 Python 网页应用测试环境的实例，分为三个阶段：

- 构建依赖阶段：使用完整 Python 镜像预构建 Python 依赖包
- Chrome 和 driver 准备阶段：基于精简 Debian 镜像安装 Chrome 和 ChromeDriver
- 最终精简测试镜像：使用 slim Python 镜像，只复制前两个阶段中必要的文件和依赖

这种方法的好处包括：

- 镜像体积减少约 70%，加快存储、网络传输和启动时间
- 提高安全性，减少潜在漏洞
- 提供更接近生产环境的测试环境
- 利用 Docker 缓存机制加速构建过程

### 如何使用 Playwright 插件来简化 API 测试中的 JSON Schema 校验工作(英文)

https://dev.to/sebastianclavijo/new-playwright-ajv-schema-validator-for-api-testing-191e

插件亮点：

- 基于广泛使用的 Ajv（Another JSON Schema Validator）构建。

- 支持 JSON Schema、OpenAPI 3、Swagger 2 等格式的验证。

- 通过提供 endpoint、method 和 status，插件会自动从 OpenAPI/Swagger 文档中提取对应 schema 并进行验证。

- 与 Playwright 的标准 API 请求兼容，也可与 pwApi 和 pwAxios 无缝集成。

- 提供详细的验证结果展示，包括错误数量、具体错误信息、定位错误字段等。

断言的例子。只需要定义`schemaDoc`就可以自动断言了。

```javascript
// Get your schema doc from a URL or a file
const schemaDoc = ...
// Make API call and get the 'response'
const data = response.body

const validationResult = await validateSchema(
    { page },
    data,
    schemaDoc,
    { endpoint: '/api/resource', method: 'POST', status: 201}
);
```

## 感受

很多年前机器比人工贵，所以招人做测试比较划算。

现在人工比机器贵，所以要求用自动化的方式让机器去做测试。

未来人工比 AI 贵，AI 所以大部分的测试工作都可以让 AI 去完成了吧？

未来的行业，只要从业人员的薪资大于 AI 需要的电费，那么基本上都会被替代了吧？
