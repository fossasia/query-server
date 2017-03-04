FROM node:boron
MAINTAINER Afroz Ahamad <enigmaeth@gmail.com>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update

# install deps
RUN apt-get install -y --no-install-recommends build-essential python-dev libpq-dev libevent-dev libmagic-dev python-pip && apt-get clean -y && curl -sL https://deb.nodesource.com/setup_4.x | bash && apt-get install -y --force-yes nodejs

# copy requirements
COPY package.json /usr/src/app/
COPY requirements.txt /usr/src/app/

# install requirements
RUN npm install
RUN pip install -r requirements.txt

# Bundle app source
COPY . /usr/src/app

EXPOSE 7001

CMD [ "npm", "start" ]
