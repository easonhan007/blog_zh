{"title": "\u7528wiremock\u81ea\u5efamock\u670d\u52a1", "draft": false, "date": "2023-04-07T14:39:24+08:00"}

我们很多时候都需要mock服务，比如

- 在做性能测试的时候，我们希望调用第三方服务的接口可以被mock掉，这样就不会因为压测而对第三方依赖造成巨大的负载
- 第三方服务归属于其他团队，不同环境之间的沟通和协调其实比较麻烦
- 消除不同测试环境之间的差异
- 控制请求的时延
- 如果是使用云服务的话，使用mock接口还可以节约出口的带宽
- 提升第三方服务的稳定性

所以mock的作用就是用最小的代价实现跟第三方接口几乎一样的假的接口，最好返回的内容是动态可配置的，这样我们在测试环境就可以直接去调用这个假接口，从而消除了对第三方的依赖。

实现mock的方式很多，最简单的做法就是随机应变，自行实现，比如在python技术栈里，我们可以用flask去这样实现

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/get-json')
def hello():
    return jsonify(hello='world') # Returns HTTP Response with {"hello": "world"}
```

用go实现起来也不难，下面的例子来自go的官方文档，使用了gin框架。[https://go.dev/doc/tutorial/web-service-gin](https://go.dev/doc/tutorial/web-service-gin)

```go
package main

import (
    "net/http"

    "github.com/gin-gonic/gin"
)

// album represents data about a record album.
type album struct {
    ID     string  `json:"id"`
    Title  string  `json:"title"`
    Artist string  `json:"artist"`
    Price  float64 `json:"price"`
}

