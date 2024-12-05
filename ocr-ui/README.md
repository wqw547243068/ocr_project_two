# 部署方案
## 方案一
直接开发环境演示
1. 本地需有nodejs > 20.0 版本
2. 在当前orc-web目录下执行 npm install
3. npm run dev
4. 浏览器访问http://localhost:5173

## 方案二
1. 本地需有nodejs > 20.0 版本
2. 在当前orc-web目录下执行 npm install
3. npm run build
4. dist文件夹
5. 通过http-server 部署，需要npm install http-server

```sh
npm install -g http-server
cd dist/

http-server -a 0.0.0.0 -p 9000
# 打开浏览器访问 http://ip:9000 或者http://localhost:9000
```

## 方案三 （直接部署dist包，可通过方案二第5步部署）
1. dist文件夹
2. 通过nginx部署

```sh
# nginx.conf

server {
  listen       8088; #访问端口
  server_name  localhost;

  location / {
    root /home/web/dist; #前端dist包地址
    index  index.html index.htm;
    try_files $uri $uri/ /index.html;

    if ($request_filename ~* .*\.(js|css)$) {
      add_header Cache-Control no-store;
    }
  }

  location /ocrapi/ {
    proxy_set_header x-forwarded-for  $remote_addr;
    proxy_pass http://127.0.0.1:8001/; #后端代理地址，若没有可不配
  }

  charset utf-8;
}

# nginx 服务启动后，打开浏览器访问 https://{nginx-server-ip}:8088
```

## 方案四
1. dist文件夹
2. 任意后台服务器部署静态资源