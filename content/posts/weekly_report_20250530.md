---
title: "测试周刊004: 单元测试和接口测试用例将成为标配"
date: 2025-05-30T09:26:37+08:00
draft: false
---

马上就到端午假期了。

今天在电梯听到两位女士的对话，大概的意思是一位认为只有一天的假期有点不太过瘾，而另一位觉得假期归来以后上 4 休 2 已经是非常划算了。

反正我是同意后者的。

## 观点

### AI 将使得单元测试和接口测试成为标配

前些天 deepseek 发布了新模型，该模型在代码能力上有了较大的提升。

有人尝试之后表示模型不仅可以正确实现编码需求，还可以在生成代码的同时给出完整的单元测试用例。

今后将有越来越多的代码会由 ai 实现，而我们可以非常自信的要求 ai 在给出实现的同时，给出完成的单元测试用例和接口测试用例。

因此在不久的将来，单元测试用例和接口测试用例将会成为增量代码的标配了吧。

测试同学可能不需要人人都会写单元测试用例了，但是学会看懂测试用例，并用测试思维来对用例进行评审，反而是更实用的技能了。

### 从质量保证到集成保证

https://medium.com/@sean.zhang/lets-rethink-the-role-of-qa-it-s-not-about-owning-quality-ed159d0a424b

传统的"质量保证"概念存在两个极端问题：

- 过度依赖 QA：认为 QA 团队独自负责产品质量，其他团队可以推卸责任
- 完全取消 QA：认为每个工程师都应该"拥有质量"，但缺乏系统级验证

作者认为传统的"质量保证"（QA）概念存在误导性，因为质量应该是每个团队的共同责任，而不是 QA 部门的专属职责。

他提出将 QA 重新定义为"集成保证"（Integration Assurance），专注于验证现代软件系统中多个服务和组件之间的协同工作，就像苹果公司需要确保 iPhone 各个供应商的零件能完美集成一样。

这个角色类似足球比赛中的守门员——不是唯一的防线，但是防止问题到达用户的最后屏障，同时帮助发现系统级的协调问题和集成风险，而 AI 测试工具应该主要由这个集成保证团队来使用，以确保从全局视角进行有效的端到端验证。

## 自动化测试

### 有效的软件测试需要通过测试替身（Test Doubles）来隔离被测系统，从而编写可控、可靠的单元测试

https://medium.com/@raissa.puti/behind-the-green-check-a-guide-to-test-doubles-7199be3b08c2

作者认为，真正的测试不仅仅是检查功能是否正常运行，而是要通过 Dummy、Stub、Spy、Mock、Fake 等不同类型的测试替身来替代真实的外部依赖（如 API、数据库、时间服务等），这样可以：

- 控制测试环境和输入数据，
- 验证特定的交互行为，
- 避免依赖不稳定的外部服务
- 提高测试速度和可靠性。

作者以自己的 React 项目 SiNgawas 为例，展示了如何在前端测试中应用这些概念，同时分享了借助 AI 工具来改进测试设计的经验。文章强调，好的测试应该专注于验证有意义的行为，而不是简单地检查 UI 渲染，通过合理使用测试替身可以让每个测试都有明确的目的和可预测的结果。

### playwright 断言中的各种坑

https://0xislamtaha.medium.com/part-2-count-me-out-assert-me-wrong-two-sneaky-playwright-pitfalls-5b53639f645f

- .count()、.all()、.isVisible() 和 .isHidden() 都是"急躁"的方法，不会等待
- 需要显式等待来避免不稳定性
- 了解哪些断言会重试，哪些不会
- 使用 toPass() 将非重试断言转换为可重试的
- 合理设置超时时间（toPass() 默认超时为 0）

比如

```javascript
// 等待特定数量的元素
await expect(page.locator("[data-testid='listItems']")).toHaveCount(5);

// 或等待至少达到某个数量
await expect(page.locator("[data-testid='listItems']")).toHaveCount(
  expect.any(Number)
);

await expect(async () => {
  expect(
    await page.locator('[data-testid="listItems"]').count()
  ).toBeGreaterThan(5);
}).toPass({ timeout: 2 * 60 * 1000 });
```

### 实用 PactumJS 进行接口测试

https://noraweisser.com/2025/05/12/what-makes-pactumjs-awesome-a-quick-look-at-its-best-features

pactumjs 的写法有点复古，有点当年流利编程的意思。比如下面的例子：

```javascript
describe("/authenticate", () => {
  it("POST with existing username and valid password", async () => {
    await spec()
      .post("/auth/login")
      .inspect()
      .withHeaders("Content-Type", "application/json")
      .withJson({
        username: process.env.USERNAME,
        password: process.env.PASSWORD,
      })
      .expectStatus(200)
      .expectJsonSchema(authenticationSchema);
  });

  it("POST with existing username and invalid password", async () => {
    await spec()
      .post("/auth/login")
      .inspect()
      .withHeaders("Content-Type", "application/json")
      .withJson({
        username: process.env.USERNAME,
        password: faker.internet.password(),
      })
      .expectStatus(401)
      .expectJsonMatch("error", "Invalid credentials");
  });

  it("POST with non-existing username and password", async () => {
    await spec()
      .post("/auth/login")
      .inspect()
      .withHeaders("Content-Type", "application/json")
      .withJson({
        username: faker.internet.username(),
        password: faker.internet.password(),
      })
      .expectStatus(401)
      .expectJsonMatch("error", "Invalid credentials");
  });
});
```

该框架还支持 json schema 断言和数据模版这些比较现代化的功能。

总之 PactumJS 是一个设计良好、对开发者友好的 API 测试自动化工具。

其流畅的语法、强大的数据处理能力以及内置的各种功能（如模式验证和动态存储）消除了开发第三方解决方案的需求，对于 JavaScript/TypeScript 的 API 测试项目来说非常值得考虑。

## 工具

### Grafana k6 1.0 正式发布

Grafana k6 1.0 的正式发布，这是该开源性能测试工具的首个主要版本。

#### 主要特点

- **语义化版本控制**：采用 SemVer 标准，重大更改只在主版本中引入
- **支持保证**：每个主要版本至少提供两年的关键修复支持
- **公共 API 接口**：为扩展开发提供稳定的 Go 模块接口

#### 主要新功能

1. **原生 TypeScript 支持**

   - 无需转译，直接支持 TypeScript
   - 提供类型安全和 IDE 自动完成功能

2. **扩展支持**

   - 支持预批准的扩展程序
   - 在 Grafana Cloud k6 中开箱即用
   - 自动处理依赖关系

3. **改进的测试结果**

   - 现代化的测试报告
   - 场景特定和分组特定的指标
   - 分层结果分组和改进的检查结果

4. **其他质量改进**
   - 稳定化的模块（k6/browser、k6/net/grpc、k6/crypto）
   - 增强的 Grafana Cloud 集成
   - 重构的 k6 cloud 命令

#### 社区成就

- GitHub 上超过 27,000 星标
- 200+ 贡献者
- 全球各时区的团队在使用

  1.0 版本标志着 k6 从性能测试工具演进为端到端可靠性测试解决方案的重要里程碑。

## 言论

> 我们正在进入一个世界，在这个世界里，最先进的系统无法提供正确性的证明，只能提供意图的概率。这要求我们彻底重新思考如何定义软件质量、合同保证和法律责任。这对法院和立法机构提出了挑战，要求它们跟上一个已经超越了旨在规范它的框架的技术范式。
> 在我们承认这些变化——并将其反映在我们的实践、合同和期望中——之前，我们是在沙子上建立信任。这不是创新，这是幻觉。
> by Dick Dowdell
