from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework import permissions

from users.models import Company, Profile, Rate, Value, ResponseToCompany
from tasks.models import Topic, BoardThing, Task, GoodOrBadJob, Report, ResponseToTask
from .serializers import *


class CompanyListView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyDetailView(RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class RatesListView(ListAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticated]


class RatesDetailView(RetrieveAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResponsesToCompanyListView(ListAPIView):
    queryset = ResponseToCompany.objects.all()
    serializer_class = ResponseToCompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class ResponsesToCompanyDetailView(RetrieveAPIView):
    queryset = ResponseToCompany.objects.all()
    serializer_class = ResponseToCompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class TopicListView(ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]


class TopicCreateView(CreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAdminUser]


class BoardThingListView(ListAPIView):
    queryset = BoardThing.objects.all()
    serializer_class = BoardThingSerializer
    permission_classes = [permissions.IsAuthenticated]


class BoardThingCreateView(CreateAPIView):
    queryset = BoardThing.objects.all()
    serializer_class = BoardThingSerializer
    permission_classes = [permissions.IsAdminUser]


class TaskListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class GorBListView(ListAPIView):
    queryset = GoodOrBadJob.objects.all()
    serializer_class = GorBSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportListView(ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportDetailView(RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResponseToTaskListView(ListAPIView):
    queryset = ResponseToTask.objects.all()
    serializer_class = ResponseToTaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResponseToTaskDetailView(RetrieveAPIView):
    queryset = ResponseToTask.objects.all()
    serializer_class = ResponseToTaskSerializer
    permission_classes = [permissions.IsAuthenticated]