---
title: "推荐1个很有用的测试wiki"
date: 2024-01-09T16:59:55+08:00
draft: false
---

https://ray.run/wiki

这个网站应该是我见过最全面的关于测试领域的知识整理了。稍微写代码数了一下，应该有200多个主要知识点，每个下面都有很多的常见问题。知识点的解释其实没啥突出的，不过常见问题对于面试来说就非常的顺手了。

稍微列举1个有意思的主题。

> Definition of Acceptance Test Driven Development

什么是ATDD?

说实话，这个概念我也是第一次见到。

> What are the key steps involved in ATDD?

ATDD的关键步骤有哪些？

The key steps involved in ATDD are:

- Collaboration among developers, testers, and business stakeholders to define acceptance criteria.
- Creation of acceptance tests before the development starts, based on the agreed-upon criteria.
- Development of the feature or user story, guided by the acceptance tests.
- Continuous Integration to ensure that code changes are automatically tested against the acceptance tests.
- Refinement of the acceptance tests as necessary, to address changes in requirements or understanding.
- Test Execution to validate that the software meets the agreed-upon acceptance criteria.
- Review and Feedback from stakeholders to confirm that the acceptance tests cover the desired functionality and behavior.
- Iteration through these steps as needed until the feature meets the acceptance criteria.

Acceptance tests are typically automated to facilitate frequent execution and regression testing. The tests are written in a language that is understandable by all parties involved, often using Behavior Driven Development (BDD) frameworks like Cucumber or SpecFlow. This ensures that the tests serve as both specification and validation.

```
Feature: User login
  Scenario: Valid login
    Given I am on the login page
    When I enter valid credentials
    Then I should be redirected to the dashboard
```
Effective ATDD requires a strong collaboration culture, clear communication, and a commitment to quality from all team members.

稍微阅读理解一下，发现所谓的ATDD的流程大概是

- 定义测试条件和范围
- 写用例
- 根据用例来写代码
- 重复上面的步骤
- 根据需求变更来修改用例
- 根据用例进行测试
- 根据客户的反馈来判断用例是否覆盖了全部的需求
- 重复上面的步骤，直到产品交付

这里的用例基本上用的是特定的DSL来写的，也就是有自己的语法，一般常用的就有BDD框架支持的语法，比如上面列举的那样。

概念不新鲜，其实是bdd的一种，不过换个名字就真的不认识了。


### 总结

- 这个wiki的内容非常全面，大部分常见的软件测试内容基本上里面都有涵盖
- 里面的内容的准确性需要自己评估，毕竟世界上没有完全正确的观点
- 适合入门以及转码的小伙伴仔细研读，主要关注跟测试流程相关的部分
- 高手和有经验的同学可以用来查缺补漏
- 面试之前可以突击看一下，一些高级岗位可以重点关注里面跟指标相关的部分

