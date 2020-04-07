FROM python:3.6

RUN apt-get update && apt-get install -y vim

RUN mkdir -p /code/
WORKDIR /code/
ADD requirements.txt .

RUN pip install -r requirements.txt

ADD eparser .
ADD templates .
ADD "*.py" .

EXPOSE 8838

ENV TZ "Asia/Shanghai"
ENV SD_SERVER "http://10.9.131.109:4367/"

ENTRYPOINT ["gunicorn", "-k", "gevent", "-t", "180", "-w", "4", "-b", "0.0.0.0:8838", "wsgi:application"]