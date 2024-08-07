---
title: "充分发挥 Selenium 4 的潜力"
date: 2024-08-07T12:23:16+08:00
draft: false
---

selenium 4 的新功能，不是非常惊喜，不过确实比较实用了。

在瞬息万变的网络自动化领域,Selenium 一直是主要参与者。随着 Selenium 4 的发布,其功能得到进一步增强,引入了前沿特性,简化了测试流程并提高了效率。Chrome DevTools 和 BiDi API 的集成不仅增强了selenium的技术能力,还为管理自动化项目的经理们带来了战略价值。

## Chrome DevTools 协议:深入浏览器自动化

Selenium 4 与 **Chrome DevTools 协议** (**CDP**) 的集成为自动化测试人员开启了无限可能。通过直接与浏览器底层协议交互,CDP 实现了全面的网络和性能监控、控制台日志访问以及高级调试能力。

想象一下,你需要测试应用在不同网络条件下的表现。利用 CDP,你可以模拟各种网络速度,分析应用如何处理缓慢或不稳定的连接。这一功能确保你的网络应用具有韧性,能够为各种网络条件下的用户提供最佳性能。

**CDP 还支持以下强大功能:**

1. **模拟网络条件**: 模拟离线模式、慢速网络等情况,测试应用的适应能力
2. **访问控制台日志**: 直接捕获和分析控制台日志,便于调试和验证 JavaScript 错误
3. **性能指标**: 收集详细的性能指标,识别瓶颈并优化加载时间
4. **安全测试**: 监控和操作 cookie,追踪混合内容等安全问题,验证 HTTPS 配置

> 启用网络拦截的示例代码:

```java
public class ChromeDevToolsExample {  
    public static void main(String[] args) {  
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        ChromeOptions options = new ChromeOptions();  
        ChromeDriver driver = new ChromeDriver(options);

        DevTools devTools = driver.getDevTools();  
        devTools.createSession();

        // 启用网络  
        devTools.send(Network.enable(Optional.empty(), Optional.empty(), Optional.empty()));

        // 添加网络请求监听器  
        devTools.addListener(Network.requestWillBeSent(), request -> {  
            System.out.println("请求 URL: " + request.getRequest().getUrl());  
        });

        driver.get("https://www.example.com");

        driver.quit();  
    }  
}
```

在这个例子中,我们启用了网络拦截来捕获浏览器发出的所有网络请求。这对于验证是否发出了正确的网络请求以及调试资源加载问题特别有用。

## BiDi API: 实时交互实现敏捷测试

双向 (BiDi) API 引入了客户端和浏览器之间的双向通信渠道,实现了实时交互和更快速的测试自动化。这项功能对于处理异步操作和确保动态、实时更新至关重要。

设想一个场景,你需要验证网页在某个用户操作(如点击按钮或填写表单)后发生的变化。使用 BiDi API,你可以发送命令并立即评估结果,无需等待整个页面重新加载,从而使测试更快、更高效。

**BiDi API 的其他重要特性包括:**

1. **实时 DOM 操作**: 直接实时交互和操作 DOM,支持高级测试场景
2. **异步事件处理**: 异步处理网络请求或 DOM 更新等事件,提高测试可靠性
3. **实时反馈**: 对浏览器操作获得即时反馈,增强测试过程的敏捷性
4. **会话管理**: 更有效地管理浏览器会话,提高对测试环境的控制

> BiDi 实现的示例代码:

```java
public class BiDiExample {  
    public static void main(String[] args) {  
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        ChromeOptions options = new ChromeOptions();  
        ChromeDriver driver = new ChromeDriver(options);

        DevTools devTools = driver.getDevTools();  
        devTools.createSession();

        // 使用 BiDi API 执行 JavaScript 代码 
        Runtime.EvaluateParameters params = new Runtime.EvaluateParameters("document.title");  
        String result = devTools.send(Runtime.evaluate(params)).getResult().getValue().toString();

        System.out.println("页面标题: " + result);

        driver.quit();  
    }  
}
```

在这里,我们使用 BiDi API 评估一个 JavaScript 表达式来获取文档标题。这允许我们在用户操作或事件发生后立即对页面状态进行实时验证。

