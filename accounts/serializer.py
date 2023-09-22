from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.encoding import smart_str, smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings

from .utils import get_unique_code

from .models import Profile



User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()        # email usermodel modelinden geldiyi ucun avtomatik ozu yenisini yaratmaga calisir buna gore burda fieldi yeniden ozumuz yenisini yaradiriq
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }


    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        return authenticate(email=email, password=password)
    

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token)
        }
        return repr_
    



class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True}
        }


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password").strip()
        confirm_password = attrs.get("confirm_password").strip()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "this username alredy exits"})
        
        if len(password) < 6:
            raise serializers.ValidationError({"error":"Sifrenin uzunlugu 6 olmalidir"})

        if not any(i.isdigit() for i in password):
            raise serializers.ValidationError({"error": "Sifrenin icinde en az bir reqem olamidir"})
        
        if password != confirm_password:
            raise serializers.ValidationError({"error": "Sifreler bir biriyle uygun deyil"})

        return attrs
    


    def create(self, validated_data):
        confirm_password = validated_data.pop("confirm_password")
        password = validated_data.get("password")


        user = User.objects.create(
            **validated_data, is_active=False
        )

        user.set_password(password)
        user.save()

        user.profile.activation_code = get_unique_code(size=6, model_=Profile)
        user.profile.save()

        send_mail(
                "Activation",
                f"Your code: {user.profile.activation_code}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently = False
        )

        return user
    

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["uuid"] = urlsafe_base64_encode(smart_bytes(instance.id))
        return repr_
    



class ActivationSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("code",)
        
    
    def validate(self, attrs):
        user = self.context.get("user")
        code = attrs.get("code").strip()
    

        if str(code) != str(user.profile.activation_code):
            raise serializers.ValidationError({"error": "Wrong code"})
        

        return attrs
    


    def create(self, validated_data):
        user = self.context.get("user")
        user.is_active = True
        user.save()

        user.profile.activation_code = None
        user.profile.save()
        
        return user
    

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["email"] = instance.email

        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token), "access": str(token.access_token)
        }
        return repr_