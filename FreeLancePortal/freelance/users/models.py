from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Company(models.Model):
	employees = models.ManyToManyField(User, blank=True)
	nameing = models.CharField(max_length=255)
	description = models.TextField()
	users_who_can_add_members = models.ManyToManyField(User, blank=True, related_name='can_add_mem')

	def __str__(self):
		return self.nameing


class Profile(models.Model):
	owner_user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Owner", related_name='my_profile')
	free_lancer_status = models.BooleanField(default=False)
	rate_as_freelancer = models.PositiveIntegerField(default=0)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companys', blank=True, null=True)
	elo = models.PositiveIntegerField(default=0)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

	def __str__(self):
		return self.owner_user.username
	
	def get_absolute_url(self):
		return reverse('profile', args=[self.owner_user.username])


class Rate(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	description_for_rate_report = models.TextField("Description for the rate report")
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rates')
	number_of_value = models.ForeignKey('Value', on_delete=models.CASCADE)
	number_of_value_v = models.FloatField(blank=True, null=True)

	def __str__(self):
		return self.user.username + " " + self.profile.owner_user.username


class Value(models.Model):
	number = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return str(self.number)


class ResponseToCompany(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE)
	to_company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='responses')
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.from_user.username + " " + self.text + " " + self.to_company.nameing

	class Meta:
		ordering = ['-created']