#!/bin/bash
set -xe

echo "
CREATE DATABASE IF NOT EXISTS market;

CREATE TABLE IF NOT EXISTS market.prices (
    symbol String,
    timestamp Float64,
    price Float64,
    decimal_places Int8
) ENGINE = Kafka SETTINGS
    kafka_broker_list = '$KAFKA_DSN',
    kafka_topic_list = '$KAFKA_CH_TOPIC',
    kafka_group_name = 'db',
    kafka_format = 'JSONEachRow',
    kafka_max_block_size = 1,
    kafka_commit_every_batch = 1;

CREATE TABLE IF NOT EXISTS market.prices_stats (
    symbol String,
    timestamp Float64,
    price Float64,
    decimal_places Int8
) ENGINE = MergeTree()
ORDER BY timestamp;

CREATE MATERIALIZED VIEW IF NOT EXISTS market.prices_consumer TO market.prices_stats AS SELECT * FROM market.prices;

" | clickhouse client -n
