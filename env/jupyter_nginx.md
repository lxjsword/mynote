---
title: jupyter+nginx部署踩坑记录
date: 2019-11-09 11:56:35
tags: tool
---
## jupyter问题
1. cd到数据目录
2. jupyter会新建，删除服务器上的文件， 涉及linux权限问题，用root用户运行
3. log里面会就来登录token

```sh
cd /home/ryanxjli/jupyter_notebook/data/ && nohup /home/ryanxjli/venv-jupyter/bin/jupyter notebook --allow-root --port ${port} --ip=${ip} > /home/ryanxjli/jupyter_notebook/log/jupter_notebook.log 2>&1 &
```

## nginx问题
1. jupyter服务单独域名部署，保证路由正确
2. 通过nginx反向代理会有跨域问题, mynote.com和9.134.7.141:9999存在跨域， 需要设置proxy_set_header Host, 如下
3. proxy_pass设置， 如果域名后面没有uri,url会原样替换， 如果有uri,会替换， 如：

    3.1 未配置uri
        location / {
            proxy_pass   http://9.134.7.141:9999;
        }
        访问mynote.com/xxx会转为9.134.7.141:9999/xxx

    3.2 配置了uri,注意后面的/
        location /note/ {
            proxy_pass   http://9.134.7.141:9999/;
        }
        访问mynote.com/note/xxx会转为9.134.7.141:9999/xxx 
     
    3.3 jupyter notebook使用了websocket, 需要websocket支持
        proxy_http_version 1.1;
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection "upgrade";

```sh
server {
        listen       80;
        server_name  mynote.com;
    
        location / {
			proxy_set_header Host $host;
			proxy_set_header X-Real-Scheme $scheme;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

			# WebSocket support
			proxy_http_version 1.1;
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection "upgrade";

			proxy_read_timeout 120s;
			proxy_next_upstream error;
		
            proxy_pass   http://9.134.7.141:9999;
        }
	}
    
server {
        listen       443 ssl;
        server_name  myspace.com;

        ssl_certificate      /home/ryanxjli/server.crt;
        ssl_certificate_key  /home/ryanxjli/server.key;
        ssl_session_timeout  5m; 
        ssl_protocols  SSLv2 SSLv3 TLSv1;
        ssl_ciphers  HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers   on; 
    
        location /jupyter { 
            proxy_set_header Host $host;
            proxy_set_header X-Real-Scheme $scheme;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            proxy_read_timeout 120s;
            proxy_next_upstream error;

            proxy_pass   https://127.0.0.1:8888/jupyter;                                                                                        
        }   
    }
```