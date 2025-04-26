FROM python:3.9.17-slim-bullseye

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

RUN echo "deb https://mirrors.ustc.edu.cn/debian/ bullseye main contrib non-free\n\
deb-src https://mirrors.ustc.edu.cn/debian/ bullseye main contrib non-free\n\
deb https://mirrors.ustc.edu.cn/debian/ bullseye-updates main contrib non-free\n\
deb-src https://mirrors.ustc.edu.cn/debian/ bullseye-updates main contrib non-free\n\
deb https://mirrors.ustc.edu.cn/debian/ bullseye-backports main contrib non-free\n\
deb-src https://mirrors.ustc.edu.cn/debian/ bullseye-backports main contrib non-free\n\
deb https://mirrors.ustc.edu.cn/debian-security/ bullseye-security main contrib non-free\n\
deb-src https://mirrors.ustc.edu.cn/debian-security/ bullseye-security main contrib non-free" > /etc/apt/sources.list

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install cryptography
RUN pip install --no-cache-dir -r requirements.txt

ADD ./server.py /app/
ENV OTEL_SERVICE_NAME ts-voucher-service
CMD ["opentelemetry-instrument", "python", "server.py" ]