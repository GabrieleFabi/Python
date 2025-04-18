# Use a base image with Python installed
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y python3 \
    python3-pip \
    && apt-get clean \
    && apt-get autoremove

COPY ./requirements.txt /var/app/requirements.txt
RUN pip install -r /var/app/requirements.txt

COPY ./ var/app/

WORKDIR /var/app

CMD /var/app