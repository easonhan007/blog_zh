---
title: "2023年 Selenium 是否正在消亡"
date: 2023-10-16T18:42:38+08:00
draft: true
---
看到一篇文章[Is Selenium Dead? Explore the State of Selenium Automation in 2023 !](https://sdetunicorns.com/blog/is-selenium-dead)，里面比较详细的描述了2023年selenium的现状以及竞品分析，感觉还是非常全面的，简单的翻译了一下，供大家参考。


技术世界中，工具和技术以飞快的速度发展，软件测试也不例外。在过去的几年里，涌现出了许多新的测试工具（如 Cypress、Playwright 和 Robot Framework 等），每种工具都有其独特的特性和方法来解决同一个问题：测试自动化。

然而，在测试自动化领域，多年来只有一个框架一直是基石：Selenium。它已经存在并开源了 15 年以上，直到最近，一场激烈的争论浮出水面：Selenium 是否已死？是否存在更好的替代品？它是否在面对新的测试工具和方法时失去了竞争力？

在这篇文章中，我将从自己的角度深入探讨 Selenium 在 2023 年的现状，探索其相对于竞争对手的优势和劣势，以及在快速变化的外部世界中中面临的挑战。

## 前提条件：

* 成为一名 QA 爱好者 😉

### Selenium 的崛起和统治

Selenium 最初由 Jason Huggins 于 2004 年开发，作为一个基于 JavaScript 的自动化工具（名为 JavaScriptTestRunner），用于自动化内部应用程序的测试，该应用程序需要耗费大量的手工工作。多年来，随着他意识到该程序的潜力，它演变成了 Selenium-core 并开源。然后，通过多位贡献者实现了许多功能，例如：

* Selenium IDE：它支持通过录制和回放功能运行自动化测试
* Selenium Grid：一种强大的功能，可以执行并行测试，以将测试执行时间减少到最低限度
* Selenium 2：这是 Selenium 1 和 Webdriver 的合并，形成了我们今天所知道的工具。

自 Selenium 2 以来，它获得了很大的关注度，其受欢迎程度迅速上升，这可以归因于几个关键因素，这些因素改变了游戏规则：

* 开源：Selenium 是开源的，这意味着它可以免费使用，并有一个庞大的社区可以帮助您解决遇到的任何问题，并有许多贡献者和用户。这导致了持续的改进和更新。
* 跨浏览器兼容性：Selenium 支持各种网络浏览器，如 Chrome、Firefox、Safari、Edge 和 Internet Explorer，使其成为网络应用程序测试的通用选择。
* 多种编程语言：Selenium 兼容多种编程语言，包括 Java、Python、C#、Ruby、JavaScript 和最近的 Kotlin。测试自动化工程师可以选择他们喜欢的语言进行测试自动化。
* 广泛采用：许多组织和公司已将 Selenium 纳入其测试自动化套件中，这导致了大量的资源、教程和支持在线可用。（现在，我自己也为我的雇主的公司管理着一个 Selenium 套件 😉）
* 与测试框架的集成：Selenium 可以与流行的测试框架如 TestNG 和 Cucumber 集成，从而实现结构化的测试用例管理和报告。
* 并行性：Selenium 使用 Selenium Grid 支持强大的测试用例并行性，这大大减少了执行时间。


**Selenium 在 2023 年的现状：已死还是未死？**

截至 2023 年，Selenium 远未消亡。它仍然是全球许多软件测试团队的重要工具，这主要归功于使其从一开始就流行起来的相同因素。

让我们研究一下其当前状态的一些关键方面：

* **持续开发：** Selenium 项目继续发布更新和改进。社区非常活跃，解决问题、添加新功能并确保 Selenium 与最新的浏览器版本兼容。
* **庞大的社区：** Selenium 的用户社区非常庞大，提供丰富的资源、论坛和讨论组，测试人员可以在其中寻求帮助和分享知识。
* **兼容性：** Selenium WebDriver 仍然兼容所有主要浏览器，确保测试人员可以有效地执行跨浏览器测试。
* **编程语言支持：** Selenium 提供对各种编程语言的支持，例如 Java、JavaScript、Ruby、C#、Kotlin 等，使其能够适应您的团队偏好和技术栈。
* **集成和生态系统：** Selenium 可以与各种工具和框架集成，例如 TestNG、Cucumber 和 Jenkins for CI/CD，以增强其功能并促进无缝的自动化工作流程。
* **云端测试：** Selenium 与云端测试平台的集成使得在各种浏览器版本和设备上执行测试变得更加容易，从而实现更广泛的测试覆盖率。

**Selenium 4.0 最新版本功能**

当 Selenium 4.0 在 2021 年推出时，它在功能和特性方面进行了全新的改造，使其获得了巨大的关注度。

* **改进后的 Selenium Grid：** 任何之前使用过 Selenium Grid 的人都知道它很难设置。新的 Selenium Grid 提供 docker 支持，使我们能够顺利地启动容器，并提供 3 种模式：独立模式、Hub 和 Node 或完全分布式模式。
* **升级后的 Selenium IDE：** 旧的 IDE 因新浏览器的版本而被弃用。现在它重新复活，并提供丰富的功能，如：直观的 GUI、改进的控制流机制、增强的元素定位策略，现在，测试可以用 Selenium 支持的任何语言导出。
* **改进的文档：** 文档已经过重新编写，使其具有简洁的用户界面，并涵盖您需要了解的有关 Selenium 的所有内容，如果您是 Selenium 初学者，我强烈建议您阅读一下。
* **相对定位器：** Selenium 4 引入了一种使用相对直观术语（例如：To left of、To right of、Above、Below）定位元素的新方法。
* **更好的窗口和选项卡管理：** 在 Selenium 3 中，打开新窗口需要大量“黑客手段”。因此，Selenium 社区现在提供了一个新的 API：“newWindow”，该 API 允许用户创建和切换到一个新的窗口/选项卡。


**基于 Selenium 的框架**

Selenium 如此广泛使用的另一个原因是其庞大的生态系统。以下是基于 Selenium 构建的一些非常有趣和广泛使用的框架：

* Java: FluentLenium, Selenide
* Python: Robot Framework, SeleniumBase
* JavaScript: CodeceptJS, Nightwatch.js, Boyka Framework
* C#: Atata, Boa Constrictor

我强烈建议您尝试这些框架，因为它们可以解决许多纯 Selenium 的痛点。

**Selenium 在 2023 年面临的挑战**

虽然 Selenium 仍然被广泛使用，但也存在一些挑战，可能会或可能不会阻碍您的测试自动化之旅。

以下是我使用 Selenium 时遇到的一些局限性：

* 复杂性：Selenium 自动化可能很复杂，尤其是初学者。设置和配置环境、编写稳定且可维护的测试脚本以及处理动态网页元素对于初学者来说可能很 daunting，这会导致更大的学习曲线。
* 脆弱性：Selenium 测试可能容易出现脆弱性，这意味着由于网络延迟、浏览器行为或元素可见性（因为 Selenium 并非专为最新的前端框架而设计）等因素，它们可能会产生不一致的结果。测试脆弱性可能会令人沮丧且耗时。
* 调试：Selenium 与其竞争对手相比缺少一个有用的功能：Snapshots。它们使您能够跟踪代码及其在浏览器中的结果，并通过使您能够返回到精确的代码行并查看其在浏览器中的结果来大大促进调试。

**Selenium 的替代品**

让我们来看看最流行的 Selenium 替代品并进行比较。

* Cypress：Cypress 是一个基于 JavaScript 的端到端测试框架，强调速度和可靠性。它提供实时重新加载和 Snapshots，并为现代 Web 应用程序提供出色的支持。

优点：
    * 具有 Snapshots 功能，可大大促进调试
    * 更好的用户界面和开发人员体验
    * 入门学习曲线较低

* Playwright：Playwright 是由 Microsoft 开发的跨浏览器和跨平台自动化库，用于 JavaScript 和 Python。它提供了一个统一的 API 来自动化浏览器（Chrome、Firefox、WebKit）并支持多种语言，如 TypeScript、JavaScript、Python、.NET 和 Java。

优点：
    * 更多内置功能
    * 更好的调试工具
    * 更容易上手

* WebDriverIO：WebDriverIO 是一个基于 NodeJS 的自动化测试框架。官方网站将 WebDriverIO 定义为“一个用于自动化现代 Web 和移动应用程序的渐进式自动化框架。它简化了与应用程序的交互，并提供了一组插件来帮助您创建可扩展、强大且稳定的测试套件。”

优点：
    * 支持浏览器、桌面和移动测试。
    * 专为使用 React、Vue、Svelte 等前端框架编写的现代 Web 应用程序进行测试而构建。

### 结论

总而言之，在 2023 年，Selenium 远未消亡。

它仍然占据着企业中最流行的工具的宝座。我们可以说，这主要是因为大多数代码库都是旧的，但它仍然是相关的。Selenium 技能在全球范围内都有巨大的吸引力和大量的职位空缺。公司有基于 Selenium 的庞大的测试套件。而且，就像任何代码库一样，它们需要维护、新功能和更新。所有这些都确保了 Selenium 社区将只会越来越大，其贡献者也将越来越多。

即使在创业界，我也看到了对 Selenium 自动化的需求，这主要是因为它的效率和韧性毋庸置疑。

然而，我不能否认它确实面临一些挑战：从测试脚本的复杂性到调试，再加上功能更丰富的替代测试工具的出现。

Selenium 的未来将取决于它适应不断变化的测试趋势和技术的能力，就像它之前所做的那样。凭借持续的开发工作、与云端服务的集成以及调试工具和报告的改进，Selenium 可以保持其软件自动化之王的宝座。

最终，如果您需要在 Selenium 和其他替代方案之间进行选择，您的选择应取决于您的测试项目的具体要求、您的团队的技能和您的组织不断变化的需求。Selenium 可能最受欢迎，但这并不意味着它是所有用例的最佳工具。