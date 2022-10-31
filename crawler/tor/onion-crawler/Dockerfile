# This dockerfile allows to run an crawl inside a docker container

# Pull base image.
#FROM debian:stable-slim
#FROM python:3
FROM ubuntu:20.04

# Install required packages.
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install sudo build-essential autoconf git zip unzip xz-utils
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install libtool libevent-dev libssl-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install python3 python3-dev python3-setuptools python3-pip
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install net-tools ethtool tshark libpcap-dev iw tcpdump
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install xvfb firefox
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install netcat
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install sshpass
RUN DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --yes install iproute2
RUN apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Install python requirements.
RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# add host user to container
RUN adduser --system --group --disabled-password --gecos '' --shell /bin/bash docker

# download geckodriver
COPY geckodriver-v0.29.0-linux64.tar.gz /bin/geckodriver-v0.29.0-linux64.tar.gz
RUN tar -zxvf /bin/geckodriver* -C /bin/
ENV PATH /bin/geckodriver:$PATH

# download torbundle
COPY tor-browser-linux64-11.0.15_en-US.tar.xz /home/docker/tbb_setup/
RUN tar -xvf /home/docker/tbb_setup/tor-browser-linux64-11.0.15_en-US.tar.xz -C /home/docker/tbb_setup/

# Set the display
ENV DISPLAY $DISPLAY
