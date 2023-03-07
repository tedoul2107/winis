from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, StockVariationSerializer
from .models import Category, SubCategory, Product, StockVariation
import jwt
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework import generics
from django.db.models import Sum, Count
from datetime import timedelta, datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')


class CategoryAPIView(APIView):

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/categories/{serializer.data[i]['id']}", "action": "GET",
                 "types": ["application/json"]},
                {"rel": "subcategories", "href": f"/api/v1/categories/{serializer.data[i]['id']}/subcategories",
                 "action": "GET", "types": ["application/json"]}
            ]

            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                token = auth[1]

                try:
                    id = decode_access_token(token)

                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/categories/{serializer.data[i]['id']}", "action": "PUT",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/categories/{serializer.data[i]['id']}", "action": "DELETE",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "subcategories", "href": f"/api/v1/categories/{serializer.data[i]['id']}/subcategories",
                         "action": "POST", "types": ["application/json"]}
                    )

                except Exception:
                    pass

        return JsonResponse(serializer.data, safe=False)


class ModifyCategoryAPIView(APIView):

    def get(self, request, id):

        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)

        user_dict = [serializer.data.copy(), ]
        user_dict[0]['links'] = [
            {"rel": "self", "href": f"/api/v1/categories/{serializer.data['id']}", "action": "GET",
             "types": ["application/json"]},
            {"rel": "subcategories", "href": f"/api/v1/categories/{serializer.data['id']}/subcategories",
             "action": "GET", "types": ["application/json"]},
        ]

        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1]

            try:
                id = decode_access_token(token)

                user_dict[0]['links'].append(
                    {"rel": "self", "href": f"/api/v1/categories/{serializer.data['id']}", "action": "PUT",
                     "types": ["application/json"]}
                )
                user_dict[0]['links'].append(
                    {"rel": "self", "href": f"/api/v1/categories/{serializer.data['id']}", "action": "DELETE",
                     "types": ["application/json"]}
                )
                user_dict[0]['links'].append(
                    {"rel": "subcategories", "href": f"/api/v1/categories/{serializer.data['id']}/subcategories",
                     "action": "POST", "types": ["application/json"]}
                )

            except Exception:
                pass

        return JsonResponse(user_dict, safe=False)

    def put(self, request, id):

        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, id):

        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubCategoryAPIView(APIView):

    def post(self, request, id):

        request.data['categoryId'] = id
        serializer = SubCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, id):

        subcategories = SubCategory.objects.filter(categoryId=id).order_by('name')
        serializer = SubCategorySerializer(subcategories, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "GET",
                 "types": ["application/json"]},
                {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}/products",
                 "action": "GET", "types": ["application/json"]}
            ]

            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                token = auth[1]

                try:
                    id = decode_access_token(token)

                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "PUT",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "DELETE",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}/products",
                         "action": "POST", "types": ["application/json"]}
                    )

                except Exception:
                    pass

        return JsonResponse(serializer.data, safe=False)


class ModifySubCatAPIView(APIView):

    def get(self, request, id):

        try:
            subcategory = SubCategory.objects.get(pk=id)
        except SubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SubCategorySerializer(subcategory)

        user_dict = [serializer.data.copy(), ]
        user_dict[0]['links'] = [
            {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data['id']}", "action": "GET",
             "types": ["application/json"]},
            {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data['id']}/products", "action": "GET",
             "types": ["application/json"]}
        ]

        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1]

            try:
                id = decode_access_token(token)

                user_dict[0]['links'].append(
                    {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data['id']}", "action": "PUT",
                     "types": ["application/json"]}
                )
                user_dict[0]['links'].append(
                    {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data['id']}", "action": "DELETE",
                     "types": ["application/json"]}
                )
                user_dict[0]['links'].append(
                    {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data['id']}/products",
                     "action": "POST", "types": ["application/json"]}
                )

            except Exception:
                pass

        return JsonResponse(user_dict, safe=False)

    def put(self, request, id):

        try:
            subcategory = SubCategory.objects.get(pk=id)
        except SubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data['categoryId'] = subcategory.categoryId.id

        serializer = SubCategorySerializer(subcategory, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_dict = [serializer.data.copy(), ]
        user_dict[0]['links'] = [
            {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data['id']}", "action": "GET",
             "types": ["application/json"]},
            {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data['id']}/products", "action": "GET",
             "types": ["application/json"]}
        ]

        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1]

            try:
                id = decode_access_token(token)

                user_dict[0]['links'].append(
                    {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data['id']}", "action": "PUT",
                     "types": ["application/json"]}
                )
                user_dict[0]['links'].append(
                    {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data['id']}", "action": "DELETE",
                     "types": ["application/json"]}
                )
                user_dict[0]['links'].append(
                    {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data['id']}/products",
                     "action": "POST", "types": ["application/json"]}
                )

            except Exception:
                pass

        return JsonResponse(user_dict, safe=False)

    def delete(self, request, id):

        try:
            subcategory = SubCategory.objects.get(pk=id)
        except SubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSubCatAPIView(APIView):

    def get(self, request):
        subcategories = SubCategory.objects.all().order_by('name')
        serializer = SubCategorySerializer(subcategories, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "GET",
                 "types": ["application/json"]},
                {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}/products",
                 "action": "GET", "types": ["application/json"]}
            ]

            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                token = auth[1]

                try:
                    id = decode_access_token(token)

                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "PUT",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "DELETE",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}/products",
                         "action": "POST", "types": ["application/json"]}
                    )

                except Exception:
                    pass

        return JsonResponse(serializer.data, safe=False)


