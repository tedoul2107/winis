from django.urls import path
from .views import CategoryAPIView, ModifyCategoryAPIView, SubCategoryAPIView, ModifySubCatAPIView, ListSubCatAPIView

urlpatterns = [
    path('categories', CategoryAPIView.as_view()),
    path('categories/<int:id>', ModifyCategoryAPIView.as_view()),
    path('categories/<int:id>/subcategories', SubCategoryAPIView.as_view()),
    path('subcategories/<int:id>', ModifySubCatAPIView.as_view()),
    path('subcategories', ListSubCatAPIView.as_view()),

]
