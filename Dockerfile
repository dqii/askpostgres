FROM postgres:15

WORKDIR /app

RUN apt-get update && apt-get install -y python3.9 python3-pip python3-venv git libpq-dev

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5432