FROM alpine:3.12

# Reguired packages
RUN apk add --no-cache su-exec py3-pip

# Requirements
RUN mkdir -p /src
ADD requirements.txt /src
RUN pip install -r /src/requirements.txt

# Docker directory
ADD docker /src/docker
RUN chmod 0755 /src/docker/*.sh
ENTRYPOINT ["/src/docker/entrypoint.sh"]

# Src
ADD telegram2mqtt /src/telegram2mqtt
ADD setup.py /src

# Install
RUN cd /src ; python3 setup.py install
