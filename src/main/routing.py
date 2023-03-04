from django.urls import path
from .consumers import ProductConsumer

# from .views import StatAPIView

ws_urlpatterns = [
    path('ws/product', ProductConsumer.as_asgi()),

]