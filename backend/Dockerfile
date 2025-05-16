FROM python:3.12-slim

WORKDIR /backend

COPY ./backend /backend
COPY create_superuser.py /backend/

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

CMD ["sh", "-c", "\
    python manage.py migrate && \
    python create_superuser.py && \
    python manage.py collectstatic --noinput && \
    python telegram.py & \
    uvicorn mysite.asgi:application --workers 5 --host 0.0.0.0 --port 8000 & \
    celery -A mysite worker --loglevel=info & \
    celery -A mysite beat --loglevel=info && \
    wait"]