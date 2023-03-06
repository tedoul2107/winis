from django.urls import path
from .consumers import ProductConsumer, VariationConsumer, SubCategoryConsumer, CategoryConsumer

# from .views import StatAPIView

ws_urlpatterns = [
    path('ws/product', ProductConsumer.as_asgi()),
    path('ws/variation', VariationConsumer.as_asgi()),
    path('ws/subcategory', SubCategoryConsumer.as_asgi()),
    path('ws/category', CategoryConsumer.as_asgi()),

]