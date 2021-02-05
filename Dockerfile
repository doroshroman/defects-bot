FROM python:3.8.2-alpine

WORKDIR /usr/src/app

RUN apk update \
    && apk add libffi-dev openssl-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

CMD [ "python", "./echobot.py" ]
