import redis
 

redis_client = redis.Redis(
    host="127.0.0.1", 
    port=6379,
    db=0,
    decode_responses=True
)

REDIS_KEY = "segment_update_queue"


def queue_update(customer_id):
    redis_client.sadd(REDIS_KEY, customer_id)