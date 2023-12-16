from django.urls import path

from .views import (
	IndexPage,TaskListPage,NewTaskPage,ListResponsesPage,
	response_to_task,detail,board_detail,send_report_to_task_or_user,
	choice_your_freelancer,add_like_or_dislike_to_task
)

urlpatterns = [
	path('', IndexPage.as_view(), name='index'),
	path('detail-task-<int:task_id>/', detail, name='detail'),
	path('task-list/', TaskListPage.as_view(), name='task_list'),
	path('board-thing-detail-<int:thing_id>/', board_detail, name='board_detail'),
	path('new-task-creation/', NewTaskPage.as_view(), name='new_task'),
	path('response-to-task-<int:pk>/', response_to_task, name='give_response'),
	path('send-report-<int:task_id>/',send_report_to_task_or_user,name='send_report'),
	path('choice-your-freelancer/<int:task_id>/<username>/', choice_your_freelancer, name='choice_freelancer'),
	path('like-dislike-to-<int:task_id>/',add_like_or_dislike_to_task,name='like_to'),
	path('all-responses-to-your-tasks-orders/',ListResponsesPage.as_view(), name='all_res'),
]