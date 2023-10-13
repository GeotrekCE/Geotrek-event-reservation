FROM ubuntu:20.04

WORKDIR /opt/png-resa

ENV TZ="Europe/Paris"

RUN apt-get update -qq && DEBIAN_FRONTEND="noninteractive" apt-get install -y \
    gcc \
    python3.8-venv \
    python3-dev \
    iproute2 \
    libpq-dev \
    tzdata && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir -U pip setuptools wheel
COPY requirements.txt requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt -U

COPY . .

ENTRYPOINT ["/bin/sh", "-e", "/opt/png-resa/entrypoint.sh"]
EXPOSE 8000
CMD ["gunicorn", "--name reservations_animations", "--workers 4", "--bind=0.0.0.0:8000", "--timeout=30", "server:app"]
