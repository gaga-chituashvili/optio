from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now

from core.models import Customer, Segment
from core.signals import on_customer_update





@api_view(['POST'])
def simulate_transaction(request):
    customer_id = request.data.get("id")

    if not customer_id:
        return Response({"error": "id is required"}, status=400)

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

    customer.total_spent += 100
    customer.last_transaction_date = now()
    customer.save()

    on_customer_update(Customer, customer)

    return Response({"status": "ok"})

@api_view(['GET'])
def get_segments(request):
    segments = Segment.objects.all().values("id", "name")
    return Response(list(segments))