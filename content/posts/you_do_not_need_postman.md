---
title: "postman替代工具2024版"
date: 2024-09-13T09:37:31+08:00
draft: false
---

又又又看到有人发帖抱怨说 postman 太慢了，想找一款可以替代 postman 的工具。这个需求基本上每隔几个月都会被提出来一次。

这里顺手总结一下原帖中提到的解决方案，再加上自己的亲身体验，给大家推荐一些 postman 的替代工具。

反正我坚持认为，postman 只要不登录，速度快点，那么它还是用起来最顺手的 http 请求工具了。

## RapidAPI

mac 用户强推了，当年的版本叫 paw，我是花了不少钱买的。现在完全免费了，妥妥的背刺。

https://paw.cloud/

## Bruno

开源的轻量 API 测试工具，类似 Postman。

下载地址: https://www.usebruno.com/。

主打一个开源以及个人用户不要钱。

## Thunder Client

这个是 vscode 的扩展，很轻量，而且免费，用起来不如 postman 顺手。

## Rest Client

同样也是 vscode 的扩展，用着还行。

## Hoppscotch

今天才之前 Hoppscotch 的前身是之前我们关注过的 postwoman。

工具地址：https://hoppscotch.io/

建议直接用 chrome 的扩展，跟当年的 postman 一样。

## Insomnia

另一个类似 Postman 的 API 工具。

我记得当年是完全开源免费的，现在要收钱了，不过免费的版本完全够用了。

https://insomnia.rest/

## Yaak

这个似乎就是 Insomnia 的原作者新写的工具，目前免费。

https://yaak.app/

## Jmeter

属于啥都能干，但是体验没有 postman 好了，完全免费，怎么都香。

https://jmeter.apache.org/

## CLI 工具

- curl:这个不用多说了
- k6: 做性能测试的，用来调 api 其实也行，但是要写代码
- requests (Python 库): 要写代码
- Playwright API: 还是要写代码
- Supertest - 与 Mocha 和 Chai 结合使用的代码测试框架: 继续要写代码
- HTTPie: 当年是纯 cli，现在似乎有 desktop 版本了？反正 cli 还是很好用的
- Hurl: https://hurl.dev/。看到有人推荐，但没用过，也是cli的

## .http 文件

JetBrains .http 文件实现，支持 API 测试的 curl 格式化工具。

这个我没用过，没有发言权。
