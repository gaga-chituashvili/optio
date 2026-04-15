import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

REDIS_KEY = "segment_update_queue"


def queue_update(customer_id):
    redis_client.sadd(REDIS_KEY, customer_id)