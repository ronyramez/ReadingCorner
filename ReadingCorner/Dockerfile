FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
#
EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
