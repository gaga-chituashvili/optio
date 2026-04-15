from django.db import models

# Create your models here.


class Customer(models.Model):
    email = models.EmailField()
    total_spent = models.FloatField(default=0)
    last_transaction_date = models.DateTimeField(null=True)


class Segment(models.Model):
    name = models.CharField(max_length=255)
    is_dynamic = models.BooleanField(default=True)
    rules = models.JSONField()




class SegmentMembership(models.Model):
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('segment', 'customer')




class SegmentDelta(models.Model):
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    added = models.JSONField()     # [customer_ids]
    removed = models.JSONField()   # [customer_ids]
    created_at = models.DateTimeField(auto_now_add=True)



class SegmentDependency(models.Model):
    parent = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='children')
    child = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='parents')