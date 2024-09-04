FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update
RUN apt-get -y install cron

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./deploy/updater/entrypoint.sh /deploy/


COPY ./src/ .

CMD ["sh", "/deploy/entrypoint.sh"]
