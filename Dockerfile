FROM python:3.13.2

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y dos2unix \
  && dos2unix start.sh \
  && chmod +x start.sh

CMD ["./start.sh"]