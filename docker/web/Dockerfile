FROM python:3
WORKDIR /root
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install flask
CMD [ "python3", "./app.py" ]
EXPOSE 5000
