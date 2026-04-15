from celery import shared_task
from core.services.segment_engine import evaluate_segment
from core.services.queue import redis_client, REDIS_KEY
from core.models import Segment

@shared_task
def evaluate_segment_task(segment_id):
    evaluate_segment(segment_id)



@shared_task
def process_batch():
    
    pipe = redis_client.pipeline()
    pipe.smembers(REDIS_KEY)
    pipe.delete(REDIS_KEY)
    ids, _ = pipe.execute()

    if not ids:
        return

    
    customer_ids = [int(i) for i in ids]

    print(f"Processing batch: {len(customer_ids)} customers")

    
    for segment in Segment.objects.filter(is_dynamic=True):
        evaluate_segment(segment.id)