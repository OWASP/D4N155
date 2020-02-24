FROM python:3.8.1-alpine
WORKDIR /root/
RUN apk add git
RUN git clone https://github.com/OWASP/D4N155.git
WORKDIR D4N155
RUN pip3 install -r requirements.txt
ENTRYPOINT ["bash"]
