from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Account


class SignupSerializer(serializers.ModelSerializer):
    """User signup serializer
    """
    email = serializers.EmailField(
            validators=[UniqueValidator(
                queryset=Account.objects.all(),
                message="This email is already exist!",
            )])

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = (
            'email',
            'first_name',
            'last_name',
            'birthdate',
            'gender',
            'contact',
            'address',
            'position',
            'job_title',
            'password',
        )

    def create(self, validated_data):
        account = Account(
                email=validated_data['email'],
                username=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                birthdate=validated_data['birthdate'],
                gender=validated_data['gender'],
                contact=validated_data['contact'],
                address=validated_data['address'],
                position=validated_data['position'],
                job_title=validated_data['job_title']
            )
        account.set_password(validated_data['password'])
        account.save()
        return account