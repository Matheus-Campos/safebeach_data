FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "tail", "-f", "/dev/null" ]
