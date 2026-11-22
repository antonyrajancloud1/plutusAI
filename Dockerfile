# One container with everything: MySQL, Redis, Celery worker and the Django server
# (plus Chromium on a virtual display, which the Exness broker login drives).
# Built from the local folder (no git clone), so the image has exactly this code.
#
#   docker build -t plutus .
#   docker run -d --name plutus -p 8090:8000 -v plutus_mysql:/var/lib/mysql \
#       -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_EMAIL=admin@example.com \
#       -e DJANGO_SUPERUSER_PASSWORD=change-me plutus
#
# MySQL data lives in the plutus_mysql volume, so it survives rebuilds.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Kolkata \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/opt/venv/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-venv python3-dev build-essential pkg-config \
        mysql-server libmysqlclient-dev redis-server tzdata ca-certificates procps xvfb xauth \
    && ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/run/mysqld && chown mysql:mysql /var/run/mysqld

WORKDIR /app

# Dependencies first so code changes don't reinstall them.
COPY requirements.txt .
RUN python3 -m venv /opt/venv && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && playwright install --with-deps chromium \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN mkdir -p logs && chmod +x docker/entrypoint.sh

VOLUME /var/lib/mysql
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/login', timeout=4)" || exit 1

CMD ["docker/entrypoint.sh"]
