FROM ubuntu
MAINTAINER Moritz Schlarb

RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get -y install python python-pip python-numpy python-matplotlib

RUN mkdir -p /opt/SAUCE

COPY . /opt/SAUCE

RUN pip install tg.devtools
RUN pip install -e /opt/SAUCE

WORKDIR /opt/SAUCE

RUN gearbox setup-app -c development.ini

ENTRYPOINT gearbox serve -c development.ini

EXPOSE 8080
