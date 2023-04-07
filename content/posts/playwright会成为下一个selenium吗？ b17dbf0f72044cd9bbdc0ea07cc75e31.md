{"title": "playwright\u4f1a\u6210\u4e3a\u4e0b\u4e00\u4e2aselenium\u5417\uff1f", "draft": false, "date": "2023-04-07T14:39:24+08:00"}

playwright是微软推出的一款e2e（端到端）测试工具，支持多种语言及浏览器，那么它会成为下一个selenium吗？前几天看到外国的一篇文章发表了其观点，这里翻译了一下**并夹杂了一点点的私货**，希望可以对大家所有帮助。

selenium作为浏览器自动化项目来说是非常成功的存在。Selenium现在已经被下载了几百万次，并继续在全球范围内被广泛接受和使用。

### Selenium的成功的原因

1. Selenium是开源的，支持多种（如Java、C#、Js、Python、Ruby、Perl等），支持所有的浏览器（chrome、firefox、edge、ie、safari、opera等），可以在多种操作系统（Windows、MAC、Linux）上运行。
2. Selenium功能强大--它可以做web测试，也能做跨浏览器兼容性测试。另外selenium设计的初衷是浏览器的自动化，所以除了用作测试之外，selenium还在web自动化操作领域有所建树。
3. Selenium有一个庞大的用户社区，可以帮助你快速入门。
4. 与其他开源工具相比，Selenium非常稳定，它的实现甚至成了标准的w3c协议。
5. 最后，Selenium社区是充满活力的，定期举行许多活动和研讨会，你可以与志同道合的人讨论最新的工具和技术。

### playwright会成为下一个selenium吗？

考虑到现代Web应用自动化，Selenium WebDriver似乎是最受欢迎的工具之一，然而，像Playwright、Puppeteer、Cypress这样的替代工具正在出现，并争取在一段长时间之后能对其进行超越。

Playwright是一个JavaScript框架，支持在前端实现Web应用程序的自动化。它在后端使用Node.js，就像Puppeteer那样。它扩展了该框架，为用户提供了编写端到端测试或隔离测试应用程序特定部分所需的所有工具。

支持使用包括Java、Js、C#、Python在内的语言编写测试用例，并像Selenium WebDriver一样在任何浏览器和任何操作系统上运行。它是开源的，很容易使用，支持单兵作战和团队协同。

在UI自动化领域，Playwright能够成为下一个Selenium的主要原因有以下七个方面。

- Playwright得到了微软的支持，其作者来自Puppeteer（谷歌）团队，因此playwright可以吸收Puppeteer积极的方面。另外，它已经了一些版本来支持多种编程语言，社区的反馈也非常积极。简而言之微软的钞能力和干爹属性使其相对其他开源项目来说可能会有更多的持续性。

- Playwright的架构更简化，它摆脱了selenium复杂的设置和维护本地driver的繁琐过程，基本上开箱即用，工程化方面的实践也更加深入。初学selenium的同学应该记得selenium安装之后没有下载driver的话就是不能用的，特定版本的浏览器需要特定版本的driver配合，对于一些长期项目的维护来说确实有时候会带来额外的工作量。

- Playwright的测试执行速度非常高（平均比selenium快40%），因为它使用JavaScript引擎如Node.js来运行测试，而不是Selenium的driver程序。因此，与Selenium WebDriver相比，使用Playright可以大大降低测试执行时间。

- 与Selenium WebDriver不同，Playwright除了支持测试页面的全屏截图外，还支持边测试边录屏，感觉现代化了不少。

- 与Selenium WebDriver相比，Playright的维护成本更低，因为它使用内部等待，而不像Selenium WebDriver需要管理显式等待。这大大降低了总的代码编写和维护成本。

- Playwright除了支持web自动化测试外，还支持RESTFul API测试。这使测试人员可以灵活地使用Playwright测试他们的后端服务。

- 最后，Playwright可以跟浏览器的开发者工具进行集成，这使得用Playwright编写开发测试非常容易和简单。

![Untitled](playwright%E4%BC%9A%E6%88%90%E4%B8%BA%E4%B8%8B%E4%B8%80%E4%B8%AAselenium%E5%90%97%EF%BC%9F%20b17dbf0f72044cd9bbdc0ea07cc75e31/Untitled.png)

原文地址：[https://medium.com/testleaftechblog/will-playwright-become-next-selenium-b41eebfa5d25](https://medium.com/testleaftechblog/will-playwright-become-next-selenium-b41eebfa5d25)