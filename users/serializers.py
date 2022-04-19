from rest_framework import serializers
from .utils import generate_key
from .models import User
import phonenumbers

import pyotp
import base64



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'name')

    def validate(self, attrs):
        try:
            my_number = phonenumbers.parse(attrs.get('phone'))
        except phonenumbers.phonenumberutil.NumberParseException:
            raise serializers.ValidationError('Invalid phone number')
        
        if not phonenumbers.is_valid_number(my_number):
            raise serializers.ValidationError('Invalid phone number')

        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class UserOtpSerializer(serializers.Serializer):
    
    otp = serializers.CharField(max_length=6, write_only=True)
    phone = serializers.CharField(max_length=13, write_only=True)

    class Meta:
        model = User
        fields = ('phone', 'otp')

    def validate(self, attrs):

        phone = attrs.get('phone')
        otp = attrs.get('otp')
        user = self.context.get('user')
        
        key = generate_key(phone)
        otp_obj = pyotp.HOTP(key)

        if not otp_obj.verify(otp, user.counter):
            raise serializers.ValidationError('Invalid OTP')

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','name', 'phone')
