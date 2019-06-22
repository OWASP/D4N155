FROM alpine

RUN apk update && apk add python3
WORKDIR /root
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT bash main

