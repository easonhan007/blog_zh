---
title: "Unit Test Best Practice"
date: 2023-08-18T10:19:49+08:00
draft: false
---

看到一篇关于单元测试最佳实践的文章，简单翻译一下，很多都说到了点子上，不能赞同更多。

单元测试是对软件应用程序中各个单元或组件进行的软件测试。单元测试旨在验证每个软件单元的执行是否符合设计预期。单元测试可以确保代码质量,提高可维护性,方便重构,并提高开发速度。

当谈到最佳实践时,这里有一些应该遵循的:

1. 为每个缺陷编写新测试:当你遇到一个缺陷时,编写一个暴露该缺陷的测试。这也称为回归测试。

2. 保持测试的小而聚焦:一个单元测试应该限制在一个独立的函数或方法中。这使得当测试失败时更容易识别和修复问题。

3. **隔离你的测试**:确保每个测试都是相互独立的。这允许你单独运行每个测试,并以任意顺序运行。(划重点了)

4. 按测试类型组织测试:你可以根据它们测试的对象类型或测试类型来组织测试。这使得查找和运行相关测试更容易。

5. 每次测试一条代码路径:每个测试应该验证方法中的一条明确的代码路径。这使得理解被测试的内容以及测试可能失败的原因更容易。

6. **避免在测试中加入逻辑**:当你在测试中加入逻辑时,你有引入测试缺陷的风险。保持测试的简单。(重点)

7. 避免在被测试的类中使用静态方法:静态方法不能在子类中重写,这使得它们难以测试。避免在你要测试的类中使用静态方法。

8. 避免测试实现细节:你的测试应该关注代码的行为,而不是它的实现。如果测试实现细节,当你的代码行为保持不变时,测试仍可能中断。

9. 首先为对应用影响最大的方法编写测试:将测试工作集中在对应用影响最大的方法上。这通常包括包含复杂逻辑或与外部资源交互的方法。

10. **使用 AAA 模式**:准备测试数据和测试环境(Arrange)、执行(Act)、断言(Assert)是编写单元测试的典型模式。单元测试方法的安排部分初始化对象和传递给被测试方法的数据值。执行部分调用带有Arrange参数的被测试方法。断言部分验证被测试方法的行为符合预期。(划重点)


原文如下:

𝗨𝗻𝗶𝘁 𝗧𝗲𝘀𝘁𝗶𝗻𝗴 𝗕𝗲𝘀𝘁 𝗣𝗿𝗮𝗰𝘁𝗶𝗰𝗲𝘀

Unit tests are software testing where individual units or components of a software application are tested. Unit testing aims to validate that each software unit performs as designed. Unit tests ensure code quality, and ease of maintenance, facilitates refactoring, and increase development speed.

When we talk about best practices, here is a list of that one should follow:

𝟭. 𝗪𝗿𝗶𝘁𝗲 𝗮 𝗻𝗲𝘄 𝘁𝗲𝘀𝘁 𝗳𝗼𝗿 𝗲𝘃𝗲𝗿𝘆 𝗱𝗲𝗳𝗲𝗰𝘁: When you encounter a defect, write a test that exposes the defect. This is also known as regression testing.

𝟮. 𝗞𝗲𝗲𝗽 𝘁𝗲𝘀𝘁𝘀 𝘀𝗺𝗮𝗹𝗹 𝗮𝗻𝗱 𝗳𝗼𝗰𝘂𝘀𝗲𝗱: A unit test should be limited to an individual function or method. This makes it easier to identify and fix problems when the test fails.

𝟯. 𝗜𝘀𝗼𝗹𝗮𝘁𝗲 𝘆𝗼𝘂𝗿 𝘁𝗲𝘀𝘁𝘀: Make sure each test is independent of all the others. This allows you to run each test individually and in any order.

𝟰. 𝗢𝗿𝗴𝗮𝗻𝗶𝘇𝗲 𝘆𝗼𝘂𝗿 𝘁𝗲𝘀𝘁𝘀 𝗯𝘆 𝘁𝗲𝘀𝘁 𝘁𝘆𝗽𝗲: You can organize your tests by the type of object they are testing or the type of test they are. This makes it easier to find and run related tests.

𝟱. 𝗧𝗲𝘀𝘁 𝗼𝗻𝗲 𝗰𝗼𝗱𝗲 𝗽𝗮𝘁𝗵 𝗮𝘁 𝗮 𝘁𝗶𝗺𝗲: Each test should verify one specific code path through a method. This makes it easier to understand what is being tested and why a test might fail.

𝟲. 𝗔𝘃𝗼𝗶𝗱 𝗹𝗼𝗴𝗶𝗰 𝗶𝗻 𝘁𝗲𝘀𝘁𝘀: When you put logic into your tests, you risk introducing bugs into your tests. Keep your tests simple.

𝟳. 𝗔𝘃𝗼𝗶𝗱 𝘀𝘁𝗮𝘁𝗶𝗰 𝗺𝗲𝘁𝗵𝗼𝗱𝘀 𝗶𝗻 𝘆𝗼𝘂𝗿 𝗰𝗹𝗮𝘀𝘀𝗲𝘀 𝘂𝗻𝗱𝗲𝗿 𝘁𝗲𝘀𝘁: Static methods can't be overridden in subclasses, which makes them difficult to test. Avoid using static methods in the classes you are testing.

𝟴. 𝗔𝘃𝗼𝗶𝗱 𝘁𝗲𝘀𝘁𝗶𝗻𝗴 𝗶𝗺𝗽𝗹𝗲𝗺𝗲𝗻𝘁𝗮𝘁𝗶𝗼𝗻 𝗱𝗲𝘁𝗮𝗶𝗹𝘀: Your tests should focus on the behavior of your code, not its implementation. If you test implementation details, your tests can break even if the behavior of your code remains the same.

𝟵. 𝗪𝗿𝗶𝘁𝗲 𝘁𝗲𝘀𝘁𝘀 𝗳𝗼𝗿 𝗺𝗲𝘁𝗵𝗼𝗱𝘀 𝘁𝗵𝗮𝘁 𝗵𝗮𝘃𝗲 𝘁𝗵𝗲 𝗺𝗼𝘀𝘁 𝗶𝗺𝗽𝗮𝗰𝘁 𝗳𝗶𝗿𝘀𝘁: Focus your testing efforts on the methods that impact your application most. This typically includes methods containing complex logic or interacting with external resources.

𝟭𝟬. 𝗨𝘀𝗲 𝘁𝗵𝗲 𝗔𝗔𝗔 𝗽𝗮𝘁𝘁𝗲𝗿𝗻: Arrange, Act, Assert is a typical pattern for writing unit tests. The Arrange section of a unit test method initializes objects and sets the data value passed to the method under test. The Act section invokes the method under test with the arranged parameters. The Assert section verifies that the action of the method under test behaves as expected.
