FROM debian:9-slim

WORKDIR /root
RUN apt-get update && apt-get update && apt-get install python3-pip git -y
RUN git clone https://github.com/adasecurity/D4N155.git && cd D4N155 && pip3 install -r requirements.txt
ENTRYPOINT ["bash","/root/D4N155/main"]
