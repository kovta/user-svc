FROM python:3.7

COPY ./requirements.txt /
RUN pip install -r requirements.txt

COPY ./config/users_test.yaml /config/users.yaml
COPY ./userservice /userservice

ENTRYPOINT ["python", "userservice"]