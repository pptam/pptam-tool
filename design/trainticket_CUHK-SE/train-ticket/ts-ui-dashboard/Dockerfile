FROM caddy:2.9
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apk del tzdata
COPY static /usr/share/nginx/html
COPY Caddyfile /etc/Caddyfile

CMD ["caddy", "run", "--config", "/etc/Caddyfile"]