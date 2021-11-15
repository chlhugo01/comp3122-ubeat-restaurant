FROM python:3.8

WORKDIR /app/
COPY restaurant_order.py requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

CMD python restaurant_order.py