> 实时 DOM 操作的示例代码:

```java
public class LiveDOMManipulation {  
    public static void main(String[] args) {  
        ChromeOptions options = new ChromeOptions();  
        WebDriver driver = new ChromeDriver(options);  
        DevTools devTools = ((ChromeDriver) driver).getDevTools();  
        devTools.createSession();
        driver.get("https://example.com");

        WebElement element = driver.findElement(By.id("elementId"));

        // 启用 DOM 
        devTools.send(DOM.enable());

        // 获取节点 ID  
        int nodeId = devTools.send(DOM.getDocument()).getRoot().getNodeId();

        // 使用 CDP 设置背景颜色  
        devTools.send(DOM.setAttributeValue(nodeId, "style", "background-color: yellow;"));

        // 向 DOM 添加新元素  
        String script = "let newElement = document.createElement('div'); newElement.innerHTML = 'Hello, World!'; document.body.appendChild(newElement);";  
        ((ChromeDriver) driver).executeScript(script);

        driver.quit();  
    }  
}
```

> 拦截网络请求的代码:

```java
public class NetworkActivity {  
    public static void main(String[] args) {  
        // 设置 ChromeDriver 和 DevTools  
        ChromeOptions options = new ChromeOptions();  
        WebDriver driver = new ChromeDriver(options);  
        DevTools devTools = ((ChromeDriver) driver).getDevTools();  
        devTools.createSession();

        // 启用网络跟踪  
        devTools.send(Network.enable());

        // 添加请求和响应监听器  
        devTools.addListener(Network.requestWillBeSent(), request -> {  
            Request req = request.getRequest();  
            System.out.println("请求 URL: " + req.getUrl());  
            System.out.println("请求方法: " + req.getMethod());  
        });

        devTools.addListener(Network.responseReceived(), response -> {  
            Response res = response.getResponse();  
            System.out.println("响应 URL: " + res.getUrl());  
            System.out.println("响应状态: " + res.getStatus());  
        });

        // 导航到网站  
        driver.get("https://www.example.com");

        // 关闭浏览器  
        driver.quit();  
    }  
}
```

> 获取性能指标

```java
public class PerformanceMetricsOverTime {  
    public static void main(String[] args) {  
        // 设置 ChromeDriver 和 DevTools  
        ChromeOptions options = new ChromeOptions();  
        WebDriver driver = new ChromeDriver(options);  
        DevTools devTools = ((ChromeDriver) driver).getDevTools();  
        devTools.createSession();

        // 启用性能监控  
        devTools.send(Performance.enable());

        // 导航到网站  
        driver.get("https://www.example.com");

        // 定时器每5秒捕获一次性能指标  
        Timer timer = new Timer();  
        timer.schedule(new TimerTask() {  
            @Override  
            public void run() {  
                List<Metric> metrics = devTools.send(Performance.getMetrics());  
                System.out.println("捕获的性能指标:");  
                for (Metric metric : metrics) {  
                    System.out.println(metric.getName() + ": " + metric.getValue());  
                }  
                System.out.println();  
            }  
        }, 0, 5000);  // 初始延迟0毫秒,每5000毫秒(5秒)重复一次

        // 运行测试一段特定时间(例如1分钟)然后停止  
        try {  
            Thread.sleep(60000);  // 运行60秒  
        } catch (InterruptedException e) {  
            e.printStackTrace();  
        }

        // 停止定时器并关闭浏览器  
        timer.cancel();  
        driver.quit();  
    }  
}
```

采用 Selenium 4 的新特性带来了几项战略优势:

1. **提高测试准确性**: 与 Chrome DevTools 的深度集成确保了更精确、更可靠的测试,减少了出错的可能性
2. **改进性能监控**: 管理者现在可以监控详细的性能指标,能够主动识别和解决瓶颈问题
3. **灵活高效的测试环境**：BiDi API 实现了即时反馈和动态交互，打造出反应迅速、适应性强的测试体系。这种环境能够快速响应变化，使测试过程更加敏捷灵活。

## 来源

[原文地址](https://medium.com/@rawataditya231/harnessing-the-capabilities-of-selenium-4-9c294de7ed61)

