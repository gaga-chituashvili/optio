from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now

from core.models import Customer
from core.signals import on_customer_update


@api_view(['POST'])
def simulate_transaction(request):
    customer = Customer.objects.get(id=request.data['id'])

    customer.total_spent += 100
    customer.last_transaction_date = now()
    customer.save()

    on_customer_update(Customer, customer)

    return Response({"status": "ok"})