FROM python:3.12-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY ./requirements.txt requirements.txt
COPY . /app

RUN pip install -r requirements.txt
RUN chmod +x /app/deployments/entrypoint.sh

ENTRYPOINT ["/app/deployments/entrypoint.sh"]




