from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategorySerializer, SubCategorySerializer
from .models import Category, SubCategory
import jwt
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header


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
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/categories/{serializer.data[i]['id']}", "action": "GET", "types": ["application/json"]},
                {"rel": "subcategories", "href": f"/api/v1/categories/{serializer.data[i]['id']}/subcategories", "action": "GET", "types": ["application/json"]}
            ]

            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                token = auth[1]

                try:
                    id = decode_access_token(token)

                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/categories/{serializer.data[i]['id']}", "action": "PUT", "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/categories/{serializer.data[i]['id']}", "action": "DELETE", "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "subcategories", "href": f"/api/v1/categories/{serializer.data[i]['id']}/subcategories", "action": "POST", "types": ["application/json"]}
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
            {"rel": "self", "href": f"/api/v1/categories/{serializer.data['id']}", "action": "GET", "types": ["application/json"]},
            {"rel": "subcategories", "href": f"/api/v1/categories/{serializer.data['id']}/subcategories", "action": "GET", "types": ["application/json"]},
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
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, id):

        subcategories = SubCategory.objects.filter(categoryId=id)
        serializer = SubCategorySerializer(subcategories, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "GET", "types": ["application/json"]},
                {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}/products", "action": "GET", "types": ["application/json"]}
            ]

            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                token = auth[1]

                try:
                    id = decode_access_token(token)

                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "PUT", "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "DELETE", "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}/products", "action": "POST", "types": ["application/json"]}
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

        print(request.data)
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
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "GET", "types": ["application/json"]},
                {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}/products", "action": "GET", "types": ["application/json"]}
            ]

            auth = get_authorization_header(request).split()
            if auth and len(auth) == 2:
                token = auth[1]

                try:
                    id = decode_access_token(token)

                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "PUT", "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "self", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}", "action": "DELETE", "types": ["application/json"]}
                    )
                    serializer.data[i]['links'].append(
                        {"rel": "products", "href": f"/api/v1/subcategories/{serializer.data[i]['id']}/products", "action": "POST", "types": ["application/json"]}
                    )

                except Exception:
                    pass

        return JsonResponse(serializer.data, safe=False)