FROM python:3

RUN apt-get update && apt-get install -y vim

RUN mkdir -p /code/
WORKDIR /code/
ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .

EXPOSE 8838

ENTRYPOINT ["gunicorn", "-k", "gevent", "-t", "600", "-w", "4", "-b", "0.0.0.0:8838", "wsgi:application"]