FROM python:3.7

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY ./config /config
COPY ./userservice /userservice

ENTRYPOINT ["python", "userservice"]