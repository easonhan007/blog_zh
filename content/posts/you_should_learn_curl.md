---
title: "人人都要会的工具之--curl"
date: 2024-06-14T09:08:39+08:00
draft: true
---

想象一下，你需要在 CI/CD 流水线中进行一些 API 调用，以进行身份验证、获取数据、发送简单请求或从网络 URI 下载文件。

你会选择哪些工具？

答案可能是使用像 Postman 这样的著名 API 测试工具。

不过一般情况下只需要用 curl 就够了。而且很多年之前 curl 就已经跨平台了，我记得 windows 上也是可以使用的。

所以我认为，写一篇关于 CURL 的文章是值得的。

我将这篇文章的范围缩小到 HTTP/HTTPS，因为写一篇关于 curl 全部功能的文章会花费好几天。你很快就会明白我为什么这么说。

### curl 是做什么的？

Curl，全称为“Client URL”，是一种命令行工具，用于通过 URL 传输数据。curl 还用于汽车、电视机、路由器、打印机、音频设备、手机、平板电脑、医疗设备、机顶盒、电脑游戏、媒体播放器等。

Curl 是超过二百亿个软件应用程序中的互联网传输引擎。

几乎每个使用互联网的人每天都会使用 Curl。

你能想象它支持多少协议吗？

```
DICT、FILE、FTP、FTPS、GOPHER、GOPHERS、HTTP、HTTPS、IMAP、IMAPS、LDAP、LDAPS、MQTT、POP3、POP3S、RTMP、RTMPS、RTSP、SCP、SFTP、SMB、SMBS、SMTP、SMTPS、TELNET、TFTP、WS 和 WSS。curl 支持 TLS 证书、HTTP POST、HTTP PUT、FTP 上传、基于 HTTP 表单的上传、代理（SOCKS4、SOCKS5、HTTP 和 HTTPS）、HTTP/2、HTTP/3、cookie、用户+密码认证（Basic、Plain、Digest、CRAM-MD5、SCRAM-SHA、NTLM、Negotiate、Kerberos、Bearer tokens 和 AWS Sigv4）、文件传输恢复、代理隧道、HSTS、Alt-Svc、unix 域套接字、HTTP 压缩（gzip、brotli 和 zstd）、etags、并行传输、DNS-over-HTTPS，等等。
```

### 为什么选择 Curl？因为它简单、无处不在且灵活！

- **简单易用**：Curl 就像 API 测试的瑞士军刀。它简单、直接，不需要编程博士学位就能使用。只需输入几个命令，按下回车键，瞧，你就像专业人士一样发送或测试 API！
- **随处可用**：无论你是在 Mac、PC 还是 Linux 机器上，Curl 都能为你服务。不需要为不同平台使用不同的工具，Curl 与每个人都相处得很好。

### 让我们开始发送 API 请求吧

首先确保你已经在电脑上安装了 Curl。别担心，这就像下载一个应用程序或使用包管理器一样简单。安装完成后，你就准备好了！

你可以从官方网页下载并安装 Curl，或者使用像 Homebrew（适用于 macOS 和 Linux）或 Chocolatey（适用于 Windows）这样的包管理器。

### 发送你的第一个请求

想象一下你想从一个 API 获取员工列表。使用 Curl 是这样的：

```bash
curl https://dummy.restapiexample.com/api/v1/employees
```

按下回车键，Curl 就会为你获取用户数据。就是这么简单！

### 输出

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "employee_name": "Tiger Nixon",
      "employee_salary": 320800,
      "employee_age": 61,
      "profile_image": ""
    },
    ...
  ],
  "message": "Successfully! All records has been fetched."
}
```

### CURL 选项

在我们开始示例之前，先了解一下 CURL 中一些最有用的选项。这里是一些常用的选项：

1. `-H`，`--header`：允许你在请求中包含自定义 HTTP 头。例如：
   ```bash
   curl -H "Content-Type: application/json" https://api.example.com/resource
   ```
2. `-d`，`--data`：在请求体中发送数据。适用于 POST 和 PUT 请求。例如：
   ```bash
   curl -X POST -d '{"name": "John"}' https://api.example.com/users
   ```
3. `-i`，`--include`：在输出中包含 HTTP 响应头。例如：
   ```bash
   curl -i https://api.example.com/resource
   ```
4. `-o`，`--output`：将响应体写入文件而不是打印到 stdout。例如：
   ```bash
   curl -o response.txt https://api.example.com/resource
   ```
5. `-u`，`--user`：提供 HTTP 基本认证的凭证（用户名:密码）。例如：
   ```bash
   curl -u username:password https://api.example.com/resource
   ```
6. `-F`，`--form`：以 multipart/form-data 请求发送数据。适用于上传文件。例如：
   ```bash
   curl -F "file=@example.txt" https://api.example.com/upload
   ```
7. `-X`，`--request`：指定 HTTP 请求方法（GET、POST、PUT、DELETE 等）。例如：
   ```bash
   curl -X POST https://api.example.com/resource
   ```
8. `-v`，`--verbose`：显示关于请求和响应的详细信息，包括头和状态码。例如：
   ```bash
   curl -v https://api.example.com/resource
   ```

你还可以组合这些选项。你会在下面看到更多的例子。

### CURL CRUD 操作

Curl 支持各种 HTTP 方法，包括 GET、POST、PUT、PATCH 和 DELETE，允许你对 API 资源执行 CRUD（创建、读取、更新、删除）操作。以下是每个 CRUD 操作的 Curl 命令示例：

#### POST（创建）

在下面的示例中，“curl -X POST” 表示 HTTP 请求应该是 POST 请求。你可以根据要发送的请求类型将“POST”替换为其他 HTTP 方法，如 GET、PUT、DELETE 等。

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Chamila","salary":"1000","age":"40"}' https://dummy.restapiexample.com/api/v1/create
```

