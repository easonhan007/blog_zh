---
title: "Rails activestorage 使用 cloudflare R2 对象存储"
date: 2024-05-14T11:10:46+08:00
draft: false
---

根据[这篇文章](https://kirillplatonov.com/posts/activestorage-cloudflare-r2/)一步一步来，基本上没啥问题。

核心几个配置在下面。

Use bin/rails `credentials:edit` to set Cloudflare credentials:

```yaml
cloudflare:
  account_id: ACCOUNT_ID
  access_key_id: YOUR_KEY
  secret_access_key: YOUR_SECRET
  bucket: BUCKET_NAME
```

Now update `config/storage.yml`:

```
cloudflare:
    service: S3
    endpoint: https://<%= Rails.application.credentials.dig(:cloudflare, :account_id) %>.r2.cloudflarestorage.com
    access_key_id: <%= Rails.application.credentials.dig(:cloudflare, :access_key_id) %>
    secret_access_key: <%= Rails.application.credentials.dig(:cloudflare, :secret_access_key) %>
    region: auto
    bucket: <%= Rails.application.credentials.dig(:cloudflare, :bucket) %>
```

And update ActiveStorage service in `config/environments/development.rb`:

```
config.active_storage.service = :cloudflare
```
