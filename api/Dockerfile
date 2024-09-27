FROM python:3.10-slim

WORKDIR /app

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    netcat-openbsd \
    supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . .

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000

ENTRYPOINT [ "/app/entrypoint.sh" ]