#!/bin/bash
# Starts MySQL, Redis, the Celery worker and Django in one container, and shuts
# MySQL down cleanly on `docker stop` so its data files stay consistent.
set -euo pipefail
cd /app

log() { echo "[entrypoint] $*"; }

# ---------------------------------------------------------------- MySQL
mkdir -p /var/run/mysqld
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld
if [ ! -d /var/lib/mysql/mysql ]; then
    log "Initialising empty MySQL data directory"
    mysqld --initialize-insecure --user=mysql
fi

log "Starting MySQL"
mysqld --user=mysql &
MYSQL_PID=$!
for _ in $(seq 1 60); do
    mysqladmin ping --silent 2>/dev/null && break
    sleep 1
done
mysqladmin ping --silent || { log "MySQL did not start"; exit 1; }
mysql -e "CREATE DATABASE IF NOT EXISTS madara_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# ---------------------------------------------------------------- Redis
log "Starting Redis"
redis-server --daemonize yes --bind 127.0.0.1 --save "" --appendonly no

# ---------------------------------------------------------------- virtual display
# The Exness broker launches Chromium with headless=False, so it needs a display.
log "Starting virtual display"
Xvfb :99 -screen 0 1280x1024x24 -nolisten tcp >/dev/null 2>&1 &
export DISPLAY=:99

# ---------------------------------------------------------------- Django
log "Applying migrations"
python3 manage.py migrate --noinput

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    if python3 manage.py shell -c "from django.contrib.auth.models import User; import sys; sys.exit(0 if User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists() else 1)"; then
        log "Admin user ${DJANGO_SUPERUSER_USERNAME} already exists"
    else
        log "Creating admin user ${DJANGO_SUPERUSER_USERNAME}"
        python3 manage.py createsuperuser --noinput
    fi
fi

# Same command the Admin Console's Celery stop/restart buttons look for.
log "Starting Celery worker"
celery -A plutus.celery worker --loglevel=info --autoscale=100,3 >> logs/celery.log 2>&1 &

log "Starting Django on :8000"
python3 manage.py runserver 0.0.0.0:8000 --noreload &
DJANGO_PID=$!

shutdown() {
    log "Stopping"
    kill "$DJANGO_PID" 2>/dev/null || true
    pkill -f "celery -A plutus.celery" 2>/dev/null || true
    redis-cli shutdown nosave 2>/dev/null || true
    pkill Xvfb 2>/dev/null || true
    mysqladmin shutdown 2>/dev/null || kill "$MYSQL_PID" 2>/dev/null || true
    wait "$MYSQL_PID" 2>/dev/null || true
    exit 0
}
trap shutdown SIGTERM SIGINT

# Stay up while Django runs; if it dies, stop everything so Docker can restart us.
wait "$DJANGO_PID" || true
shutdown
