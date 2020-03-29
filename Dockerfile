FROM golang:buster
WORKDIR /root/
RUN apt update && apt-get install python3-pip git -y
RUN git clone https://github.com/OWASP/D4N155.git && cd D4N155 && pip3 install -r requirements.txt
ENTRYPOINT ["bash"]
