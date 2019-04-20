FROM ubuntu:16.04

MAINTAINER Dockerfiles

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	git \
	python3 \
	python3-dev \
	libmysqlclient-dev \
	python3-setuptools \
	python3-pip \
	nginx && \
	pip3 install --upgrade pip setuptools && \
   rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY requirements ./requirements
RUN pip3 install -r requirements.txt

# add (the rest of) our code
COPY . .
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic
EXPOSE 8000

CMD ["uwsgi", "-i" ,"uwsgi.ini", "--http", ":8000"]