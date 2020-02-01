FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt && pip install flask
CMD [ "python", "./app.py" ]

