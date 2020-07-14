FROM python:3

RUN apt-get update
RUN apt-get -y install nano

ENV  TIME_ZONE Asia/Shanghai
ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple"

RUN echo "${TIME_ZONE}" > /etc/timezone
RUN ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

RUN mkdir /projects
WORKDIR /projects
COPY . /projects/

RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip
RUN pip --no-cache-dir install  -i ${PIPURL} -r requirements.txt

CMD python run.py
