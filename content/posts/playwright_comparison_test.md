---
title: "每个项目都能用上吧:使用Playwright进行图片比较测试"
date: 2024-03-16T16:42:27+08:00
draft: false
---

Playwright 做为新一代的浏览器 ui 自动化测试工具，有很多有意思的功能，其中截图对比就是其中一个。

本质上讲 playwright 的图片对比测试其实就是**基准测试**，其流程大致如下：

- 先运行一遍测试用例，把代码里定义的需要截图的地方都截图，这些截图就是以后测试的**基准**了，后面所有的比较都是针对于这次截图进行的
- 第一遍运行测试用例时候用例会报错，因为之前没有任何截图，不过没关系，再运行一次就可以了
- 任何时候都可以再次运行用例，此时会拿本次运行时的截图跟第一次保存的截图做像素级的比较，一旦像素有差异用例就会失败，否则用例通过

下面简单介绍一下如何从零开始使用 playwright 进行截图对比测试。

### 安装 playwright

安装 playwright 之前，大家需要安装 nodejs，这一步可以自行搜索。

这里推荐大家使用[Typescript](https://www.typescriptlang.org/)进行代码的编写。主要是因为在入门阶段我们基本上不会接触到复杂的 typescript 语法结构，难度其实跟写 javascript 差不多，心智上的压力其实不算大。最重要的一点是，使用 typescript+vscode+playwright 这套微软组合（三者都是微软出品的），可以在编辑器里非常容易的得到稳定的代码提示，毕竟 ts 可以算得上是静态语言，对于初学者来说代码提示有时候是非常重要的。

因为国内的网络问题，整个安装过程需要用到[淘宝 npm 源](npm.taobao.org)。

打开**命令行**，敲入下面的命令。不知道怎么使用命令行的同学可以自行搜索弄清楚命令行是怎么回事。

```
npm install -D @playwright/test  --registry=https://registry.npmmirror.com
npm install -D typescript  --registry=https://registry.npmmirror.com
npx playwright install

mkdir -p tests
touch tests/itest.info.spec.ts
```

第 1 行是安装 playwright 及测试套件；第 2 行是安装 typescript，第 3 行是安装 playwright 需要调用的浏览器。最后两行则创建了 tests 文件夹并创建了名为`itest.info.spec.ts`的文件。

### 第一个用例

在`itest.info.spec.ts`中输入下面的内容。

```typescript
import { test, expect } from "@playwright/test";

test("Itest.info homepage", async ({ page }) => {
  await page.goto("http://www.itest.info");
  await expect(page).toHaveScreenshot();
});
```

上面代码的意思是跳转到重定向学院的首页www.itest.info，然后截图，如果截图跟之前保存的像素级别一致，那么用例通过，否则用例失败。

在命令行里用下面的命令运行用例。

```
npx playwright test
```

第一次运行时大概率会报下名的错误`Error: A snapshot doesn't exist at .......png, writing actual.` ，这是正常的，因为之前确实没有保存基准的截图，所以这次运行之后 playwright 会自动把这次运行时的截图保存下来作为基准，再运行一次上面的命令不出意外的话用例就会通过了，这时候命令行的输出大致如下。

```
Running 1 test using 1 worker

  ✓  1 tests/itest.info.spec.ts:3:5 › Itest.info homepage (1.7s)

  1 passed (2.2s)
```

### 更多运行方式

playwright 默认运行用例的时候浏览器默认是运行在 headless 模式下的，也就是说我们看不到浏览器在做什么，在调试的时候这是很不友好的。不过 playwright 提供了多种运行方式，非常好用。

**展示 html 报告**

```
npx playwright test --reporter html
```

运行结束后 playwright 会自动展示 html 格式的测试报告，其中可以看到每一步的运行时缩略图，非常好用，推荐默认就这样运行。

**非 headless 模式运行**

这种运行方式可以保持浏览器开启，并且会打开 playwright 自带的运行时 ui，调试起来非常方便。

```
npx playwright test --ui
```

### 更新基准截图

很好理解，每次增加用例或者重构用例之后我们都希望可以更新基准截图,用下面的命令。

```
npx playwright test -u
# or
npx playwright test --update-snapshots
```

### 截图整个页面

默认情况下 playwright 不会截整个页面，只会默认分辨率大小的一屏，有时候我们却希望可以截图整个屏幕，这时候可以用下面的方式。

```typescript
test("Itest.info course page", async ({ page }) => {
  await page.goto("http://www.itest.info");
  await page.getByRole("link").filter({ hasText: "课程" }).click();
  await expect(page).toHaveScreenshot({ fullPage: true });
});
```

### 只截图某个元素

如果我们在测试一个电商网站，那么产品页面最重要的元素是什么？个人观点是加入购物车按钮或者是购买按钮。这时候只截图页面上的核心部分就显得非常重要了。如果我们能只截图加购按钮，那么我们可以实现在任意商品详情页上验证加入购物车功能是否失效的能力。

下面的代码演示了只截图重定向学院主页上**查看订阅计划**按钮的用例。

```typescript
test("Itest.info subscribe button", async ({ page }) => {
  await page.goto("http://www.itest.info");
  const btn = page.getByRole("link").filter({ hasText: "查看订阅计划" });
  await expect(btn).toHaveScreenshot();
});
```

### 只截图某个区域

我们也可以指定只截图某个区域，示例代码如下

```typescript
await expect(page).toHaveScreenshot({
  // square at the center of the page
  clip: {
    x: (width - 400) / 2,
    y: (height - 400) / 2,
    width: 400,
    height: 400,
  },
});
```

### 截图时隐藏某些特定的元素

有时候我们希望测试截图里不要包含页面上的一些敏感信息，比如用户名，用户资产之类的，这时候就需要在截图时去除掉这部分了，playwright 提供的 mask 功能正好可以满足我们的需求。示例代码如下：

```typescript
test("with mask", async ({ page }) => {
  await page.goto("http://www.itest.info");
  await expect(page).toHaveScreenshot({
    mask: [page.getByAltText("Placeholder Image")],
  });
});
```

在上面的代码里，我把页面上所有的图片都给 mask 掉了，大家看截图的时候就会发现被 mask 的区域被玫红色的方块所代替了。

### 总结

playwright 的截图对比功能非常完善，基本上是只有要前端页面的项目都可以用起来，这里的核心思路是尽量选择**不变**的功能或者 ui 进行测试，当然了也可以导入固定的数据来获得同样的效果。这里我总结了一些截图比较的使用场景供大家参考。

- 尽量选择页面上具体的并且是**不变**的的元素或者区域进行截图比较，像我上面举例用的商品详情页的**加入购物车**按钮等；
- 如果在测试环境使用，建议每次运行用例前都**导入一套固定的数据**，这样断言基本上可以无脑写；
- 使用 mask 或者是引入自定义 css（playwright 支持，我没有举例）的时候屏蔽页面上动态变化的部分；

### 思考题

- playwright 默认的截图路径是哪里？
- 是否可以自定义 playwright 的默认截图路径？具体如何配置？
- 是否可以自定义截图的文件名？
- 默认配置下只要截图和基准截图的像素不一致 playwright 就会认为用例不通过，是否可以自定义截图比较的宽容度？
