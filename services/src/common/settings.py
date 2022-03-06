from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    clickhouse_dsn: str = 'http://clickhouse:8123'
    kafka_dsn: str = 'kafka:9092'
    kafka_price_events_topic_prefix: str = 'price_events_'
    symbols_count: int = 100
    symbols_prefix: str = 'ticker_'