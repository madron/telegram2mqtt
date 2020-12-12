FROM alpine:3.12

# Reguired packages
RUN apk add --no-cache su-exec py3-pip

# Compiled requirements
RUN mkdir -p /src/requirements
ADD requirements/compiled.txt /src/requirements
RUN    apk add --no-cache gcc python3-dev musl-dev libffi-dev \
   && pip install wheel \
   && pip install -r /src/requirements/compiled.txt \
   && apk del gcc python3-dev musl-dev libffi-dev

# Requirements
ADD requirements/common.txt /src/requirements
RUN pip install -r /src/requirements/common.txt

# Docker directory
ADD docker /src/docker
RUN chmod 0755 /src/docker/*.sh
ENTRYPOINT ["/src/docker/entrypoint.sh"]

# Src
ADD telegram2mqtt /src/telegram2mqtt
ADD setup.py /src

# Install
RUN cd /src ; python3 setup.py install
