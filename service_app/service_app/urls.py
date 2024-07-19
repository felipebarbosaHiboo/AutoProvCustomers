from django.urls import path
from .views import customer, get_additional_fields

urlpatterns = [
    path('customer/', customer, name='customer'),
    path('get-additional-fields/', get_additional_fields, name='get_additional_fields'),
]
