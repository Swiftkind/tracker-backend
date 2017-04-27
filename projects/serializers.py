from rest_framework import serializers

from accounts.models import Account

from .models import (
                    Company,
                    Project,
                    ProjectMember,
                    Log
                )

class CompanySerializer(serializers.ModelSerializer):
    """Render company data
    """

    class Meta:
        model = Company
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    """Render project data
    """

    class Meta:
        model = Project
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    """Render account data
    """

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'email', 'profile_photo')


class ProjectMemberSerializer(serializers.ModelSerializer):
    """Render member data
    """
    member = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()

    def get_member(self, instance):
        return AccountSerializer(instance.account).data

    def get_profile_photo(self, instance):
        request = self.context.get('request')
        user = self.get_member(instance)
        photo = user.get('profile_photo')
        if not photo:
            return None
        return request.build_absolute_uri(photo)

    class Meta:
        model = ProjectMember
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    """Render log data
    """

    seconds = serializers.CharField()
    project = serializers.IntegerField(source='member.project.id')

    class Meta:
        model = Log
        fields = '__all__'


class MemberLogSerializer(serializers.ModelSerializer):
    """Render log data
    """
    log_field = serializers.CharField(source='log')
    member = ProjectMemberSerializer()

    class Meta:
        model = Log
        fields = '__all__'
