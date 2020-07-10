FROM python:3
MAINTAINER kunyu.he.uchicago@gmail.com

RUN apt-get update
RUN apt-get -y install nano vim

ENV  TIME_ZONE Asia/Shanghai
ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple"

RUN echo "${TIME_ZONE}" > /etc/timezone
RUN ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

RUN mkdir /projects
WORKDIR /projects
COPY . /projects/

RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip
RUN pip --no-cache-dir install  -i ${PIPURL} -r requirements.txt

RUN chmod 777 -R ./*
CMD ./run.sh
