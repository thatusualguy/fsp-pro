FROM python:3.12-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./static ./src ./manage.py ./config.py /app/

CMD ["gunicorn", "src.wsgi:application", "--bind", "0.0.0.0:9090"]




