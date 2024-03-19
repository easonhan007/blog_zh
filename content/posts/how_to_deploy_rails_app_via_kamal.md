---
title: "如何使用kamal部署rails项目"
date: 2024-03-19T20:18:54+08:00
draft: false
---

之前一直搞不定 https，今天看了一眼发现是自己配置错了，顺手记录一下，反正 [kamal](https://kamal-deploy.org/) 每次部署都是常用常新，因为 kamal 深度绑定了 [traefik](https://traefik.io/traefik/)，所以两种配置混在一起，理解起来有一点难度，所以过段时间再去配置，就会有点陌生感。

### 最重要的一点，更新 credentials

因为 kamal 的`.env`文件里需要有 master key 和 secert key，前者需要用来解密 credentials，后者保存在 credentials 里面，所以先直接生成一个，防止 docker build 的时候出错。

```
rm config/credentials.yml.enc
EDITOR="code --wait" bin/rails credentials:edit
```

### 确保项目在本地可以 build 成功

用`docker build . -t xxxx` 去测试一下。

### 安装 kamal

感觉不需要用 bundle 装，直接全局装最省事。

```
gem install kamal
kamal version
```

### 初始化项目

```
kamal init
```

这条命令会生成 2 个文件

- `.env`: rails7.0x 里面.gitignore 文件里没有加这个，**一定要手动加进去，不要提交到代码库**
- `config/deploy.yml`： 核心配置文件

### 修改 deploy.yml 文件

```
# Name of your application. Used to uniquely configure containers.
service: up-to-date

# Name of the container image.
image: my-user-name/up-to-date

# Deploy to these servers.
servers:
  web: # Use a named role, so it can be used as entrypoint by Traefik
    hosts:
      - my-server-ip
    labels:
      traefik.http.routers.up-to-date-web.entrypoints: websecure
      traefik.http.routers.up-to-date-web.rule: Host(`up.ethanhan.cc`)
      traefik.http.routers.up-to-date-web.tls.certresolver: letsencrypt
      traefik.http.routers.up-to-date-web.tls: true

# Credentials for your image host.
registry:
  # Specify the registry server, if you're not using Docker Hub
  # server: registry.digitalocean.com / ghcr.io / ...
  username: my-user-name

  # Always use an access token rather than real password when possible.
  password:
    - KAMAL_REGISTRY_PASSWORD
env:
  clear:
    RUBY_YJIT_ENABLE: 1
    RAILS_SERVE_STATIC_FILES: true
  secret:
    - RAILS_MASTER_KEY
volumes:
  - "/root/up_to_date/storage:/rails/storage" #
# Use a different ssh user than root
ssh:
  user: root
traefik:
  options:
    publish:
      - "443:443"
    volume:
      - "/letsencrypt/acme.json:/letsencrypt/acme.json" # To save the configuration file.
  args:
    entryPoints.web.address: ":80"
    entryPoints.websecure.address: ":443"
    entrypoints.websecure.http.tls: true
    entryPoints.web.http.redirections.entryPoint.to: websecure # We want to force https
    entryPoints.web.http.redirections.entryPoint.scheme: https
    entryPoints.web.http.redirections.entrypoint.permanent: true
    certificatesResolvers.letsencrypt.acme.email: "me@ethanhan.cc"
    certificatesResolvers.letsencrypt.acme.storage: "/letsencrypt/acme.json" # Must match the path in `volume`
    certificatesResolvers.letsencrypt.acme.httpchallenge: true
    certificatesResolvers.letsencrypt.acme.httpchallenge.entrypoint: web # Must match the role in `servers`

builder:
  local:
    arch: amd64

```

下面要配置 ssl 证书的存储，非常重要 🚀。

```
$ mkdir -p /letsencrypt &&
  touch /letsencrypt/acme.json &&
  chmod 600 /letsencrypt/acme.json
```

基本上照搬上面的配置就好了，应该直接可以实现自动 https 和证书续期的功能。

### 配置远程环境

```
kamal setup
```

[官方文档](https://kamal-deploy.org/docs/installation)解释了这步的作用。

> This will:

    Connect to the servers over SSH (using root by default, authenticated by your ssh key)
    Install Docker and curl on any server that might be missing it (using apt-get): root access is needed via ssh for this.
    Log into the registry both locally and remotely
    Build the image using the standard Dockerfile in the root of the application.
    Push the image to the registry.
    Pull the image from the registry onto the servers.
    Push the ENV variables from .env onto the servers.
    Ensure Traefik is running and accepting traffic on port 80.
    Ensure your app responds with 200 OK to GET /up (you must have curl installed inside your app image!).
    Start a new container with the version of the app that matches the current git version hash.
    Stop the old container running the previous version of the app.
    Prune unused images and stopped containers to ensure servers don’t fill up.

### 重启 traefik

```
kamal traefik reboot
```

这才是真正重新读取配置文件然后重启。🚗 不要用`kamal traefic restart`

重启之后看日志里的报错。

```
kamal traefik logs | grep error
```

一般来说没有严重的报错就可以了。

### 总结

目前还没搞明白怎么在 traefik 里配置多个 subdomain 的操作，所以上面的配置不能算是完整体。有[一篇文章](https://www.luizkowalski.net/traefik-with-kamal-tips-and-tricks/)提到过配置方法，有空需要研究一下。
