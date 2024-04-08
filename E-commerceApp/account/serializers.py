from rest_framework import serializers
from django.contrib.auth.models import User




class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'password')

        extra_kwargs = {
            'first_name': {'required':True ,'allow_blank':False},
            'last_name' : {'required':True ,'allow_blank':False},
            'email' : {'required':True ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False,'min_length':8}
        }



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'username') 







# SignUpSerializer is tailored for creating new users, with additional constraints on required fields and password length.
# UserSerializer more general-purpose serializer for displaying user information, likely used in scenarios where you're retrieving or updating user details but not necessarily creating new users