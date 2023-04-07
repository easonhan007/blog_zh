{"title": "python requests\u7684\u66ff\u4ee3\u8005\uff1fhttpx\u521d\u4f53\u9a8c", "draft": false, "date": "2023-04-07T14:39:24+08:00"}

python的requests库由于其使用简单，文档丰富成为了很多人在发送http请求时候的优选选择。前几天看到了一个类似的实现httpx，在这里简单使用体验一下，顺便简单分享一下体验心得。

相比较requests，httpx支持sync和async的API，支持http1.1和http2。httpx尽最大努力兼容requests的API，这样一来用户从requests转换到httpx的成本就相对较为低廉了。

### 基本API

```python
>>> import httpx
>>> r = httpx.get('https://www.example.org/')
>>> r
<Response [200 OK]>
>>> r.status_code
200
>>> r.headers['content-type']
'text/html; charset=UTF-8'
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

简单扫一圈，满眼都是requests当年的样子。下面是requests的API，大家来找茬，看看哪里不一样。

```python
>>> import requests
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>> r.status_code
200
>> r.headers['content-type']
'application/json; charset=utf8'
>> r.encoding
'utf-8'
>> r.text
'{"type":"User"...'
>> r.json()
{'private_gists': 419, 'total_private_repos': 77, ...}
```

不能说非常相似，只能说是一模一样。

### httpx client

requests为一组http请求提供了session对象来进行统一设置和管理，httpx则相应的提供了client对象。我们来对比一下使用方式先。

首先使用starlette来创建一个简单的python api服务。starlette项目可以想象成是async版本的flask，跟httpx系出同门。

```python
# example.py
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request):
    await asyncio.sleep(0.1) # 加一点点等待，不加也可以
    return JSONResponse({'hello': 'world'})

routes = [
    Route("/", endpoint=homepage)
]

# app = Starlette(debug=True, routes=routes)
app = Starlette(debug=False, routes=routes)
```

使用uvicorn运行。

```bash
$ uvicorn example:app
```

上面的服务提供了1个接口localhost:8000，返回值如下

```bash
http :8000

HTTP/1.1 200 OK
content-length: 17
content-type: application/json
date: Thu, 11 Aug 2022 07:10:07 GMT
server: uvicorn

{
    "hello": "world"
}
```

我们先用非client/session方式来访问该接口30次，顺便统计一下运行时间

requests先出场。

```python
# without_session
import requests

for i in range(0,30):
	res = requests.get('http://localhost:8000/').json()
	print(res)
```

```bash
python without_session.py  0.24s user 0.08s system 9% cpu 3.500 total
```

上面是不用session的方式，3.5s完成。

使用session试试。

```python
import requests

s = requests.Session()

for i in range(0,30):
	res = s.get('http://localhost:8000/').json()
	print(res)
```

```python
python with_session.py  0.22s user 0.08s system 8% cpu 3.443 total
```

3.44s，快了一点点。

下面是httpx不使用client的方式。

```python
python without_client.py  0.69s user 0.11s system 20% cpu 3.972 total
```

3.9s。

使用client试试

```python
import httpx

with httpx.Client() as client:
	for i in range(0, 30):
		res = client.get('http://localhost:8000/').json()
		print(res)
```

```python
python with_client.py  0.38s user 0.11s system 13% cpu 3.707 total
```

3.7s，也快了一些。

这里可以简单总结一下，使用client/session可以提升一组请求的发送效率，另外也提供了进行统一配置（比如修改header的）的快捷方式。上面的测试由于请求处理的太快效果不是很明显，在日常的测试中两种方式的区别可能会更加容易发现一些。

### async

还是30个请求，这次我们用httpx的async方式来试试。

```python
import asyncio
from asyncio import tasks
import httpx

async def send_requests(client):
	r = await client.get('http://localhost:8000')
	print(r.json())
	return r.json()
		

async def main():
	tasks = []	
	async with httpx.AsyncClient() as client:
		for i in range(0, 30):
			tasks.append(send_requests(client))

		await asyncio.gather(*tasks)
			

asyncio.run(main())
```

```python
python httpx_async.py  0.47s user 0.13s system 71% cpu 0.848 total
```

0.84秒，这大概就是httpx的最终奥义吧。

### 总结

作为下一代的http client，httpx出自名门望族(其开发团队开发了**[django-rest-framework](https://github.com/encode/django-rest-framework)**)，兼容了部分的requests api，支持async操作等，是具有取代requests的能力的，在爬虫场景非常有潜力。