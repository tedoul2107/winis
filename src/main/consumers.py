from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer

from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, StockVariationSerializer
from .models import Category, SubCategory, Product, StockVariation


class ProductConsumer(GenericAsyncAPIConsumer):

    queryset = Product.objects.all()
    permission_classes = (permissions.AllowAny, )

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Product)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):

        data = ProductSerializer(instance=instance).data

        data['links'] = [
            {"rel": "self", "href": f"/api/v1/products/{data['id']}", "action": "GET",
             "types": ["application/json"]},
            {"rel": "stock_changes", "href": f"/api/v1/products/{data['id']}/stock_changes",
             "action": "GET", "types": ["application/json"]},
            {"rel": "self", "href": f"/api/v1/products/{data['id']}", "action": "PUT",
             "types": ["application/json"]},
            {"rel": "self", "href": f"/api/v1/products/{data['id']}", "action": "DELETE",
             "types": ["application/json"]},
            {"rel": "stock_changes", "href": f"/api/v1/products/{data['id']}/stock_changes",
             "action": "POST", "types": ["application/json"]}
        ]

        return dict(data=data, action=action.value)


class VariationConsumer(GenericAsyncAPIConsumer):

    queryset = StockVariation.objects.all()
    permission_classes = (permissions.AllowAny, )

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(StockVariation)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=StockVariationSerializer(instance=instance).data, action=action.value)


class SubCategoryConsumer(GenericAsyncAPIConsumer):

    queryset = SubCategory.objects.all()
    permission_classes = (permissions.AllowAny, )

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(SubCategory)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        data = SubCategorySerializer(instance=instance).data

        data['links'] = [
            {"rel": "self", "href": f"/api/v1/subcategories/{data['id']}", "action": "GET",
             "types": ["application/json"]},
            {"rel": "products", "href": f"/api/v1/subcategories/{data['id']}/products",
             "action": "GET", "types": ["application/json"]},
            {"rel": "self", "href": f"/api/v1/subcategories/{data['id']}", "action": "PUT",
             "types": ["application/json"]},
            {"rel": "self", "href": f"/api/v1/subcategories/{data['id']}", "action": "DELETE",
             "types": ["application/json"]},
            {"rel": "products", "href": f"/api/v1/subcategories/{data['id']}/products",
             "action": "POST", "types": ["application/json"]}
        ]

        return dict(data=data, action=action.value)


class CategoryConsumer(GenericAsyncAPIConsumer):

    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny, )

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Category)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):

        data = CategorySerializer(instance=instance).data

        data['links'] = [
            {"rel": "self", "href": f"/api/v1/categories/{data['id']}", "action": "GET",
             "types": ["application/json"]},
            {"rel": "subcategories", "href": f"/api/v1/categories/{data['id']}/subcategories",
             "action": "GET", "types": ["application/json"]},
            {"rel": "self", "href": f"/api/v1/categories/{data['id']}", "action": "PUT",
             "types": ["application/json"]},
            {"rel": "self", "href": f"/api/v1/categories/{data['id']}", "action": "DELETE",
             "types": ["application/json"]},
            {"rel": "subcategories", "href": f"/api/v1/categories/{data['id']}/subcategories",
             "action": "POST", "types": ["application/json"]}
        ]

        return dict(data=data, action=action.value)