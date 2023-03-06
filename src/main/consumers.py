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
        return dict(data=ProductSerializer(instance=instance).data, action=action.value)


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
        return dict(data=SubCategorySerializer(instance=instance).data, action=action.value)


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
        return dict(data=CategorySerializer(instance=instance).data, action=action.value)