class ProductPaginationAPIView(APIView):
    def get(self, request):

        products = Product.objects.all().order_by('model')

        try:
            limit = int(self.request.query_params.get('limit', 10))
            offset = int(self.request.query_params.get('offset', 1))
        except:
            limit = 10
            offset = 1

        paginator = Paginator(products, per_page=limit)
        products = paginator.get_page(offset)

        if offset > paginator.num_pages:
            return JsonResponse([], safe=False)

        # paginator = Paginator(products, per_page=int(request.data['num_items']))
        # page = int(request.data['page'])
        # products = paginator.get_page(page)

        serializer = ProductSerializer(products, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "GET",
                 "types": ["application/json"]},
                {"rel": "stock_changes", "href": f"/api/v1/products/{serializer.data[i]['id']}/stock_changes",
                 "action": "GET", "types": ["application/json"]}
            ]

            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                token = auth[1]

                try:
                    id = decode_access_token(token)

                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "PUT",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "DELETE",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "stock_changes", "href": f"/api/v1/products/{serializer.data[i]['id']}/stock_changes",
                         "action": "POST", "types": ["application/json"]}
                    )

                except Exception:
                    pass

        return JsonResponse(serializer.data, safe=False)


class ProductPaginationAPIView2(APIView):
    def get(self, request, id):
        products = Product.objects.filter(subcategoryId=id).order_by('model')

        try:
            limit = int(self.request.query_params.get('limit', 10))
            offset = int(self.request.query_params.get('offset', 1))
        except:
            limit = 10
            offset = 1

        paginator = Paginator(products, per_page=limit)
        products = paginator.get_page(offset)

        if offset > paginator.num_pages:
            return JsonResponse([], safe=False)

        # paginator = Paginator(products, per_page=int(request.data['num_items']))
        # page = int(request.data['page'])
        # products = paginator.get_page(page)

        serializer = ProductSerializer(products, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "GET",
                 "types": ["application/json"]},
                {"rel": "stock_changes", "href": f"/api/v1/products/{serializer.data[i]['id']}/stock_changes",
                 "action": "GET", "types": ["application/json"]}
            ]

            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                token = auth[1]

                try:
                    id = decode_access_token(token)

                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "PUT",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "DELETE",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "stock_changes", "href": f"/api/v1/products/{serializer.data[i]['id']}/stock_changes",
                         "action": "POST", "types": ["application/json"]}
                    )

                except Exception:
                    pass

        return JsonResponse(serializer.data, safe=False)


class ProductAPIView(APIView):

    def post(self, request, id):

        request.data['subcategoryId'] = id
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, id):

        products = Product.objects.filter(subcategoryId=id).order_by('model')
        serializer = ProductSerializer(products, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "GET",
                 "types": ["application/json"]},
                {"rel": "stock_changes", "href": f"/api/v1/products/{serializer.data[i]['id']}/stock_changes",
                 "action": "GET", "types": ["application/json"]}
            ]

            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                token = auth[1]

                try:
                    id = decode_access_token(token)

                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "PUT",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "DELETE",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "stock_changes", "href": f"/api/v1/products/{serializer.data[i]['id']}/stock_changes",
                         "action": "POST", "types": ["application/json"]}
                    )

                except Exception:
                    pass

        return JsonResponse(serializer.data, safe=False)


