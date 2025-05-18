FROM python:3.12-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY ./requirements.txt requirements.txt
COPY . /app
RUN python manage.py collectstatic --noinput
RUN pip install -r requirements.txt

CMD ["gunicorn", "src.wsgi:application", "--bind", "0.0.0.0:9090"]




