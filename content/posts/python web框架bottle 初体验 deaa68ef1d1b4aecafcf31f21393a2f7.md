{"title": "python web\u6846\u67b6bottle \u521d\u4f53\u9a8c", "draft": false, "date": "2023-04-07T14:39:24+08:00"}

### 功能

拉取金山词霸每日一句的内容存到redis里，用bottle实现简单的路由去回显内容

### 安装

```go
pip install bottle

Installing collected packages: bottle
Successfully installed bottle-0.12.21
```

### 获取内容

api接口的响应如下，通过日期就可以拿到每日一句的具体内容了

```json
{
	errno: 0,
	errmsg: "success",
	sid: 4543,
	title: "2022-07-04",
	content: "The darker the sky, the brighter the stars. ",
	note: "天空越黑，星星越亮。",
	translation: "新版每日一句",
	picture: "https://staticedu-wps.cache.iciba.com/image/cae3e193caf289efe5d33bf63a37ad4b.jpg",
	picture2: "https://staticedu-wps.cache.iciba.com/image/6286d34c787320416bc8d7083e6f6553.jpg",
	picture3: "https://staticedu-wps.cache.iciba.com/image/8d56d2093875904a2483203784d600b6.jpg",
	caption: "词霸每日一句",
	tts: "https://staticedu-wps.cache.iciba.com/audio/ba16eadbfc36a3640409665c50ae996c.mp3",
	tts_size: "",
	s_pv: 5564,
	sp_pv: 0,
	love: 7,
	s_content: "",
	s_link: "",
	period: 0,
	loveFlag: 0,
	tags: "",
	keep: 0,
	comment_count: 640,
	last_title: "2022-07-03",
	next_title: 0,
}
```

具体代码如下

```python
URL = 'https://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title=2022-07-04'

def set_quotes():
	r = redis.Redis(host='localhost', port=6379, db=0)
	obj = requests.get(URL).json()
	r.set(obj['title'], obj['content'])
```

### 第一个路由

创建文件get_quote_v1.py文件，内容如下

```python
import redis
from bottle import route, run, debug, template

@route('/quote')
def get_quote():
	key = '2022-07-04'
	r = redis.Redis(host='localhost', port=6379, db=0)
	content = r.get(key)
	return template('quote_v1', quote=content)
```

这里通过redis拿到了7月4日的每日一句内容，然后渲染了`quote_v1`这个模板

### 第一个模板

在当前文件夹下创建`quote_v1.tpl`文件，内容如下

```html
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
<div class="w-1/2 mx-auto">
  <h1 class="text-2xl font-bold my-64 text-center">
	{{quote}}
  </h1>
</div>
</body>
</html>
```

### 最终效果

![Untitled](python%20web%E6%A1%86%E6%9E%B6bottle%20%E5%88%9D%E4%BD%93%E9%AA%8C%20deaa68ef1d1b4aecafcf31f21393a2f7/Untitled.png)

### 世界应该更丰富多彩一些

我们可以看到接口里返回了中文，英文以及配图信息，那3个picture字段就是。能不能实现个每日一句的卡片，主背景是配图，文字浮在图片上？

答案是肯定的。具体实现方式是我们可以把响应内容直接存在redis的string里，key就是每天的日期，value是响应返回的json字符串。取数据的时候只要把json字符串拿到然后转成python的字典就好了。

### 具体实现

```python
@route('/quote_v2')
def get_quote():
	key = '2022-07-04'
	r = redis.Redis(host='localhost', port=6379, db=0)
	json_str = r.get(key)
	quote_obj = json.loads(json_str)
	return template('quote_v2', en=quote_obj['content'], cn=quote_obj['note'], img=quote_obj['picture2'])

debug(True)
run(reloader=True)
```

路由处理的代码跟之前差不多，只是把http响应里的json字段缓存了一下。

模板代码

```html
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
<div class="container mx-auto my-20">
<div class="max-w-sm bg-white rounded-lg border border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700 mx-auto">
    <a href="#">
        <img class="rounded-t-lg" src="{{img}}" alt="" />
    </a>
    <div class="p-5">
        <a href="#">
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{{en}}</h5>
        </a>
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">{{cn}}</p>
    </div>
</div>
</div>
</body>
</html>
```

改变了一下样式，显示了更多的内容。

### 最终效果

![Untitled](python%20web%E6%A1%86%E6%9E%B6bottle%20%E5%88%9D%E4%BD%93%E9%AA%8C%20deaa68ef1d1b4aecafcf31f21393a2f7/Untitled%201.png)

### 总结

bottle体验下来感觉跟flask差不多，有时间的同学可以拿来玩玩。

优点

- 使用简单
- 配置简单
- 文档详细
- 模板简单

缺点

- 模板tpl格式的编辑器支持不好，目前找不到好的高亮显示方式
- 支持wsgi，然而找不到一个完整的例子，只能自己捣鼓