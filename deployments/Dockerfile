WORKDIR /app

COPY deployments/requirements.txt /app/deployments/requirements.txt
RUN pip install -r /app/deployments/requirements.txt
RUN pip install gunicorn

COPY  . /app

CMD ["gunicorn", "rc_backend.rc_backend.wsgi:application", "--bind", "0.0.0.0:9090"]




