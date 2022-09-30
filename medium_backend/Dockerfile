FROM python:3.11-rc-slim-buster
# PYTHONUNBUFFERED prevents Python from buffering our standard output stream
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt
CMD sh init.sh && python manage.py runserver 0.0.0.0:8000
