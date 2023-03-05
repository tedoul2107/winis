from django.urls import path
from .consumers import ProductConsumer, VariationConsumer

# from .views import StatAPIView

ws_urlpatterns = [
    path('ws/product', ProductConsumer.as_asgi()),
    path('ws/variation', VariationConsumer.as_asgi()),
]