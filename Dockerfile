FROM node:boron
MAINTAINER Afroz Ahamad <enigmaeth@gmail.com>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	python3-dev \
	libpq-dev \
	libevent-dev \
	libmagic-dev \
	python3-pip && apt-get clean -y

# copy requirements
COPY package.json /usr/src/app/
COPY bower.json /usr/src/app/
COPY .bowerrc /usr/src/app
COPY requirements.txt /usr/src/app/

# install requirements
RUN npm install
RUN npm install --global bower
RUN bower --allow-root install
RUN pip3 install -r requirements.txt

# Bundle app source
COPY . /usr/src/app

EXPOSE 7001

CMD [ "python3", "app/server.py" ]
