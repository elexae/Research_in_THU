FROM ubuntu:16.04
LABEL name="none" email="none@none.cn"

RUN apt-get update && \
    apt-get install -y python-pip libsodium18

RUN pip install shadowsocks==2.8.2

COPY ./config.json /etc/shadowsocks/config.json

ENTRYPOINT [ "/usr/local/bin/sslocal", "-c", "/etc/shadowsocks/config.json" ]
