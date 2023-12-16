from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

from users.models import Profile

User = get_user_model()


class Topic(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	slug = models.SlugField()

	def __str__(self):
		return self.name


class BoardThing(models.Model):
	intro = models.CharField(max_length=50)
	description = models.TextField()
	slug = models.SlugField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.intro


class Task(models.Model):
	intro = models.CharField(max_length=255)
	description = RichTextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	taks_topic = models.ManyToManyField(Topic, blank=True)
	responsible_people_count = models.PositiveIntegerField(default=0)
	slug = models.SlugField(blank=True, null=True)
	freelancer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='my_order')
	finished_status = models.BooleanField(default=False)
	likes_count = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.intro


class GoodOrBadJob(models.Model):
	VALUE_CHOICES = (
		('g', 'Good'),
		('b', 'Bad'),
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
	value = models.CharField(choices=VALUE_CHOICES, max_length=1)

	def __str__(self):
		return 'From ' + self.user.username + " to " + self.task.intro


class Report(models.Model):
	TYPES_OF_REPORTS_CHOICES = (
		('ff', 'fraud from freelancer'),
		('fc', 'fraud from customer'),
		('ot', 'Other reason'),
	)

	from_user = models.ForeignKey(User, on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_to_user', blank=True, null=True)
	type = models.CharField(max_length=2, choices=TYPES_OF_REPORTS_CHOICES)
	description = models.TextField()
	continued = models.BooleanField(default=False)
	photo_proof = models.ImageField(upload_to='proofs/', blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name='reports_to_task')

	def __str__(self):
		return f"Report from {self.from_user.username} to {self.task.intro}"


class ResponseToTask(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE)
	to_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='responses')
	text = RichTextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.from_user.username + " " + self.to_task.intro