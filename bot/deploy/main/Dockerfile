FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt
COPY ./deploy/main/entrypoint.sh /deploy/
COPY ./src/ .

CMD [ "sh", "/deploy/entrypoint.sh" ]