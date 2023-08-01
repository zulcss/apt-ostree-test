FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y \
	python3 \
	python3-click \
	python3-pip \
	python3-pbr \
	python3-rich

ADD assets/15update-stamp /etc/apt/apt.conf.d/15-update-stamp
ADD assets/pip.conf /etc/pip.conf

RUN mkdir -p /usr/src/apt-ostree
WORKDIR /usr/src/apt-ostree
