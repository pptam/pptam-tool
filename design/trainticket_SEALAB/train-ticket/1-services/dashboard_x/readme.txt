

nginx lua:
http://www.lua.org/
http://www.lua.org/pil/


openresty:
https://openresty.org/cn/
https://github.com/openresty/docker-openresty
https://github.com/openresty/lua-nginx-module


docker openresty:
https://hub.docker.com/r/openresty/openresty/
docker run [options] openresty/openresty:trusty
docker pull openresty/openresty:trusty
docker pull openresty/openresty:1.11.2.3-trusty
docker pull openresty/openresty
docker run -d -p 16600:16600 --name my-openresty openresty/openresty
docker exec -it my-openresty /bin/sh


docker build:
docker build -t my/openresty .
docker run -d -p 16600:16600 --name my-openresty my/openresty
docker exec -it my-openresty /bin/sh
    

url:
http://localhost:16600/