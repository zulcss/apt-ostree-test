# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y \
	bdebstrap \
	bubblewrap \
	debos \
	git \
	ostree \
	python3 \
	python3-apt \
	python3-click \
	python3-pip \
	python3-pbr \
	python3-rich \
	reprepro \
	vim

ADD assets/pip.conf /etc/pip.conf

RUN mkdir -p /usr/src/apt-ostree
WORKDIR /usr/src/apt-ostree
