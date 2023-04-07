{"title": "\u653e\u5f03postman\uff1f\u4e00\u4e2a\u67084k star\uff1f\u63a5\u53e3\u6d4b\u8bd5\u5de5\u5177hoppscotch\u8bc4\u6d4b", "draft": false, "date": "2023-04-07T14:39:24+08:00"}

天下苦postman久矣！

记得当初potman刚横空出世时，其形态只是一个浏览器扩展而已，尽管功能简单，不过却带来了另一个非常大的优势，那就是软件体积非常小，安装到浏览器上以后可以借助于浏览器同步的功能，实现各种跨平台支持，特别是对我我这种拥有win/mac/iinux的人来说，方便快捷是第一位的。

后来postman推出了独立的桌面版本，功能逐渐迭代，性能差的慢慢变态，现在劝退我的是两点：启动速度慢和我用不到的功能慢慢变多；当然除了这两点外还有个相当大的槽点是：postman会想方设法让你登录，如果你不小心使用了同步功能的话，你的测试文件会公开分享到postman上供人品评，这是一个巨大的安全隐患。

D轮融了2.25亿美金，postman注定要在商业化的道路上越走越远，注定会增加很多我不需要的功能，各种同步，花式协作，满屏的效率提升，不厌其烦的提示我升级等等，对我来说其实需求很简单，只要可以让我朴素的调试接口就可以了。

于是各种postman的替代工具应运而生，比如postwoman，insomnia等等，这种工具的技术栈都差不多，都是用js开发的类似于原生客户端的跨平台工具，今天给大家带来的是一款很火的开源postman替代工具: hoppscotch，这个工具在github上目前有40,000的star，3月份新增4000的star，应该是目前最火的测试工具了。

### 安装

hoppscotch只需要安装一个浏览器扩展就可以了，支持chrome和firefox。比postman动则上百兆的安装包来说，安装过程简单了不少。

安装好扩展之后访问[https://hoppscotch.io/](https://hoppscotch.io/)就可以使用了。

### UI

hoppscotch的界面跟postman差不多，会用postman的同学应该会感到比较亲切。

### 功能

功能上hoppscotch也跟postman不相上下

- 支持rest api调试
- 支持GraphQL语法
- 支持websocket和socket.io
- 支持从collection生成文档，这个我不会用
- 支持collection的创建及导出
- 支持多种Authorization方式
- 支持pre-request script
- 支持断言，跟postman的写法不能说很像，只能说是一摸一样
- 完善的快捷键支持
- 支持pwa，轻量化的网页解决方案，让网页应用的体验跟desktop一样，再也不用忍受postman的龟速启动了
- 支持proxy，支持自建proxy
- 个性化定制：白天模式和暗夜模式，各种颜色主题，可以调整字体大小
- 支持cli，这个真是没想到，看了一眼是go写的，功能有限，不过可以在命令行运行collection了，不过似乎不支持websocket
- 完全开源，前端应该是vue写的，有开发能力的同学可以进行定制

### 部署

我们可以在远程服务器上部署个hoppscotch版本，然后远程进行访问。不过用docker部署的话似乎有点问题，就是浏览器插件无法识别的问题，于是就需要部署个proxy用来转发请求，这样就会出现本地localhost无法解析的问题，所以如果不是必须的话，用pwa的版本体验上就已经很好了。

### 总结

总的来说hoppscotch是可以替代postman的，这里推荐大家去试一试。另外hoppscotch也可以登录上传workspace，我也试过也不想试，还是那句话，能不登录就不登录，如果遇到需要协作进行collecton的场景，可以试着用git去管理。