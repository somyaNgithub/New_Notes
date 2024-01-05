from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password



class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Set write_only to True for password field
    
    class Meta:
        model = CustomUser
        fields =['U_id','userName','password']
    
    def create(self, validated_data):
        # Hash the password before saving it to the database
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class CustomUtilsUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields =[ 'U_id','userName']