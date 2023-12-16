from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.models import User

from freelance.utils import IsNotFreelancerMixin, IsFreeLancerMixin
from users.models import Company

from .models import BoardThing, Topic, Task, ResponseToTask, GoodOrBadJob
from .forms import NewTaskForm, GiveResponseForm, SendReportForm, GiveLikeForm


class IndexPage(View):

	def get(self, request, *args, **kwargs):
		newest_board_thing = BoardThing.objects.order_by('-created')[:1]
		context = {
			'newest_board_thing': newest_board_thing
		}
		return render(request, 'index.html', context)


class TaskListPage(View):

	def get(self, request, *args, **kwargs):
		tasks = Task.objects.order_by('-created')
		context = {
			'tasks': tasks
		}
		return render(request, 'taks-list.html', context)


class NewTaskPage(LoginRequiredMixin, IsNotFreelancerMixin, CreateView):
	model = Task
	form_class = NewTaskForm
	template_name = 'new_task.html'
	success_url = reverse_lazy('index')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


@login_required
def response_to_task(request, pk):
	task = get_object_or_404(Task, pk=pk)
	user = request.user

	if user.my_profile.free_lancer_status != True:
		raise Http404('You are not a freelancer')
	else:
		if request.method == 'POST':
			form = GiveResponseForm(request.POST)
			if form.is_valid():
				new_response = form.save(commit=False)
				new_response.from_user = user
				new_response.to_task = task
				new_response.save()
				messages.info(request, 'Отклик успешно отправлен')
				return redirect('index')
		else:
			form = GiveResponseForm()
	
	return render(request, 'give_response.html', {'form': form})


def detail(request, task_id):
	task = get_object_or_404(Task, pk=task_id)
	context = {
		'task': task
	}
	return render(request, 'detail.html', context)


def board_detail(request, thing_id):
	b_thing = get_object_or_404(BoardThing, pk=thing_id)
	return render(request, 'b.html', {'b_thing': b_thing})


@login_required
def send_report_to_task_or_user(request, task_id):
	task = get_object_or_404(Task, pk=task_id)

	if (task.freelancer == request.user or task.user == request.user):
		if request.method == 'POST':
			form = SendReportForm(request.POST, request.FILES)
			if form.is_valid():
				new_report = form.save(commit=False)
				new_report.from_user = request.user
				new_report.task = task
				new_report.save()
				messages.info(request, 'Репорт успешно отправлен')
				return redirect('index')
		else:
			form = SendReportForm()
	else:
		raise Http404("You can't do it")
	
	context = {
		'form': form, 
		'task': task,
	}
	return render(request, 'send_report.html', context)


@login_required
def choice_your_freelancer(request, task_id, username):
	req_user = request.user
	user = get_object_or_404(User, username=username)
	task = get_object_or_404(Task, pk=task_id)
	#ckecks
	if req_user != task.user and user.my_profile.free_lancer_status != True:
		raise Http404('Не подходят по критериям')
	else:
		task.freelancer = user
		task.save()
		ResponseToTask.objects.filter(from_user=user, to_task=task).delete()

	return redirect(request.META.get('HTTP_REFERER'))


@login_required
def add_like_or_dislike_to_task(request, task_id):
	req_user = request.user
	task = get_object_or_404(Task, pk=task_id)

	if (req_user != task.user or req_user.my_profile.free_lancer_status == True):
		raise Http404('You can not leave a like or a dislike')
	else:
		current_likes_count = task.likes_count

		if request.method == 'POST':
			form = GiveLikeForm(request.POST)
			if form.is_valid():
				like = form.save(commit=False)
				like.user = req_user
				like.task = task
				if like.value == 'g':
					like.task.freelancer.my_profile.elo += 20
				else:
					like.task.freelancer.my_profile.elo -= 20
				like.task.freelancer.my_profile.save()
				like.save()
				task.likes_count = current_likes_count + 1
				task.finished_status = True
				task.save()
				return HttpResponseRedirect(reverse('detail', args=[task.pk]))
		else:
			form = GiveLikeForm()
		
		return render(request, 'give_like.html', {'form': form, 'task': task})


class ListResponsesPage(LoginRequiredMixin, IsNotFreelancerMixin, View):

	def get(self, request, *args, **kwargs):
		req_user = request.user
		responses = ResponseToTask.objects.filter(to_task__user=req_user)
		context = {
			'responses': responses
		}
		return render(request, 'responses.html', context)