class ModifyProductAPIView(APIView):

    def get(self, request, id):

        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)

        user_dict = [serializer.data.copy(), ]
        user_dict[0]['links'] = [
            {"rel": "self", "href": f"/api/v1/products/{serializer.data['id']}", "action": "GET",
             "types": ["application/json"]},
            {"rel": "stock_changes", "href": f"/api/v1/products/{serializer.data['id']}/stock_changes",
             "action": "GET", "types": ["application/json"]}
        ]

        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1]

            try:
                id = decode_access_token(token)

                user_dict[0]['links'].append(
                    {"rel": "self", "href": f"/api/v1/products/{serializer.data['id']}", "action": "PUT",
                     "types": ["application/json"]}
                )
                user_dict[0]['links'].append(
                    {"rel": "self", "href": f"/api/v1/products/{serializer.data['id']}", "action": "DELETE",
                     "types": ["application/json"]}
                )
                user_dict[0]['links'].append(
                    {"rel": "stock_changes", "href": f"/api/v1/products/{serializer.data['id']}/stock_changes",
                     "action": "POST", "types": ["application/json"]}
                )

            except Exception:
                pass

        return JsonResponse(user_dict, safe=False)

    def put(self, request, id):

        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data._mutable = True

        request.data['subcategoryId'] = product.subcategoryId.id
        # print(request.data)
        serializer = ProductSerializer(product, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, id):

        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListProductAPIView(APIView):

    def get(self, request):
        products = Product.objects.all().order_by('model')
        serializer = ProductSerializer(products, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "GET",
                 "types": ["application/json"]},
                {"rel": "stock_changes", "href": f"/api/v1/products/{serializer.data[i]['id']}/stock_changes",
                 "action": "GET", "types": ["application/json"]}
            ]

            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                token = auth[1]

                try:
                    id = decode_access_token(token)

                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "PUT",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/products/{serializer.data[i]['id']}", "action": "DELETE",
                         "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "stock_changes", "href": f"/api/v1/products/{serializer.data[i]['id']}/stock_changes",
                         "action": "POST", "types": ["application/json"]}
                    )

                except Exception:
                    pass

        return JsonResponse(serializer.data, safe=False)


class StockCreationAPIView(APIView):
    def post(self, request, id):
        request.data['productId'] = id

        if request.data['type'] == 'PLUS':
            request.data['status'] = 'VALIDATED'

            try:
                product = Product.objects.get(pk=id)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            product.quantity += request.data['quantity']

            serializer_p = ProductSerializer(product, data={'quantity': product.quantity,
                                                            'subcategoryId': product.subcategoryId.id,
                                                            'model': product.model, 'color': product.color})
            serializer_p.is_valid(raise_exception=True)
            serializer_p.save()

        elif request.data['type'] == 'MINUS':
            request.data['status'] = 'PENDING'

        serializer = StockVariationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, id):
        stockchanges = StockVariation.objects.filter(productId=id).order_by('-datetime')
        serializer = StockVariationSerializer(stockchanges, many=True)
        return JsonResponse(serializer.data, safe=False)


class ListVariationAPIView(APIView):
    def get(self, request, id, status='pending'):
        stockchanges = StockVariation.objects.filter(productId=id).filter(status=status.upper()).order_by('-datetime')
        serializer = StockVariationSerializer(stockchanges, many=True)
        return JsonResponse(serializer.data, safe=False)


class ListVariationAPIView2(APIView):
    def get(self, request, status):
        stockchanges = StockVariation.objects.all().filter(status=status.upper()).order_by('-datetime')
        serializer = StockVariationSerializer(stockchanges, many=True)
        return JsonResponse(serializer.data, safe=False)


class ListVariationAPIView3(APIView):
    def get(self, request, userId, status='pending'):
        stockchanges = StockVariation.objects.all().filter(userId=userId).filter(status=status.upper()).order_by('-datetime')
        serializer = StockVariationSerializer(stockchanges, many=True)
        return JsonResponse(serializer.data, safe=False)


class ListVariationAPIView4(APIView):
    def get(self, request):
        stockchanges = StockVariation.objects.all().order_by('-datetime')
        serializer = StockVariationSerializer(stockchanges, many=True)
        return JsonResponse(serializer.data, safe=False)


class SellProductAPIView(APIView):
    def post(self, request, id):
        request.data['productId'] = id
        request.data['type'] = 'MINUS'
        request.data['status'] = 'PENDING'

        serializer = StockVariationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


