FROM python:3.8

WORKDIR /api
COPY requeriments.txt /api/requeriments.txt

RUN pip install --no-cache-dir --upgrade -r /api/requeriments.txt
RUN apt-get update && apt-get install -y default-jdk

COPY . /api

ENV JAVA_HOME /usr/lib/jvm/default-jvm

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port","80"]