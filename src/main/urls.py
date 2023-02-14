from django.urls import path, re_path
from .views import CategoryAPIView, ModifyCategoryAPIView, SubCategoryAPIView, ModifySubCatAPIView, ListSubCatAPIView, \
    ProductAPIView, ModifyProductAPIView, ListProductAPIView, StockVariationAPIView, SearchProductAPIView, StatAPIView

urlpatterns = [
    path('categories', CategoryAPIView.as_view()),
    path('categories/<int:id>', ModifyCategoryAPIView.as_view()),
    path('categories/<int:id>/subcategories', SubCategoryAPIView.as_view()),
    path('subcategories/<int:id>', ModifySubCatAPIView.as_view()),
    path('subcategories', ListSubCatAPIView.as_view()),
    path('subcategories/<int:id>/products', ProductAPIView.as_view()),
    path('products/<int:id>', ModifyProductAPIView.as_view()),
    path('products', ListProductAPIView.as_view()),
    path('products/<int:id>/stock_changes', StockVariationAPIView.as_view()),
    re_path('products/filter', SearchProductAPIView.as_view()),
    path('stats', StatAPIView.as_view())

]
