FROM ubuntu:20.04

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

# Install necessary packages and add the deadsnakes PPA
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    curl \
    gnupg \
    build-essential \
    mysql-server \
    redis-server \
    vim \
    libmysqlclient-dev \
    pkg-config \
    net-tools \
    git && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Update `python3` to point to `python3.10`
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2

# Install pip for Python 3.10
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

# Install cloudflared
RUN curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared && \
    chmod +x /usr/local/bin/cloudflared

# Configure MySQL
RUN sed -i 's/^\(bind-address\s.*\)/# \1/' /etc/mysql/mysql.conf.d/mysqld.cnf && \
    echo '[mysqld]\nskip-host-cache\nskip-name-resolve' > /etc/mysql/conf.d/docker.cnf && \
    mkdir -p /var/run/mysqld && chown -R mysql:mysql /var/run/mysqld
VOLUME /var/lib/mysql

# Upgrade pip for Python 3.10
RUN python3 -m pip install --upgrade pip

# Clone repository and install requirements
RUN git clone https://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@github.com/antonyrajancloud1/plutusAI.git /app_source
WORKDIR /app_source
RUN python3 -m pip install -r requirements.txt

# Expose ports
EXPOSE 3306
EXPOSE 6379

# Create and run startup script
RUN echo "#!/bin/bash" > /startup.sh && \
    echo "echo 'Starting MySQL...'" >> /startup.sh && \
    echo "/usr/sbin/mysqld &" >> /startup.sh && \
    echo "echo 'Starting Redis...'" >> /startup.sh && \
    echo "/usr/bin/redis-server &" >> /startup.sh && \
    echo "sleep 10" >> /startup.sh && \
    echo "echo 'Creating Database...'" >> /startup.sh && \
    echo "mysql -e 'CREATE DATABASE IF NOT EXISTS madara_db;'" >> /startup.sh && \
    echo "echo 'Running Django Migrations...'" >> /startup.sh && \
    echo "python3 manage.py makemigrations" >> /startup.sh && \
    echo "python3 manage.py migrate" >> /startup.sh && \
    echo "exec /bin/bash" >> /startup.sh && \
    chmod +x /startup.sh

CMD ["/startup.sh"]
