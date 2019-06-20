FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && pip install flask
COPY . .
CMD [ "python", "./app.py" ]
EXPOSE 5000
