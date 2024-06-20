---
title: "活久见!性能测试工具Gatling支持javascript了"
date: 2024-05-31T07:53:06+08:00
draft: false
---

很久之前给大家介绍过一款性能测试工具 Gatling。该工具有开源版本和企业版本，一般情况下我们只关注开源版本，毕竟企业版还是非常贵的。之前的开源版本中，测试脚本是用 Scala 写的，这门语言有点高阶，写起来不顺手，不过 2024 年的今天，情况有所改变。

Gatling 团队 5 月 23 日宣布，他们已为 Gatling 负载测试新增了 JavaScript 和 TypeScript SDK。这个新的 JavaScript SDK 是 npm 库中第一个企业级负载测试工具，使更多的开发者能够使用他们熟悉的编程语言进行 Gatling 负载测试。

自从 Gatling 推出以来，它一直是一个基于 Java 虚拟机（JVM）的开发工具，专注于负载测试。现在，开发者可以使用 Gatling JavaScript SDK 编写负载测试，并将测试编译在 JVM 上运行。这结合了脚本语言的灵活性和多线程等必要的性能特性。

最重要的是，使用 Gatling 不再局限于 Java 开发者。通过 npm 安装命令设置项目，熟悉的语法使 JavaScript 开发者可以轻松上手，同时拥有 Gatling 引擎的强大功能来运行负载测试。

### 为什么 Gatling 团队开发了 JavaScript 和 TypeScript SDK？

JavaScript 生态系统的惊人发展是不可否认的。最初，它只是一个前端脚本语言。随着 NodeJS 和 TypeScript 的出现，它现在成为构建现代 Web 应用程序和 API 的全栈、类型安全的语言。根据某些估计，JavaScript 是 98%财富 500 强企业技术栈的一部分。

### Java 和 JavaScript 的历史

Java 和 JavaScript 的历史从一开始就紧密相连。两种语言都是在硅谷开发并于 1995 年发布的。JavaScript 最初被称为 Mocha，但 Netscape 将其改名为 JavaScript，以利用 Java 日益增长的人气。

多年来，这两种语言在很大程度上是互补的，Java 作为服务器端的主力，而 JavaScript 则为浏览器中的网站和应用程序提供动力。从一开始，Netscape 的开发者就意识到了在服务器端运行 JavaScript 的潜力。

1997 年，Netscape 开始开发 Rhino，一个能够在 JVM 上运行的 JavaScript 引擎。尽管 Rhino 有编译和解释版本，但仍然存在性能问题。Oracle 后来开发了 Nashorn 取代 Rhino，但由于 JavaScript 生态系统的发展过快，Nashorn 在 Java 11 中被弃用。

在弃用 Nashorn 后不久，Oracle 发布了 GraalVM，这是一个可供社区和企业使用的 Java 开发工具包（JDK）。GraalVM 是流行的 OpenJDK 的替代品，包括以下功能：

- Graal 编译器，即时编译器（JIT）。
- GraalVM 原生映像，提前编译 Java 应用程序。
- Truffle 语言实现框架和 GraalVM SDK，为其他编程语言的实现提供 Java 框架。
- GraalVM 多语言 API，在 Java 主机应用程序中嵌入客语言代码。
- JavaScript 运行时，符合 ECMAScript 2023 标准的 JavaScript 和 Node.js 运行时。
- LLVM 运行时，执行可以翻译成 LLVM 位代码的语言。

GraalVM 的发布促使 Gatling 的开发者开始着手开发 JavaScript SDK。

### 技术细节

SDK 的目标是允许 Gatling 用户完全使用 JavaScript 或 TypeScript 编写负载测试模拟。用户还可以包括自己喜欢的 npm 库，同时利用 Gatling 健壮且经过良好测试的代码库。

为实现这一目标，Gatling 团队在 GraalVM 上运行，这是一个多语言虚拟机，能够在同一环境中运行多种编程语言的代码。JavaScript 支持来自 GraalJS 项目。

当开发者用 JavaScript 编写模拟时，他们对 SDK 的所有调用都会被转换为对 Gatling Java SDK 的调用。模拟然后可以在与用 Java、Kotlin 或 Scala 编写的模拟相同的 Gatling 引擎上运行。

使用 JavaScript 或 TypeScript 的唯一前提是安装 NodeJS（带有 npm）。当开发者运行第一个负载测试时，Gatling-js CLI 会下载 GraalVM 和一些 Java 库以启用 Gatling 引擎。

JavaScript SDK 还支持 Gatling Recorder，这是一个应用程序，可以捕获基于浏览器的用户操作并将其转换为负载测试脚本。如果开发者是负载测试的新手，Recorder 是学习复杂场景脚本的另一个绝佳工具。

### 接下来的计划

Gatling JavaScript SDK 的首个版本涵盖了几乎所有 Java SDK 可用的 HTTP 协议功能。作为 Gatling 开放核心承诺的一部分，并遵循 Apache 2.0 许可证，所有 Gatling 用户都可以使用。Gatling 团队正在积极推进三个项目，以扩展 JavaScript 开发者的体验：

- 在 Gatling Enterprise 上支持 JavaScript 和 TypeScript。
- 扩展 SDK 以涵盖更多协议，如 WebSocket 和 gRPC。

Gatling 团队知道一些现有客户非常期待将 Gatling 的使用扩展到他们的 JavaScript 和 TypeScript 开发者，因此 Gatling Enterprise 的支持正在进行中。团队将在接下来的几周内分享更多细节。

### 看下测试脚本究竟怎么写的

翻了一下文档，目前 js 的 sdk 只支持发送 http 请求，坦白来说竞争力还是不足的，毕竟 k6 就支持 js，而且特性更加丰富。不过我们也看到，gatling 还是有计划为 js sdk 提供更多的协议支持的。

根据官方文档，简单的 js 的测试脚本如下

```javascript
import { constantUsersPerSec, scenario, simulation } from "@gatling.io/core";
import { http } from "@gatling.io/http";

export default simulation((setUp) => {
  const httpProtocol = http
    .baseUrl("https://computer-database.gatling.io")
    .acceptHeader("application/json")
    .contentTypeHeader("application/json");

  const myScenario = scenario("My Scenario").exec(
    http("Request 1").get("/computers/")
  );

  setUp(myScenario.injectOpen(constantUsersPerSec(2).during(60))).protocols(
    httpProtocol
  );
});
```

看起来还不错，实话实说跟其他家支持 js 的性能工具比较的话，同质化还是很严重的。这里就不展开了，顺便一提 Gatling 的本地安装过程有一点点的纯新手劝退，所以要跑起来的话可能会相对麻烦一点点。

说实话我还是非常期待后面的 typescript 版本的，因为上了 ts 之后，就有完备的代码提示效果了，这对新手来说非常重要。

### 总结

新的 js sdk 的引入给 Gatling 这款冷门的性能测试工具增加了一点点的活力，目前来说只是初级阶段，并没有给人带来太多的惊喜。然而只要是只支持纯脚本的测试工具，怎么看来都是专业和相对冷门的选择，很难广泛的流行开来。这样看来，支持哪种类型的脚本语言其实并不重要了吧。
