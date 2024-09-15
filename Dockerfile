FROM python:3.9.7-alpine
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
RUN flask db init && flask db migrate && flask db upgrade
CMD ["python", "main.py"]