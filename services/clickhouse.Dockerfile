FROM yandex/clickhouse-server

#COPY kafka.xml /etc/clickhouse-server/config.d/kafka.xml
COPY init-db.sh /docker-entrypoint-initdb.d/init-db.sh