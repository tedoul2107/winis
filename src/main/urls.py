from django.urls import path, re_path
from .views import CategoryAPIView, ModifyCategoryAPIView, SubCategoryAPIView, ModifySubCatAPIView, ListSubCatAPIView, \
    ProductAPIView, ModifyProductAPIView, ListProductAPIView, StockVariationAPIView, \
    SearchProductAPIView, StatAPIView, FilterProductAPIView, ProductPaginationAPIView, ProductPaginationAPIView2, \
    StockCreationAPIView, SellProductAPIView, ListVariationAPIView, ListVariationAPIView2, ListVariationAPIView3

urlpatterns = [
    path('categories', CategoryAPIView.as_view()),
    path('categories/<int:id>', ModifyCategoryAPIView.as_view()),
    path('categories/<int:id>/subcategories', SubCategoryAPIView.as_view()),
    path('subcategories/<int:id>', ModifySubCatAPIView.as_view()),
    path('subcategories', ListSubCatAPIView.as_view()),
    path('subcategories/<int:id>/products', ProductAPIView.as_view()),
    path('products/<int:id>', ModifyProductAPIView.as_view()),
    path('products', ListProductAPIView.as_view()),

    # path('products/<int:id>/stock_changes', StockVariationAPIView.as_view()),
    path('products/<int:id>/sell', SellProductAPIView.as_view()),
    path('products/<int:id>/stock_changes', StockCreationAPIView.as_view()),
    path('stock_changes/<int:id>', StockVariationAPIView.as_view()),
    path('products/<int:id>/stock_changes/<str:status>', ListVariationAPIView.as_view()),
    path('stock_changes/<str:status>', ListVariationAPIView2.as_view()),
    path('stock_changes/<int:userId>/<str:status>', ListVariationAPIView3.as_view()),

    re_path('products/filter', FilterProductAPIView.as_view()),
    re_path('products/search', SearchProductAPIView.as_view()),
    path('stats', StatAPIView.as_view()),

    path('products/pagination', ProductPaginationAPIView.as_view()),
    path('subcategories/<int:id>/products/pagination', ProductPaginationAPIView2.as_view())
]
