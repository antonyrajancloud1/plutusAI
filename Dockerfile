FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    mysql-server \
    redis-server \
    vim \
    libmysqlclient-dev \
    pkg-config \
    net-tools \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure MySQL
RUN sed -i 's/^\(bind-address\s.*\)/# \1/' /etc/mysql/mysql.conf.d/mysqld.cnf
RUN echo '[mysqld]\nskip-host-cache\nskip-name-resolve' > /etc/mysql/conf.d/docker.cnf
RUN mkdir -p /var/run/mysqld && chown -R mysql:mysql /var/run/mysqld
VOLUME /var/lib/mysql

# Upgrade pip
RUN pip3 install --upgrade pip

# Clone repository and install requirements
RUN git clone https://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@github.com/antonyrajancloud1/plutusAI.git /app_source
WORKDIR /app_source
RUN pip3 install -r requirements.txt

# Expose ports
EXPOSE 3306
EXPOSE 6379

# Create and run startup script
RUN echo "#!/bin/bash" > /startup.sh && \
    echo "service mysql start" >> /startup.sh && \
    echo "service redis-server start" >> /startup.sh && \
    echo "mysql -e \"CREATE DATABASE IF NOT EXISTS madara_db;\"" >> /startup.sh && \
    echo "python3 manage.py makemigrations" >> /startup.sh && \
    echo "python3 manage.py migrate" >> /startup.sh && \
    echo "exec /bin/bash" >> /startup.sh && \
    chmod +x /startup.sh

CMD ["/startup.sh"]
