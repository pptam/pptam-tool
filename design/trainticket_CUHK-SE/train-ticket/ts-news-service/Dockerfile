FROM golang:alpine3.19

RUN mkdir -p /app
WORKDIR /app
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apk del tzdata
ADD . /app/
RUN go mod tidy && go build -o app
CMD [ "./app" ]