FROM python:3.8

WORKDIR /app/
COPY unit.py requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

CMD pytest unit.py