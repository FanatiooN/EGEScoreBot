FROM python:3.11.4-slim

RUN apt-get update & pip3 install --upgrade setuptools && apt-get install -y 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
