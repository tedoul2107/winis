from .models import Product

from .serializers import ProductSerializer

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework import permissions


class ProductConsumer(GenericAsyncAPIConsumer):

    queryset = Product.objects.all()
    permission_classes = (permissions.AllowAny, )

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

        # await self.accept()

    @model_observer(Product)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=ProductSerializer(instance=instance).data, action=action.value)
