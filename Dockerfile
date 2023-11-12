FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN groupadd --gid 1000 python && useradd --uid 1000 --gid python --create-home --shell=/bin/bash python

USER python

CMD [ "tail", "-f", "/dev/null" ]
