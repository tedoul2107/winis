from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, AuthenticationFailed
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token


class RegisterAPIView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        for i in range(len(serializer.data)):
            serializer.data[i]['links'] = [
                {"rel": "self", "href": f"/api/v1/users/{serializer.data[i]['id']}", "action": "GET", "types": ["application/json"]},
                {"rel": "self", "href": f"/api/v1/users/{serializer.data[i]['id']}", "action": "PUT", "types": ["application/json"]},
                {"rel": "self", "href": f"/api/v1/users/{serializer.data[i]['id']}", "action": "DELETE","types": ["application/json"]},
            ]

        return JsonResponse(serializer.data, safe=False)


class LoginAPIView(APIView):

    def post(self, request):
        user = User.objects.filter(username=request.data['username']).first()

        if not user:
            raise APIException('Invalid credentials!')

        if not user.check_password(request.data['password']):
            raise APIException('Invalid credentials!')

        # serializer = UserSerializer(user)
        # return Response(serializer.data)

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)
        response.data = {
            "token": access_token
        }

        return response


class UserAPIView(APIView):

    def get(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1]
            id = decode_access_token(token)

            user = User.objects.filter(pk=id).first()
            serializer = UserSerializer(user, many=False)

            user_dict = serializer.data.copy()

            user_dict['links'] = [
                {"rel": "self", "href": f"/api/v1/users/{serializer.data['id']}", "action": "GET", "types": ["application/json"]},
                {"rel": "self", "href": f"/api/v1/users/{serializer.data['id']}", "action": "PUT", "types": ["application/json"]},
                {"rel": "self", "href": f"/api/v1/users/{serializer.data['id']}", "action": "DELETE", "types": ["application/json"]},
            ]

            return JsonResponse(user_dict, safe=False)

        raise AuthenticationFailed('unauthenticated')


class RefreshAPIView(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)

        return Response({
            'token': access_token
        })


class LogoutAPIView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie(key='refreshToken')
        response.data = {
            'message': 'success'
        }
        return response


class UserDetailAPIView(APIView):

    def get(self, request, id):

        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)

        user_dict = serializer.data.copy()
        user_dict['links'] = [
            {"rel": "self", "href": f"/api/v1/users/{serializer.data['id']}", "action": "GET",
             "types": ["application/json"]},
            {"rel": "self", "href": f"/api/v1/users/{serializer.data['id']}", "action": "PUT",
             "types": ["application/json"]},
            {"rel": "self", "href": f"/api/v1/users/{serializer.data['id']}", "action": "DELETE",
             "types": ["application/json"]},
        ]

        return JsonResponse(user_dict, safe=False)

    def put(self, request, id):

        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_dict = serializer.data.copy()
        user_dict['links'] = [
            {"rel": "self", "href": f"/api/v1/users/{serializer.data['id']}", "action": "GET",
             "types": ["application/json"]},
            {"rel": "self", "href": f"/api/v1/users/{serializer.data['id']}", "action": "PUT",
             "types": ["application/json"]},
            {"rel": "self", "href": f"/api/v1/users/{serializer.data['id']}", "action": "DELETE",
             "types": ["application/json"]},
        ]

        return JsonResponse(user_dict, safe=False)

    def delete(self, request, id):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