class StockVariationAPIView(APIView):

    def get(self, request, id):

        try:
            stock_variation = StockVariation.objects.get(pk=id)
        except StockVariation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StockVariationSerializer(stock_variation)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, id):

        try:
            stock_variation = StockVariation.objects.get(pk=id)
        except StockVariation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # request.data._mutable = True
        request.data['productId'] = stock_variation.productId.id
        request.data['userId'] = stock_variation.userId.id
        request.data['quantity'] = stock_variation.quantity

        serializer = StockVariationSerializer(stock_variation, data=request.data)

        serializer.is_valid(raise_exception=True)

        if (
            request.data['status'] == 'VALIDATED'
            and stock_variation.type == 'MINUS'
            and stock_variation.status == 'PENDING'
        ):
            try:
                product = Product.objects.get(pk=stock_variation.productId.id)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.data['quantity'] > product.quantity:
                return JsonResponse({"message": "insufficient quantity"})
            product.quantity -= request.data['quantity']

            serializer_p = ProductSerializer(product, data={'quantity': product.quantity,
                                                                    'subcategoryId': product.subcategoryId.id,
                                                                    'model': product.model, 'color': product.color})
            serializer_p.is_valid(raise_exception=True)
            serializer_p.save()

        if (
                request.data['status'] == 'VALIDATED'
                and stock_variation.status == 'CANCELLED'
        ):
            return JsonResponse({"message": "This variation is already cancelled, you can't validated"})

        if (
                request.data['status'] == 'VALIDATED'
                and stock_variation.type == 'PLUS'
        ):
            return JsonResponse({"message": "This variation is already validated"})

        if (
                request.data['status'] == 'CANCELLED'
                and stock_variation.status == 'VALIDATED'
        ):
            return JsonResponse({"message": "This variation is already validated"})

        if (
                request.data['status'] == 'CANCELLED'
                and stock_variation.status == 'CANCELLED'
        ):
            return JsonResponse({"message": "This variation is already cancelled"})

        if (
                request.data['status'] == 'VALIDATED'
                and stock_variation.status == 'VALIDATED'
        ):
            return JsonResponse({"message": "This variation is already validated"})

        if (
                request.data['status'] == 'PENDING'
        ):
            return JsonResponse({"message": "This operation is unauthorized"})

        serializer.save()

        return JsonResponse(serializer.data, safe=False)


class FilterProductAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):

        products = Product.objects.all()

        diameter = self.request.query_params.get('diameter', 14.5)
        n_tone = self.request.query_params.get('n_tone', 3)
        cycle_period = self.request.query_params.get('cycle_period', 'Yearly')

        products = products.filter(subcategoryId_id__categoryId_id__diameter=diameter).filter(subcategoryId_id__n_tone=n_tone)\
            .filter(subcategoryId_id__cycle_period=cycle_period)

        return products


class SearchProductAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):

        products = Product.objects.all()

        keyword = self.request.query_params.get('keyword', 'FreshTone Natural')

        products = products.filter(subcategoryId_id__name__icontains=keyword)

        return products


class StatAPIView(APIView):

    def get_total_lens(self):
        try:
            total = Product.objects.all().aggregate(Sum('quantity'))
        except:
            total = 0

        return total

    def get_total_sales(self):

        try:
            total = (StockVariation.objects.filter(status='VALIDATED')
                  .values('type')
                  .annotate(dcount=Sum('quantity'))
                  .order_by()
                  )
        except:
            total = 0
        return total

    def get_week_sales(self):

        try:
            total = (StockVariation.objects.filter(status='VALIDATED')
                     .filter(datetime__gte=datetime.now()-timedelta(days=7))
                 .values('type')
                 .annotate(dcount=Sum('quantity'))
                 .order_by()
                 )
        except Exception:
            total = 0
        return total

    def get(self, request):

        total_lens = self.get_total_lens()
        total_sales = self.get_total_sales()
        week_sales = self.get_week_sales()

        if len(week_sales) > 0:
            try:
                week_sales = week_sales[0]['dcount']
            except Exception:
                week_sales = 0
        else:
            week_sales = 0

        try:
            total_sales = total_sales[0]['dcount']
        except Exception:
            total_sales = 0

        try:
            total_lens = total_lens['quantity__sum']
        except Exception:
            total_lens = 0

        # print(total_sales)
        # print(total_lens)
        # print(week_sales)

        return JsonResponse({"total_lens": total_lens, "total_sales": total_sales, "week_sales": week_sales}, safe=False, status=status.HTTP_200_OK)
