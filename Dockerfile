FROM ubuntu:precise

ENV DEBIAN_FRONTEND noninteractive

#ADD https://help.ubuntu.com/lts/sample/sources.list /etc/apt/sources.list
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN echo "deb http://archive.ubuntu.com/ubuntu precise-updates main universe" >> /etc/apt/sources.list
RUN echo "deb http://security.ubuntu.com/ubuntu precise-security main universe" >> /etc/apt/sources.list
RUN apt-get -q update

#RUN apt-get -q -y upgrade
RUN apt-get -q -y install wget
RUN apt-get -q -y install --no-install-recommends gcc openjdk-7-jre-headless openjdk-7-jdk
RUN apt-get -q -y install python-pip python-dev
#RUN apt-get -q -y install python-numpy python-matplotlib

ENV DEBIAN_FRONTEND dialog

RUN mkdir -p /opt/SAUCE && cd /opt/SAUCE/ && wget -q --no-check-certificate https://github.com/moschlar/SAUCE/archive/master.tar.gz
RUN tar -xzf /opt/SAUCE/master.tar.gz -C /opt/SAUCE/

RUN pip install -i http://tg.gy/222/ tg.devtools
RUN pip install -M -e /opt/SAUCE/SAUCE-master
#RUN pip install -M SAUCE[similarity,nosetests]

RUN cd /opt/SAUCE/SAUCE-master/ && paster setup-app development.ini

RUN sed -e 's/127.0.0.1/0.0.0.0/g' -i /opt/SAUCE/SAUCE-master/development.ini

MAINTAINER moschlar

EXPOSE 8080

ENTRYPOINT cd /opt/SAUCE/SAUCE-master/ && paster serve development.ini
CMD cd /opt/SAUCE/SAUCE-master/ && paster serve development.ini

