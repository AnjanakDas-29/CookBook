from .models import Recipe,UserProfile

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

from rest_framework import serializers
    



class RecipeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipe
        fields ='__all__'
        

    
        extra_kwargs ={
            'title':{  
                'error_messages':{
                    'blank':'Recipe title cannot be empty',
                    'max_length' :'Title cannot exceed 200 characters'
                }
                
            },
            'instructions':{
                'error_messages':{
                    'blank':'Instruction cannot be empty'
                }    
            }
            
            }
        

    def validate_ingredients(self,value):
        if not value or len(value)==0:
            raise serializers.ValidationError("Alteast one ingredient is required")
        return value         
        
    

class UserSerializer(serializers.ModelSerializer):
    User = get_user_model()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    #created_by = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = UserProfile
        fields = ["id", "username","role", "email", "first_name", "last_name", "date_joined", "password","gender"]
        read_only_fields = ["id", "date_joined"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")

        
        if request and request.method in ["PATCH", "PUT"]:
            self.fields["username"].required = False
            self.fields["password"].required = False
        else:
            self.fields["password"].required = True
            self.fields["username"].required = True

    def validate_email(self, value):
        validate_email(value)
        if UserProfile.objects.filter(email__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Email must be unique.")
        return value

    def create(self, validated_data):
      user = UserProfile.objects.create_user(**validated_data)
      return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password =serializers.CharField()


    

    def validate(self,data):
            user = authenticate(**data)
            if user and user.is_active:
                return {"user": user}
            raise serializers.ValidationError("Incorrect Credentials")