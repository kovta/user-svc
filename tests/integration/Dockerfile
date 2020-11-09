FROM python:3.7

COPY ./requirements.txt /
COPY ./requirements-dev.txt /
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY ./config /config
COPY ./userservice /
COPY ./tests /tests
COPY ./init_db.py /

ENTRYPOINT ["pytest", "tests/integration"]