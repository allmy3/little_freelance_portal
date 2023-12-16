from django.contrib import admin

from .models import Topic, BoardThing, Task, Report, GoodOrBadJob, ResponseToTask

admin.site.register(Topic)
admin.site.register(BoardThing)
admin.site.register(Task)
admin.site.register(Report)
admin.site.register(GoodOrBadJob)
admin.site.register(ResponseToTask)