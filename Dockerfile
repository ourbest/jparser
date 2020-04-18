FROM ourbest/python3

RUN mkdir -p /code/
WORKDIR /code/
ADD requirements.txt .

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

ADD eparser eparser
ADD templates templates
ADD "*.py" ./

EXPOSE 8838

ENV TZ "Asia/Shanghai"
ENV SD_SERVER "http://10.9.131.109:4367/"

ENTRYPOINT ["gunicorn", "-k", "gevent", "-t", "180", "-w", "4", "-b", "0.0.0.0:8838", "wsgi:application"]