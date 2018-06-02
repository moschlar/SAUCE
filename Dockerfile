FROM ubuntu
MAINTAINER Moritz Schlarb

RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get -y install python python-pip python-numpy python-matplotlib
RUN apt-get -y install language-pack-en-base language-pack-de-base git java-sdk-headless
RUN pip install --upgrade pip && pip install tg.devtools

ADD ["https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64.deb", "/tmp"]
RUN ["dpkg", "-i", "/tmp/dumb-init_1.2.1_amd64.deb"]

RUN mkdir -p /opt/SAUCE
COPY . /opt/SAUCE

RUN ["pip", "install", "-e", "/opt/SAUCE"]

WORKDIR /opt/SAUCE

RUN ["gearbox" ,"setup-app", "-c", "development.ini"]

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD ["gearbox", "serve", "-c", "development.ini"]

EXPOSE 8080
