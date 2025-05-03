FROM python:3.12-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY  . /app

CMD ["gunicorn", "rc_backend.rc_backend.wsgi:application", "--bind", "0.0.0.0:9090"]




