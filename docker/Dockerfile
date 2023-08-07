FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y \
	bdebstrap \
	ostree \
	python3 \
	python3-click \
	python3-pip \
	python3-pbr \
	python3-rich

ADD assets/pip.conf /etc/pip.conf

RUN mkdir -p /usr/src/apt-ostree
WORKDIR /usr/src/apt-ostree
