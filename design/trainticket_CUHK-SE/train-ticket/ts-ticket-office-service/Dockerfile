FROM node:20-bullseye

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

WORKDIR /app

ADD . . 

RUN npm config set registry https://registry.npmmirror.com \
    && npm install \
    && npm cache clean --force  # 清理缓存，减小镜像体积

ENV OTEL_SERVICE_NAME "ts-ticket-office-service"

CMD [ "npm", "start" ]

EXPOSE 8080