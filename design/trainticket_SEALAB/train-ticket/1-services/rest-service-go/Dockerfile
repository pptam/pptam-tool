# FROM grayzone/beego
FROM mrrm/web.go


RUN mkdir -p /app
WORKDIR /app

# ADD ./node_modules /app/node_modules
# ADD ./package.json /app/
# RUN npm install

ADD ./server.go /app/
RUN go build
CMD [ "./app" ]

EXPOSE 16102