{"title": "Chrome\u2019s Headless mode gets an upgrade", "draft": false, "date": "2023-04-07T14:39:24+08:00"}

Chrome’s Headless mode just got a whole lot better!

Chrome’s Headless mode just got a whole lot better! This article presents an overview of recent engineering efforts to make Headless more useful for developers by bringing Headless closer to Chrome’s regular “headful” mode.

## [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#background)Background

[Back in 2017](https://developer.chrome.com/blog/headless-chrome/), Chrome 59 introduced the so-called Headless mode, which lets you run the browser in an unattended environment without any visible UI. Essentially, running Chrome without chrome!

Headless mode is a popular choice for browser automation through projects like [Puppeteer](https://developer.chrome.com/docs/puppeteer/) or [ChromeDriver](https://chromedriver.chromium.org/). Here’s a minimal command-line example of using Headless mode to create a PDF file of a given URL:

```
chrome --headless --print-to-pdf https://developer.chrome.com/
```

## [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#whats-new-in-headless)What’s new in Headless?

Before we dive into the recent Headless improvements, it’s important to understand how the “old” Headless worked. The command-line snippet we showed earlier uses the `--headless` command-line flag, suggesting that Headless is just a mode of operation of the regular Chrome browser. Perhaps surprisingly, this wasn’t actually true. Technically, **the old Headless was [a separate, alternate browser implementation](https://source.chromium.org/chromium/chromium/src/+/main:headless/;drc=c67febd82ae3e18ac8db1397f4ccfa87b0da2ffc)** that happened to be shipped as part of the same Chrome binary. It doesn’t share any of the Chrome browser code in `[//chrome](https://source.chromium.org/chromium/chromium/src/+/main:chrome/)`.

As you might imagine, implementing and maintaining this separate Headless browser came with a lot of engineering overhead — but that wasn’t the only problem. Because Headless was a separate implementation, it had its own bugs and features that weren’t present in headful Chrome. This created a confusing situation where any automated browser test might pass in headful mode but fail in Headless mode, or vice versa — a major pain point for automation engineers. It also excluded any automated testing that relied on having a browser extension installed, for example. The same goes for any other browser-level functionality: unless Headless had its own, separate implementation of it, it wasn’t supported.

In 2021, the Chrome team set out to solve this problem, and unify Headless and headful modes once and for all.

We’re excited to announce that the new Headless mode is now available in Chrome 112! In this mode, Chrome creates but doesn’t display any platform windows. All other functionality, existing and future, is available with no limitations.

## Try out the new Headless

To try the new Headless mode, pass the `--headless=new` command-line flag:

```
chrome --headless=new
```

For now, the old Headless mode is still available via:

```
chrome --headless=old
```

Currently, passing the `--headless` command-line flag without an explicit value still activates the old Headless mode — but we plan to change this default to new Headless over time.

We plan to completely remove the old Headless from the Chrome binary and stop supporting this mode in Puppeteer later this year. As part of this removal, we’ll make the old Headless available as a separate standalone binary for those users who can’t upgrade yet.

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#new-headless-in-puppeteer)New Headless in Puppeteer

To opt in to the new Headless mode in Puppeteer:

```
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: 'new',
  // `headless: true` (default) enables old Headless;
  // `headless: 'new'` enables new Headless;
  // `headless: false` enables “headful” mode.
});

const page = await browser.newPage();
await page.goto('https://developer.chrome.com/');

// …

await browser.close();
```

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#new-headless-in-selenium-webdriver)New Headless in Selenium-WebDriver

To use the new Headless mode in Selenium-WebDriver:

```
const driver = await env
  .builder()
  .setChromeOptions(options.addArguments('--headless=new'))
  .build();

await driver.get('https://developer.chrome.com/');

// …

await driver.quit();
```

See [the Selenium team’s blog post](https://www.selenium.dev/blog/2023/headless-is-going-away/#what-are-the-two-headless-modes) for more information, including examples using other language bindings.

### Headless-specific command-line flags

The following command-line flags are available for the new Headless mode.

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#-dump-dom)`-dump-dom`

The `--dump-dom` flag prints the serialized DOM of the target page to stdout. Here’s an example:

```
chrome --headless=new --dump-dom https://developer.chrome.com/
```

Note that this is different from simply printing the HTML source code (which you might do with `curl`). To bring you the output of `--dump-dom`, Chrome first parses the HTML code into a DOM, executes any `<script>` that might alter the DOM, and then turns that DOM back into a serialized string of HTML.

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#-screenshot)`-screenshot`

The `--screenshot` flag takes a screenshot of the target page and saves it as `screenshot.png` in the current working directory. It’s especially useful in combination with the `--window-size` flag. Here’s an example:

```
chrome --headless=new --screenshot --window-size=412,892 https://developer.chrome.com/
```

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#-print-to-pdf)`-print-to-pdf`

The `--print-to-pdf` flag saves the target page as a PDF named `output.pdf` in the current working directory. Here’s an example:

```
chrome --headless=new --print-to-pdf https://developer.chrome.com/
```

Optionally, you can add the `--no-pdf-header-footer` flag to omit the print header (with the current date and time) and footer (with the URL and the page number).

```
chrome --headless=new --print-to-pdf --no-pdf-header-footer https://developer.chrome.com/
```

The functionality behind the `--no-pdf-header-footer` flag was previously available via the `--print-to-pdf-no-header` flag. Depending on which Chrome version you’re using, you might need to fall back to the old flag name.

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#-timeout)`-timeout`

The `--timeout` flag specifies the delay in milliseconds after which the page’s content is captured by `--dump-dom`, `--screenshot`, and `--print-to-pdf`. When neither `--timeout` nor `--virtual-time-budget` (see below) are specified, the page content is captured as soon as the page is loaded.

To illustrate its use, consider [this demo page which increments, logs, and displays a counter every second](https://mathiasbynens.be/demo/time) using `setTimeout(fn, 1000)`. Here’s the relevant code:

```
<output>0</output>
<script>
  const element = document.querySelector('output');
  let counter = 0;
  setInterval(() => {
    counter++;
    console.log(counter);
    element.textContent = counter;
  }, 1_000);
</script>
```

After one second, the page contains “1”; after two seconds, “2”, and so on. Here’s how you’d capture the page’s state after 5 seconds and save it as a PDF:

```
chrome --headless=new --print-to-pdf --timeout=5000 https://mathiasbynens.be/demo/time
```

The `--timeout=5000` flag tells Chrome to wait for 5 seconds before printing the PDF. Thus, this process takes at least 5 seconds to run.

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#-virtual-time-budget)`-virtual-time-budget`

The `--virtual-time-budget` enables time travel! Well, to some extent. Virtual Time acts as a “fast-forward” for any time-dependent code (for example, `setTimeout`/`setInterval`). It forces the browser to execute any of the page’s code as fast as possible while making the page believe that the time actually goes by.

- `-virtual-time-budget` is most commonly used as a replacement for `-timeout`, like this:

```
chrome --headless=new --print-to-pdf --virtual-time-budget=5000 https://mathiasbynens.be/demo/time
```

This produces the same result as the previous example with `--timeout`. The difference is that, with `--virtual-time-budget`, the process takes very little real time — just about the same time as if there was no timeout specified at all. The difference becomes more obvious with larger values:

```
chrome --headless=new --print-to-pdf --virtual-time-budget=42000 https://mathiasbynens.be/demo/time
```

With `--timeout=42000`, it would take at least 42 seconds before the PDF gets printed. With `--virtual-time-budget=42000`, it barely takes longer than the previous example.

## Debugging

Because Chrome is effectively invisible in Headless mode, it might sound tricky to figure out what’s going on in case of issues. Luckily, it’s possible to debug Headless Chrome in a way that’s very similar to headful Chrome. The trick is to launch Chrome in Headless mode with the `--remote-debugging-port` command-line flag.

```
chrome --headless=new --remote-debugging-port=0 https://developer.chrome.com/
```

This prints a unique WebSocket URL to stdout, for example:

```
DevTools listening on ws://127.0.0.1:60926/devtools/browser/b4bd6eaa-b7c8-4319-8212-225097472fd9
```

In a regular headful Chrome instance, we can then use [Chrome DevTools remote debugging](https://developer.chrome.com/docs/devtools/remote-debugging/) to connect to the Headless target and inspect it. To do so, go to `chrome://inspect`, click the **Configure…** button, and enter the IP address and port number from the WebSocket URL. In the above example, I entered `127.0.0.1:60926`. Click **Done** and you should see a Remote Target appear with all its tabs and other targets listed below. Click **inspect** and you now have access to Chrome DevTools inspecting the remote Headless target, **including a live view of the page**!

Chrome的无头模式变得更好了！

本文概述了最近的工程努力，将无头模式更加有用地与Chrome的常规“有头”模式联系起来，使其更适合开发人员。

## [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#background) 背景

回到2017年，Chrome 59引入了所谓的无头模式，它允许您在没有任何可见UI的无人值守环境下运行浏览器。本质上是在没有Chrome的情况下运行Chrome！

无头模式是通过项目（如Puppeteer或ChromeDriver）进行浏览器自动化的流行选择。以下是使用无头模式创建给定URL的PDF文件的最小命令行示例：

```
chrome --headless --print-to-pdf <https://developer.chrome.com/>

```

## [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#whats-new-in-headless) 无头模式有什么新功能？

在我们深入了解最近的无头改进之前，了解“旧”无头是如何工作的非常重要。我们之前展示的命令行片段使用了“--headless”命令行标志，这表明无头只是常规Chrome浏览器的操作模式。令人惊讶的是，事实并非如此。从技术上讲，旧的无头是一个单独的、替代的浏览器实现，恰好作为同一Chrome二进制文件的一部分进行了发布。它不共享Chrome浏览器代码中的任何内容。

正如您可能想象的那样，实现和维护这个单独的无头浏览器带来了很多工程开销，但这并不是唯一的问题。由于无头是一个单独的实现，它有自己的错误和功能，在headful Chrome中不存在。这会创建一个令人困惑的情况，任何自动化浏览器测试都可能在headful模式下通过，但在无头模式下失败，反之亦然，这是自动化工程师的主要痛点。例如，它还排除了任何依赖于安装浏览器扩展的自动化测试。任何其他浏览器级别的功能也是如此：除非无头有自己的、单独的实现，否则就不被支持。

2021年，Chrome团队着手解决这个问题，彻底统一无头和headful模式。

我们很高兴地宣布，新的无头模式现在在Chrome 112中可用！在该模式下，Chrome创建但不显示任何平台窗口。所有其他功能，现有和未来的，都可以无限制地使用。

## 尝试新的无头

要尝试新的无头模式，请传递 `--headless=new` 命令行标志：

```
chrome --headless=new

```

目前，旧的无头模式仍可通过以下方式获得：

```
chrome --headless=old

```

目前，传递没有明确值的 `--headless` 命令行标志仍会激活旧的无头模式，但我们计划随着时间的推移将此默认更改为新的无头模式。

我们计划从Chrome二进制文件中完全删除旧的无头，在今年晚些时候停止支持此模式。作为此删除的一部分，我们将使旧的无头模式可用作单独的独立二进制文件，供那些无法升级的用户使用。

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#new-headless-in-puppeteer)  Puppeteer中的新无头模式

要在 Puppeteer 中选择新的无头模式：

```
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: 'new',
  // `headless: true` (default) enables old Headless;
  // `headless: 'new'` enables new Headless;
  // `headless: false` enables “headful” mode.
});

const page = await browser.newPage();
await page.goto('<https://developer.chrome.com/>');

// ...

await browser.close();

```

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#new-headless-in-selenium-webdriver)  Selenium-WebDriver中的新无头模式

要在 Selenium-WebDriver 中使用新的无头模式：

```
const driver = await env
  .builder()
  .setChromeOptions(options.addArguments('--headless=new'))
  .build();

await driver.get('<https://developer.chrome.com/>');

// ...

await driver.quit();

```

请参阅 Selenium 团队的博客文章，以获取更多信息，包括使用其他语言绑定的示例。

### 无头专用命令行标志

以下命令行标志可用于新的无头模式。

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#-dump-dom) `dump-dom`

- `-dump-dom` 标志将目标页面的序列化DOM打印到标准输出。以下是一个示例：

```
chrome --headless=new --dump-dom <https://developer.chrome.com/>

```

请注意，这与仅打印HTML源代码（您可能使用curl）不同。为了为您带来 `--dump-dom` 的输出，Chrome首先将HTML代码解析为DOM，执行可能更改DOM的任何 `<script>`，然后将该DOM转换回HTML的序列化字符串。

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#-screenshot) `screenshot`

- `-screenshot` 标志对目标页面进行截图，并将其保存为当前工作目录中的 `screenshot.png`。它特别适用于与 `-window-size` 标志组合使用。以下是一个示例：

```
chrome --headless=new --screenshot --window-size=412,892 <https://developer.chrome.com/>

```

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#-print-to-pdf) `print-to-pdf`

- `-print-to-pdf` 标志将目标页面保存为名为 `output.pdf` 的PDF文件，保存在当前工作目录中。以下是一个示例：

```
chrome --headless=new --print-to-pdf <https://developer.chrome.com/>

```

可以选择添加 `--no-pdf-header-footer` 标志，以省略打印页眉（带有当前日期和时间）和页脚（带有URL和页码）。

```
chrome --headless=new --print-to-pdf --no-pdf-header-footer <https://developer.chrome.com/>

```

- `-no-pdf-header-footer` 标志背后的功能以前可通过 `-print-to-pdf-no-header` 标志实现。根据您使用的Chrome版本，您可能需要回退到旧的标志名称。

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#-timeout) `timeout`

- `-timeout` 标志指定页面加载后多少毫秒后，页面的内容会被 `-dump-dom`、`-screenshot` 和 `-print-to-pdf` 捕获。当未指定 `-timeout` 或 `-virtual-time-budget`（详见下文）时，页面内容将在页面加载后立即捕获。

为了说明其用法，请考虑使用 `setTimeout(fn, 1000)` 每隔一秒钟自增、记录和显示计数器的 [此演示页面](https://mathiasbynens.be/demo/time)。以下是相关代码：

```
<output>0</output>
<script>
  const element = document.querySelector('output');
  let counter = 0;
  setInterval(() => {
    counter++;
    console.log(counter);
    element.textContent = counter;
  }, 1_000);
</script>

```

一秒钟后，页面包含“1”；两秒后，“2”，依此类推。以下是在 5 秒后捕获页面状态并将其保存为 PDF 的方法：

```
chrome --headless=new --print-to-pdf --timeout=5000 <https://mathiasbynens.be/demo/time>

```

- `-timeout=5000` 标志告诉 Chrome 等待 5 秒钟，然后再打印 PDF。因此，此过程需要至少 5 秒才能运行。

### [#](https://developer.chrome.com/articles/new-headless/?utm_campaign=Software%2BTesting%2BWeekly&utm_medium=web&utm_source=Software_Testing_Weekly_157#-virtual-time-budget) `virtual-time-budget`

- `-virtual-time-budget` 让时间旅行！在某种程度上是这样。虚拟时间作为任何时间依赖性代码（例如 `setTimeout`/`setInterval`）的“快进”操作。它强制浏览器尽可能快地执行页面的任何代码，同时使页面相信时间实际上确实过去了。
- `virtual-time-budget` 最常用作 `timeout` 的替代，如下所示：

```
chrome --headless=new --print-to-pdf --virtual-time-budget=5000 <https://mathiasbynens.be/demo/time>

```

这与前面的 `--timeout` 示例产生相同的结果。不同之处在于，使用 `--virtual-time-budget`，该过程需要非常少的实际时间 - 就像根本没有指定超时一样。使用较大的值时，差异变得更加明显：

```
chrome --headless=new --print-to-pdf --virtual-time-budget=42000 <https://mathiasbynens.be/demo/time>

```

使用 `--timeout=42000`，在打印 PDF 之前至少需要 42 秒。使用 `--virtual-time-budget=42000`，它几乎与上一个示例一样快。

## 调试

因为在无头模式下，Chrome实际上是不可见的，所以在出现问题时找出问题所在可能会比较棘手。幸运的是，可以以与有头Chrome非常相似的方式在无头Chrome中进行调试。诀窍是使用带有 `--remote-debugging-port` 命令行标志在无头模式下启动Chrome。

```
chrome --headless=new --remote-debugging-port=0 <https://developer.chrome.com/>

```

这将在标准输出中打印一个唯一的WebSocket URL，例如：

```
DevTools listening on ws://127.0.0.1:60926/devtools/browser/b4bd6eaa-b7c8-4319-8212-225097472fd9

```

在常规的有头Chrome实例中，我们可以使用 Chrome DevTools 远程调试连接到无头目标并进行检查。为此，请转到 `chrome://inspect`，单击 "Configure..." 按钮，然后输入 WebSocket URL 中的 IP 地址和端口号。在上面的示例中，我输入了 `127.0.0.1:60926`。单击 "完成"，您应该会看到一个远程目