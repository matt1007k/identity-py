import redis
import json
from typing import Optional, TypeVar
from pydantic import BaseModel

from core.config.env import REDIS_HOST, REDIS_PORT

T = TypeVar("T", bound=BaseModel)


class RedisCache:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=0):
        try:
            self.client = redis.Redis(
                host=host, port=port, db=db, decode_responses=True
            )

            self.default_expiration = 60 * 60 * 24  # 24 hours in seconds
            self.client.ping()  # Prueba la conexión
            print(f"Conectado a Redis en {host}:{port}")
        except redis.exceptions.ConnectionError as e:
            print(f"Redis connection error: {e}")
            raise

    def get_data(self, key: str, model_class: type[T]) -> Optional[T]:
        print(REDIS_HOST, REDIS_PORT)
        """Retrieve data from Redis cache"""
        try:
            cached = self.client.get(key)
            if cached:
                data = json.loads(cached)
                return model_class(**data)
            return None
        except redis.exceptions.ConnectionError as e:
            print(f"Redis connection error: {e}")
            return None

    def save_data(self, key: str, data: BaseModel, expiration: int = None) -> None:
        """Save data to Redis cache"""
        if expiration is None:
            expiration = self.default_expiration
        self.client.setex(key, expiration, json.dumps(data.model_dump()))


# Create a singleton instance
redis_cache = RedisCache()
