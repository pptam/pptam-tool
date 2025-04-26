FROM python:3.9.17-slim-bullseye

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

RUN echo "deb http://mirrors.ustc.edu.cn/debian bullseye main contrib non-free\n\
deb http://mirrors.ustc.edu.cn/debian bullseye-updates main contrib non-free" > /etc/apt/sources.list


RUN apt update -y
RUN apt install -y cmake libgl1-mesa-glx build-essential libglib2.0-0

ENV PYTHONUNBUFFERED=TRUE

RUN mkdir -p /app
ADD . /app/
WORKDIR /app

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt
RUN opentelemetry-bootstrap -a install
ENV OTEL_SERVICE_NAME ts-avatar-service
CMD ["opentelemetry-instrument", "gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]

EXPOSE 8080
