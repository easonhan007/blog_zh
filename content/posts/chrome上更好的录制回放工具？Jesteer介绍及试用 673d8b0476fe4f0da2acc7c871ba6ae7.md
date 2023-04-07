{"title": "chrome\u4e0a\u66f4\u597d\u7684\u5f55\u5236\u56de\u653e\u5de5\u5177\uff1fJesteer\u4ecb\u7ecd\u53ca\u8bd5\u7528", "draft": false, "date": "2023-04-07T14:39:24+08:00"}

之前跟大家分享后chrome上原生的录制回放功能，今天看到了一款最新的的录制回放工具jesteer，于是第一时间来了解和试用一下。

### 主要功能

- 不用写代码，直接可以录制和回放
- 可以录制基本的页面交互
- 自动创建基于Puppeteer的脚本
- 回放时的快照检查功能
- 简单舒适的web ui

### 安装

jesteer是一款chrome插件，直接去chrome商店里所有jesteer点击安装既可。

### 界面

jesterr的界面很简单，就3个按钮

- Record：开始录制
- Take a snapshot：dom高亮
- Copy to clipboard

### 简单上手使用

- 点击Record开始录制
- 录制过程中点击Take a snapshot进行断言
- 点击Stop Recording停止录制
- 点击Copy to clipboard拷贝生成的代码到剪切板

这几步还是非常简单的，后来我遇到了一个问题，怎么进行用例的回放呢？之前chrome自带的Recorder是可以录制完成后直接回放的，而jesteer则找不到回放按钮。折腾一小会后我终于找到了答案。

### 把生成的代码粘贴到测试项目中

为了可以运行生成的代码，我决定新建一个nodejs项目来进行尝试。

```jsx
mkdir jesteer_example
cd jesteer_example
npm init
npm install --save-dev jest
npm install --save-dev puppteer
touch example.test.js

```

修改package.json

```jsx
{
  "scripts": {
    "test": "jest"
  }
}
```

我打开一个空白页，然后输入www.itest.info，跳转到搜索页面后，添加一个snapshot断言，最后结束录制。下面是录制出来的脚本。

```jsx
/* 
This test suite was created using JESTEER, a project developed by 
Tim Ruszala, Katie Janzen, Clare Cerullo, and Charissa Ramirez.

Learn more at https://github.com/oslabs-beta/Jesteer .
*/
const puppeteer = require('puppeteer'); // v13.0.0 or later

jest.setTimeout(10000);
describe('', () => {

let browser, page, timeout;

beforeAll(async () => {
browser = await puppeteer.launch({
headless: true,
});
});

beforeEach(async () => {
page = await browser.newPage();
timeout = 5000;
page.setDefaultTimeout(timeout);
});

afterEach(async () => {
await page.close();
});

afterAll(async () => {
await browser.close();
});

it('', async () => {

{
const promises = [];
promises.push(page.waitForNavigation());
await page.goto('chrome://newtab/');
await Promise.all(promises);
}

await page.waitForNavigation();

await page.keyboard.type('itest.info');

await page.keyboard.press('Enter');

{
const element = await page.waitForSelector('#su');
await element.click();
}

{
const element = await page.waitForSelector('HTML > BODY:nth-child(2)');
await element.click();
}

await page.waitForNavigation();

{
const snapped = await page.$eval('#1 > DIV:nth-child(1) > DIV:nth-child(1) > H3:nth-child(1) > A:nth-child(1)', el => el.innerHTML);
expect(snapped).toMatchSnapshot();
}

});

});
```

使用npm run test命令来运行，不出意外运行失败。

```jsx
FAIL  ./sum.test.js
    ✕  (297 ms)

  ●  ›

    net::ERR_INVALID_URL at chrome://newtab/

      37 | const promises = [];
      38 | promises.push(page.waitForNavigation());
    > 39 | await page.goto('chrome://newtab/');
         | ^
      40 | await Promise.all(promises);
      41 | }
      42 |

      at navigate (node_modules/puppeteer/src/common/FrameManager.ts:226:13)
      at FrameManager.navigateFrame (node_modules/puppeteer/src/common/FrameManager.ts:198:17)
      at Frame.goto (node_modules/puppeteer/src/common/FrameManager.ts:792:12)
      at Page.goto (node_modules/puppeteer/src/common/Page.ts:1781:12)
      at Object.<anonymous> (sum.test.js:39:1)
```

查了一下代码，应该是打开chrome的新tab页面之后自动等待的代码报错导致。

### 初步结论

初步结论现在应该有了，jesteer录制出来的代码其实没办法自动识别上下文，也就是说如果在地址栏上输入url并按回车键打开一个新页面，我们期望的结果是直接录制成goto url，但是jesteer只能忠实的还原我们的操作，而这些操作有可能导致回放失败。

### 总结

先说优点

- jesteer作为一款纯录制工具，其提供的snapshot比对功能还是非常强大的，等于是支持了在录制时候直接录制断言的能力；
- jesteer可以录制用户的一系列简单交互，对于一些页面来说还是很管用的；
- 根据jesteer的文档描述，jesteer比chrome原生的recorder录制准确性更高；
- jesteer录制出的脚本集成了jest框架，等于可以直接录制用例，而不是一系列的操作，省去了把脚本加工成用例的过程；

再说不足

- jesteer需要用户对nodejs有一定的了解，不能直接录制完就一键回放；
- jesteer录制出的脚本需要进行一些加工，比如上文可以感知到的修改goto的语句的工作；
- jesteer帮助文档比较简单，想上手用起来需要发挥一点点的想象力

### 最后

对于一些简单的操作和场景，且不介意使用jest作为测试框架的话，jesteer还是比较推荐的，可以极大的提升生产力；其他情况下就不推荐了。