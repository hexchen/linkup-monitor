FROM ubuntu:24.04

ENV TZ=Europe/Berlin
RUN apt-get update && apt-get install -y python3 python3-requests python3-yaml python3-prometheus-client

EXPOSE 8000

COPY . .
CMD ["python3", "main.py"]
