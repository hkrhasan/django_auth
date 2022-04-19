from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from users.models import User
from users.renderers import UserRenderer
from users.serializers import UserOtpSerializer, UserProfileSerializer, UserRegistrationSerializer
import pyotp
from .utils import generate_key, get_tokens_for_user, send_otp
from django.contrib.auth import authenticate


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        
        try:
            user = User.objects.get(phone=request.data.get('phone'))
        except ObjectDoesNotExist:
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(**serializer.validated_data)

        user.counter += 1
        user.save()

        key = generate_key(user.phone)
        otp = pyotp.HOTP(key)

        try:
            send_otp(user.phone, otp.at(user.counter))
        except Exception as e:
            print(e)
            return Response({'errors': {"phone": ["Could not send OTP"]}}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'OTP sent successfully', 'otp': otp.at(user.counter)}, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        renderer_classes = [UserRenderer]

        try:
            user = User.objects.get(phone=request.data.get('phone'))
        except ObjectDoesNotExist:
            return Response({'errors': {"phone": ["User does not exist"]}}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserOtpSerializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        
        token = get_tokens_for_user(user)

        return Response({'message': 'login successful', 'token': token}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