输出

```json
{
  "status": "success",
  "data": {
    "id": 1960
  },
  "message": "Successfully! Record has been added."
}
```

#### GET（读取）

GET 是默认的 CURL 命令。所以你不需要指定任何选项。

```bash
curl https://dummy.restapiexample.com/api/v1/employee/1
```

输出

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "employee_name": "Tiger Nixon",
    "employee_salary": 320800,
    "employee_age": 61,
    "profile_image": ""
  },
  "message": "Successfully! Record has been fetched."
}
```

#### PUT（更新）

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Chamila A","salary":"2000","age":"40"}' https://dummy.restapiexample.com/public/api/v1/update/2
```

输出

```json
{
  "status": "success",
  "data": [],
  "message": "Successfully! Record has been updated."
}
```

#### DELETE（删除）

```bash
curl -X DELETE https://dummy.restapiexample.com/api/v1/delete/2
```

输出

```json
{
  "status": "success",
  "data": "2",
  "message": "Successfully! Record has been deleted"
}
```

### 高级选项

有时，你需要证明自己的身份或在请求中添加特殊指令。别担心，Curl 也能帮你搞定！

#### 添加认证：

```bash
curl -H "Authorization: Bearer <token>" https://api.example.com/protected/resource
```

#### 自定义头：

```bash
curl -H "X-Custom-Header: Value" https://api.example.com/users
```

Curl 就像变色龙——它可以适应任何情况！

### 处理响应

发送请求后，你会从 API 那里得到响应。Curl 可以帮你理解这一切！

#### 检查响应头：

```bash
curl -i https://dummy.restapiexample.com/api/v1/employee/1
```

输出

```
HTTP/1.1 200 OK
Date: Mon, 13 May 2024 21:58:33 GMT
Server: nginx/1.21.6
Content-Type: application/json
Cache-Control: no-cache, private
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 58
Cache-Control: max-age=86400
Expires: Tue, 14 May

 2024 21:58:33 GMT
Vary: Accept-Encoding
X-Endurance-Cache-Level: 2
X-nginx-cache: WordPress
X-Server-Cache: true
X-Proxy-Cache: MISS
Transfer-Encoding: chunked

{"status":"success","data":{"id":1,"employee_name":"Tiger Nixon","employee_salary":320800,"employee_age":61,"profile_image":""},"message":"Successfully! Record has been fetched."}
```

#### 将响应数据保存到文件：

```bash
curl -o response.json https://dummy.restapiexample.com/api/v1/employee/1
```

#### 格式化 JSON 响应：

你需要安装 jq。你可以使用 brew 或 choco 来安装它。

在 Windows 中

```bash
choco install jq
```

安装完成后，你可以运行

```bash
curl https://dummy.restapiexample.com/api/v1/employee/1 | jq
```

输出

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "employee_name": "Tiger Nixon",
    "employee_salary": 320800,
    "employee_age": 61,
    "profile_image": ""
  },
  "message": "Successfully! Record has been fetched."
}
```

#### 没有 jq 的输出将会是这样的

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "employee_name": "Tiger Nixon",
    "employee_salary": 320800,
    "employee_age": 61,
    "profile_image": ""
  },
  "message": "Successfully! Record has been fetched."
}
```

### 总结

根据之前的经验，使用 ai 工具生成 curl 代码非常容易，而且准确性高。

所以下次你需要测试 API 时，不用担心——只需使用 Curl 就可以了。
