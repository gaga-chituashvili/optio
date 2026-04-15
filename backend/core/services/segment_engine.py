from core.models import (
    Segment,
    Customer,
    SegmentMembership,
    SegmentDelta,
    SegmentDependency
)

from core.tasks import evaluate_segment_task
from core.services.notifications import notify 


def apply_rules(customer, rules):
    if not rules:
        return True

    if "min_spent" in rules:
        if customer.total_spent < rules["min_spent"]:
            return False

    return True


def evaluate_segment(segment_id):
    try:
        segment = Segment.objects.get(id=segment_id)
    except Segment.DoesNotExist:
        return

    if not segment.is_dynamic:
        return

    customers = Customer.objects.all()

    new_ids = {
        c.id for c in customers
        if apply_rules(c, segment.rules)
    }

    old_ids = set(
        SegmentMembership.objects.filter(segment=segment)
        .values_list('customer_id', flat=True)
    )

    added = new_ids - old_ids
    removed = old_ids - new_ids

    if not added and not removed:
        return

  
    SegmentMembership.objects.filter(
        segment=segment,
        customer_id__in=removed
    ).delete()

  
    SegmentMembership.objects.bulk_create(
        [
            SegmentMembership(segment=segment, customer_id=i)
            for i in added
        ],
        ignore_conflicts=True
    )

    
    delta = SegmentDelta.objects.create(
        segment=segment,
        added=list(added),
        removed=list(removed)
    )

 
    notify(delta)
    trigger_dependent_segments(segment.id)


def trigger_dependent_segments(segment_id):
    children = SegmentDependency.objects.filter(parent_id=segment_id)

    for child in children:
        evaluate_segment_task.delay(child.child_id)