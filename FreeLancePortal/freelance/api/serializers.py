from email.policy import default
from rest_framework import serializers

from django.contrib.auth import get_user_model

from users.models import Company, Profile, Rate, Value, ResponseToCompany
from tasks.models import Topic, BoardThing, Task, GoodOrBadJob, Report, ResponseToTask

User = get_user_model()


# USERS SERIALIZERS
class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['nameing', 'description']


class ProfileSerializer(serializers.ModelSerializer):

    owner_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    company = serializers.SlugRelatedField(read_only=True, slug_field='nameing')

    class Meta:
        model = Profile
        fields = ['owner_user', 'company', 'free_lancer_status', 'elo']


class RateSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    profile = serializers.SlugRelatedField(read_only=True, slug_field='pk')
    number_of_value = serializers.SlugRelatedField(read_only=True, slug_field='number')

    class Meta:
        model = Rate
        fields = ['user', 'description_for_rate_report', 'profile', 'number_of_value']


class ResponseToCompanySerializer(serializers.ModelSerializer):

    from_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    to_company = serializers.SlugRelatedField(read_only=True, slug_field='nameing')

    class Meta:
        model = ResponseToCompany
        fields = ['from_user', 'to_company', 'text', 'created']


# Tasks serializers
class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['name', 'description', 'slug']


class BoardThingSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoardThing
        fields = ['intro', 'description', 'slug', 'created']


class TaskSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    taks_topic = serializers.SlugRelatedField(read_only=True, slug_field='name')
    freelancer = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Task
        fields = ['pk','intro','description','created','user','taks_topic','responsible_people_count','freelancer','finished_status','likes_count']


class GorBSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    task = serializers.SlugRelatedField(read_only=True, slug_field='intro')

    class Meta:
        model = GoodOrBadJob
        fields = ['user', 'task', 'value']


class ReportSerializer(serializers.ModelSerializer):

    from_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    to_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    task = serializers.SlugRelatedField(read_only=True, slug_field='intro')

    class Meta:
        model = Report
        fields = ['from_user', 'to_user','type','description','continued','created','task']


class ResponseToTaskSerializer(serializers.ModelSerializer):

    from_user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    to_task = serializers.SlugRelatedField(read_only=True, slug_field='intro')

    class Meta:
        model = ResponseToTask
        fields = ['from_user','to_task','text','created']