// albums slice to seed record album data.
var albums = []album{
    {ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
    {ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
    {ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
}

func main() {
    router := gin.Default()
    router.GET("/albums", getAlbums)
    router.GET("/albums/:id", getAlbumByID)
    router.POST("/albums", postAlbums)

    router.Run("localhost:8080")
}

// getAlbums responds with the list of all albums as JSON.
func getAlbums(c *gin.Context) {
    c.IndentedJSON(http.StatusOK, albums)
}

// postAlbums adds an album from JSON received in the request body.
func postAlbums(c *gin.Context) {
    var newAlbum album

    // Call BindJSON to bind the received JSON to
    // newAlbum.
    if err := c.BindJSON(&newAlbum); err != nil {
        return
    }

    // Add the new album to the slice.
    albums = append(albums, newAlbum)
    c.IndentedJSON(http.StatusCreated, newAlbum)
}

// getAlbumByID locates the album whose ID value matches the id
// parameter sent by the client, then returns that album as a response.
func getAlbumByID(c *gin.Context) {
    id := c.Param("id")

    // Loop through the list of albums, looking for
    // an album whose ID value matches the parameter.
    for _, a := range albums {
        if a.ID == id {
            c.IndentedJSON(http.StatusOK, a)
            return
        }
    }
    c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
}
```

从上面的代码可以看出来，如果不需要实现创建接口的话，代码量还能少三分之一左右，总的来看其实难度也不算大。

对于有兴趣写代码的同学来说，上面两种做法都是值得赞赏的，不过后面的部署和维护问题可能会随着代码量的增加而变得麻烦起来。这时候使用通用的mock服务可能会更简单一些。

### Mock as a Service

这是一种提供mock能力的通用方式，相比于写代码，mock as a service可以提供更加简单灵活的创建mock接口的方式，比如

- 通过ui界面上的表单
- 发送http请求
- 配置文件

我们可以自己实现这样的mock服务，不过这样会有一定的难度，比如

- 平台的形态是什么样的？
- 如果有ui，那么谁来设计，谁来实现？
- 如果这是command line，那么用户会不会从入门到放弃？
- 如何保证灵活性和扩展性？
- 谁来部署和维护？

另外mock平台其实不同企业之间的共性也是很明显的，所以如果市面上有通用解决方案的话，我们直接拿来用也不是不可以。

### wiremock

wiremock就是这样一款工具，项目地址：[https://github.com/wiremock/wiremock](https://github.com/wiremock/wiremock)

其主要的特性有

- 更高级的请求匹配方式
- 动态响应模板
- 可以在单元测试里运行
- 故障注入和时延注入
- 支持录制和回放
- 支持通过java python http 和json文件来定义mock接口

我简单看了一下，比我自己写的话要好很多。

### 安装

建议docker安装。

```bash
docker run -it --rm \
  -p 8080:8080 \
  --name wiremock \
  -v $PWD:/home/wiremock \
  wiremock/wiremock:2.33.1
```

本文写作的时候，wiremock的最新版本是2.33.1。

这里重点解释一下 -v 参数，这里我们把当前文件夹映射到了容器的`/home/wiremock/` 路径下，运行之后当前路径会生成2个新的文件夹，分别是

- `__files`
- `__mappings`

运行之后命令行展示如下，看到这个界面就是服务启动成功了，可以用`ctrl+c`来停止服务

```
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
 /$$      /$$ /$$                     /$$      /$$                     /$$
| $$  /$ | $$|__/                    | $$$    /$$$                    | $$
| $$ /$$$| $$ /$$  /$$$$$$   /$$$$$$ | $$$$  /$$$$  /$$$$$$   /$$$$$$$| $$   /$$
| $$/$$ $$ $$| $$ /$$__  $$ /$$__  $$| $$ $$/$$ $$ /$$__  $$ /$$_____/| $$  /$$/
| $$$$_  $$$$| $$| $$  \__/| $$$$$$$$| $$  $$$| $$| $$  \ $$| $$      | $$$$$$/
| $$$/ \  $$$| $$| $$      | $$_____/| $$\  $ | $$| $$  | $$| $$      | $$_  $$
| $$/   \  $$| $$| $$      |  $$$$$$$| $$ \/  | $$|  $$$$$$/|  $$$$$$$| $$ \  $$
|__/     \__/|__/|__/       \_______/|__/     |__/ \______/  \_______/|__/  \__/

port:                         8080
enable-browser-proxying:      false
disable-banner:               false
no-request-journal:           false
verbose:                      false
```

当然，因为wiremock是使用java实现的，我们也可以用启动jar包的方式来运行，前提是需要安装jdk或者是jre。

```bash
java -jar wiremock-jre8-standalone-2.33.1.jar
```

更多配置项可以参考文档：[https://wiremock.org/docs/running-standalone/](https://wiremock.org/docs/running-standalone/)

### 静态mock一个接口

下面我们来写一个静态的mock接口，静态的意思是接口的返回是写死的，不是动态的。

创建一个名为example.json的文件，内容如下

```json
{
  "request": {
    "method": "GET",
    "url": "/products/1"
  },
  "response": {
    "status": 200,
    "fixedDelayMilliseconds": 1000,
    "jsonBody": {
      "data": [{
        "type": "product",
        "id": "1",
        "attributes": {
          "productName": "Raspberry PI",
          "productDescription": "Best product ever",
          "price": 42,
          "stock": 500
        }
      }]
    }
  }
}
```

把这个文件放到/mappings路径下面，然后重新启动服务，然后浏览器访问或者curl:`http://localhost:8080/products/1`，响应结果如下

```json
{
  "data": [
    {
      "type": "product",
      "id": "1",
      "attributes": {
        "productName": "Raspberry PI",
        "productDescription": "Best product ever",
        "price": 42,
        "stock": 500
      }
    }
  ]
}
```

### 反向代理模式

我们可以使用nginx的反向代理模式来提升wiremock的容量。docker-compose.yml如下

```yaml
version: "2"
services:
  wiremock:
    image: wiremock/wiremock:2.33.1
    volumes:
      - ../mappings:/home/wiremock/mappings:ro
    ports: 
      - 8080
  
  nginx-load-balancer:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - wiremock
    ports:
      - "80:8080"
```

ng的配置如下

```
user  nginx;

events {
    worker_connections   1000;
}

http {
        server {
              listen 8080;
              location / {
                proxy_pass http://wiremock:8080;
              }
        }
}
```

运行：`docker-compose up -d` 

停止: `docker-compose stop`

### 更高的流量要求

如果我们需要部署一个企业级的mock服务，那么ng+wiremock的方式可能达不到一个很高的容量上限，这时候我们可以使用ks8，通过k8s serivce的负载均衡机制，多启动一些wiremock pod来提升系统的整体吞吐量。

### 总结

在时间有限和需求变化相对较快的情况下，wiremock+ng应该是一个不错的通用mock服务解决方案。