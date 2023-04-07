{"title": "selenium 4 0\u65b0\u7279\u6027\u53ca\u65b0\u65e7api\u5bf9\u6bd4", "draft": false, "date": "2023-04-07T14:39:24+08:00"}

众所周知，java语言版本的selenium一般被认为是最正宗的selenium版本，今天我们以java语言为例，来看看selenium 4.0的各种新特性以及新旧api的对比。

### **Capabilities**

如果你需要对浏览器进行一些全局设置，那么使用Capabilities是唯一的选择。说实话，旧的Capabilities有点不太符合直觉，具体用法如下。

```csharp
DesiredCapabilities capabilities = DesiredCapabilities.chrome();
capabilities.setCapability("platform", "Mac OS X");
capabilities.setCapability("version", "94");
driver = new RemoteWebDriver(capabilities);
```

在新版本中，我们直接设置options就可以了，语义上显得更为自然。

```csharp
ChromeOptions options = new ChromeOptions();
options.setBrowserVersion("94");
options.setPlatformName("Mac OS X");
driver = new ChromeDriver(options);
```

### Waits

在之前的版本里，我们实例化各种wait对象时候需要传入2个参数：time以及type of time，在新版本里我们只需要使用Duration类就可以了。

这是之前的做法

```csharp
driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
driver.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);
driver.manage().timeouts().setScriptTimeout(10, TimeUnit.SECONDS);
```

新的方式

```csharp
driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
driver.manage().timeouts().pageLoadTimeout(Duration.ofMinutes(3));
driver.manage().timeouts().setScriptTimeout(Duration.ofHours(1));
```

当然，现在支持各式各样的Duration了，需要注意的是这里接受的是long型的参数。

```csharp
Duration.ofNanos(long nanos);
Duration.ofMillis(long millis);
Duration.ofSeconds(long seconds);
Duration.ofMinutes(long minutes);
Duration.ofHours(long hours);
Duration.ofDays(long days);
```

当然，我们还可以直接设置浏览器的各种全局等待时间，代码上看观感好了不少。

```csharp
ChromeOptions options = new ChromeOptions();
options.setImplicitWaitTimeout(Duration.ofSeconds(10));
options.setScriptTimeout(Duration.ofSeconds(10));
options.setPageLoadTimeout(Duration.ofSeconds(10));
```

### 相对定位器

一些哲学流派告诉我们，世界是变化的，相对的，没有绝对的静，也没有绝对的动，物体总是相对着其他物体进行着运动。

在之前的selenium版本里，我们大部分情况下只能通过绝对定位器来定位元素，比如

- 定位一个id=xxx的元素
- 定位所有class=yyy的元素
- 定位所有的tag那么=zzz的元素

当然，还是有例外的，我们可以通过xpath或者css来不那么绝对的定位元素。比如

- .nav > li：定位class为nav的元素下所有的直接li子元素
- #nav .item：定位id是nav下面所有的class为item的元素

这也是我推荐用css定位的原因，更灵活更简洁，同时可以跟前端的技术栈保持相对统一，xpath的定位能力更强一些，同时也带来了给多的复杂性和学习成本。

在selenium 4.0中，相对定位器终于千呼万唤始出来，我们可以省去相对复杂的xpath表达式，用更加直观的方式来定位元素了，举个例子，下面是一个登录页面。

![Untitled](selenium%204%200%E6%96%B0%E7%89%B9%E6%80%A7%E5%8F%8A%E6%96%B0%E6%97%A7api%E5%AF%B9%E6%AF%94%202805e5a829b74964afe8f263d7bb64ef/Untitled.png)

其html代码如下：

```csharp
<div class="row">
    <div class="large-6 small-12 columns">
        <label for="password">Password</label>
        <input type="password" name="password" id="password">
    </div>
</div>
```

我们试着去定位input之前的那个label，经验丰富的你可以想象到页面上会有非常多label，所以用tagname的方式应该不可取；另外这个label还没有其他更加独特的属性可以利用。不过我们可以发现，睡在他下铺的兄弟input有id属性，定位起来相对简单，很自然的会想到能不能利用input来定位label呢？现在都2021年了，这类的相对定位方式已经被支持了的。

```csharp
WebElement passwordArea = driver.findElement(By.id("password"));
WebElement labelOfPass = driver.findElement(with(By.tagName("label")).above(passwordArea));
System.out.println(labelOfPass.getText());
```

大家可以猜一猜上面代码的输出是什么？

### toLeftOf/toRightOf/near

除了上面所展示的above方式以外，selenium 4.0还支持below，toLeftOf/toRightOf/near等方式，举个简单的例子。

```csharp
<tr>
    <td class="name">itest.info</td>
    <td class="website">itest.info</td>
    <td class="actions">
        <a href="#edit">Edit</a>
        <a href="#delete">Delete</a>
    </td>
</tr>
```

如果我们要定位上面的delete按钮，我们可以用下面的相对定位方式

```java
WebElement website = driver.findElement(By.xpath("(//td[text()='itest.info'])"));
driver.findElement(with(By.linkText("Delete")).toRightOf(website)).click();

// or
driver.findElement(with(By.linkText("Delete")).near(website)).click();
```

### 打开新窗口或者新标签页

在之前的selenium版本中，我们如果要打开新窗口或者是新标签页的话，我们需要先实例化1个driver对象，然后使用window handler来进行下一步的操作；在4.0以后，我们可以直接使用switchTo()方法来打开新窗口。下面是具体的例子：

```java
WebDriver driver = Driver.get();
driver.get("http://www.itest.info/");
        
driver.switchTo().newWindow(WindowType.WINDOW);
driver.get("https://qq.com");
```

打开新标签页也很好办，我们只需要修改WindowType就好了。

```java
WebDriver driver = Driver.get();
driver.get("http://www.itest.info/");
        
driver.switchTo().newWindow(WindowType.TAB);
driver.get("https://qq.com");
```

### **DevTools协议**

在4.0之后我们可以直接使用chrome的开发者工具接口来获取网络情况或者是性能数据了。下面的例子展示了如何使用devtools来设置自己的地理位置，自动化打卡签到有希望了。

```java
WebDriver driver = new ChromeDriver();
DevTools devTools = ((HasDevTools)driver).getDevTools();
devTools.createSession();
devTools.send(Emulation.setGeolocationOverride(Optional.of(38.89511),
                Optional.of(-77.03637),
                Optional.of(1)));
driver.get("https://my-location.org/");
```

### 总结

selenium 4.0并没有带来特别多令人啧啧称奇的特性，不过从api的设计以及语义上，元素的定位上都有了不同程度的优化和提升，这也是selenium成熟的体现。作为1个从selenium rc时代就使用selenium的老用户，对这次大的版本更新我竟然觉得有一丝丝的感动，毕竟是一个开源项目，大家都有自己的工作和生活，能十几年如一日的维护和更新selenium本来就是一件不容易的事情，维护者们为了梦想和情怀还在努力，我们不妨也一起加油吧，学无止境，我独自迈步向前，让举步不前的人自己卷自己吧。