FROM python:3
MAINTAINER kunyu.he.uchicago@gmail.com


ENV  TIME_ZONE Asia/Shanghai
ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple"

RUN echo "${TIME_ZONE}" > /etc/timezone
RUN ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

RUN mkdir /projects

WORKDIR /logs
WORKDIR /projects

COPY .  /projects/

RUN apk --update add bash nano

RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip
RUN pip --no-cache-dir install  -i ${PIPURL} -r requirements.txt

CMD ./run.sh
