FROM python:3.8.11-alpine3.14

RUN echo -e "https://mirrors.aliyun.com/alpine/v3.14/main/\nhttps://mirrors.aliyun.com/alpine/v3.14/community/" > /etc/apk/repositories \
    && apk update \
    && apk add --no-cache gcc g++ make cmake libc-dev libffi-dev musl-dev libxslt-dev openssl-dev linux-headers python3 python3-dev py-pip tzdata \
    && apk upgrade musl \
    && echo "Asia/Shanghai" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN python3 -m pip install -i https://pypi.douban.com/simple/ --upgrade pip
RUN pip3 install -i https://pypi.douban.com/simple/ uWSGI==2.0.19.1

RUN mkdir /config

ADD requirements.txt /config/
RUN pip3 install -i https://pypi.douban.com/simple/ -r /config/requirements.txt

RUN mkdir /prometheus-flask
WORKDIR /prometheus-flask
