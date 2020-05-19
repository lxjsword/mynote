---
title: docker搭建个人学习环境
date: 2019-11-16 11:38:00
tags: docker
---
### 目标
尽可能使用现有docker镜像, 快速搭建一套个人学习环境, 本地利用vscode remote开发环境, 目前已部署在腾讯云上 https://www.lxjsword.cn

1. 初始化docker网络环境, 搭建子网及网关, 初始化共享盘

2. 搭建nginx, 作为环境的接入层

3. 搭建jupyter, 作为个人学习笔记记录和Python实验

4. 搭建filebrowser, 作为个人云盘

5. 搭建hexo, 写博客

6. 搭建gitbook

### 初始化环境
#### 初始化脚本
``` init.sh
docker network create \
--driver bridge \
--subnet=172.18.0.0/16 \
--gateway=172.18.0.1 \
mynet

docker volume create myddata
```

### 搭建nginx
#### 目录结构
![目录结构](/images/docker_init/1573876590755.jpg)

* certs相关证书
* conf.d/default.conf http路由配置
* conf.d/jupyter.conf https路由配置
* public hexo生成的静态文件
#### 启动脚本run.sh
``` run.sh
docker run -d --rm \
-p 80:80 \
-p 443:443 \
--name dnginx --network mynet \
-v $(pwd)/conf.d:/etc/nginx/conf.d \
-v $(pwd)/certs:/etc/nginx/certs \
-v myddata:/usr/share/nginx/html \
-v $(pwd)/public:/data/public \
--ip 172.18.0.3 \
nginx:1.17.4
```
#### 路由配置
``` jupyter.conf
server {
        listen 443 ssl;                                                                                                                             
        server_name  localhost;
        client_max_body_size 1024M;

        ssl_certificate      /etc/nginx/certs/server.crt;
        ssl_certificate_key  /etc/nginx/certs/server.key;
        ssl_session_timeout  5m; 
        ssl_protocols  SSLv2 SSLv3 TLSv1;
        ssl_ciphers  HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers   on; 
        
        location /jupyter { 
            proxy_set_header Host $host;
            proxy_set_header X-Real-Scheme $scheme;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            proxy_http_version 1.1;
            proxy_redirect off;
            proxy_buffering off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_read_timeout 86400;

            #proxy_read_timeout 120s;
            proxy_next_upstream error;

            proxy_pass   https://172.18.0.2:8888;
        }   

        location ~ ^/gitbook/(.*)$ {
        proxy_set_header  X-Real-IP       $remote_addr;
        proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header  Host  $host;
        proxy_hide_header X-Current-Location;
        add_header X-Current-Location $request_uri;
        proxy_pass http://172.18.0.6:4000/$1;                                                                                            
        }

        # location ~ ^/fb/(.*)$ {
        # proxy_set_header  X-Real-IP       $remote_addr;
        # proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
        # proxy_set_header  Host  $host;
        # proxy_hide_header X-Current-Location;
        # add_header X-Current-Location $request_uri;
        # proxy_pass http://172.18.0.8:80/$1;                                                                                            
        # }

        location /fb {
        proxy_set_header  X-Real-IP       $remote_addr;
        proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header  Host  $host;
        proxy_hide_header X-Current-Location;
        add_header X-Current-Location $request_uri;
        proxy_pass http://172.18.0.8:80/fb;                                                                                            
        }

        # location /{
        # proxy_set_header  X-Real-IP       $remote_addr;
        # proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
        # proxy_set_header  Host  $host;
        # proxy_hide_header X-Current-Location;
        # add_header X-Current-Location $request_uri;
        # proxy_pass http://172.18.0.5:4000;                                                                                            
        # }

        location / {
          root   /data/public;		##请求对应文件位置
          index  index.html index.htm;		##请求对应文件
        }
    }
```

### 搭建jupyter
#### 启动脚本
``` run.sh
# 参考https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#notebook-options
# password用Ipython生成sha1

docker run --rm -d -p 8888:8888 \
--user root \
-v $(pwd)/note:/home/jovyan \
--ip 172.18.0.2 \
--name djupyter \
-e GEN_CERT=yes \
--network mynet \
jupyter/base-notebook:notebook-6.0.0 \
start-notebook.sh \
--NotebookApp.base_url=/jupyter \
--NotebookApp.password='sha1:xxxxxxx:xxxxxxxxxxxxxxxxxxxx'
```

### 搭建filebrowser
#### 启动脚本
``` run.sh
docker run -d \
--name dfb \
--network mynet \
--ip 172.18.0.8 \
-p 9999:80 \
-v $(pwd)/data:/srv \
-v $(pwd)/.filebrowser.json:/.filebrowser.json \
-v $(pwd)/database.db:/database.db \
filebrowser/filebrowser:latest
```

#### 体验地址
https://www.lxjsword.cn/fb/
账号: anonymous
密码: 123456

### 搭建hexo
#### 启动脚本
``` run.sh
docker run --rm -it \
--network mynet \
--ip 172.18.0.5 \
-p 5000:4000 \
-v $(pwd)/source:/opt/hexo/ipple1986/source \
-v $(pwd)/public:/opt/hexo/ipple1986/public \
-v $(pwd)/_config.yml:/opt/hexo/ipple1986/_config.yml \
-v $(pwd)/next:/opt/hexo/ipple1986/themes/next \
dhexo:latest
```

### 搭建gitbook
#### 启动脚本
``` run.sh
docker run --rm -it \
-p 4000:4000 \
--network mynet \
--ip 172.18.0.6 \
-v $(pwd)/gitbook:/srv/gitbook \
fellah/gitbook
```

#### 构建脚本
``` build.sh
docker run --rm \
-v $(pwd)/gitbook:/srv/gitbook \
-v myddata:/srv/html \
fellah/gitbook \
gitbook build . /srv/html/gitbook
```