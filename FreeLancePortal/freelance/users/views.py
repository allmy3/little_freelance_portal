from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.db.models import Avg
from django.contrib.auth import update_session_auth_hash

from freelance.utils import UserIsNotAuthMixin, IsFreeLancerMixin

from .models import Profile, Rate, Value, Company
from .forms import LoginForm, RegisterForm, ChangeProfileForm, GiveRateForm, ChangeUserPasswordForm, SendResComForm

User = get_user_model()


class LoginPage(UserIsNotAuthMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        return render(request, 'users/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
        context = {
            'form': form
        }
        return render(request, 'users/login.html', context)


class RegisterPage(UserIsNotAuthMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return redirect('login')
        context = {
            'form': form
        }
        return render(request, 'users/register.html', {'form': form})


class LogoutPage(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    rate_status = None
    # Rate response exists check
    if Rate.objects.filter(user=request.user, profile=profile_user.my_profile).exists():
        rate_status = True
    else:
        rate_status = False
    # Average rate value calculating
    profile_freelancer_rate_avg = Rate.objects.filter(profile=profile_user.my_profile).aggregate(Avg('number_of_value'))

    context = {
        'profile_user': profile_user,
        'rate_status': rate_status,
        'profile_freelancer_rate_avg': profile_freelancer_rate_avg
    }
    return render(request, 'users/profile.html', context)


class ChangeProfilePage(LoginRequiredMixin, UpdateView):
    template_name = 'users/change_profile.html'
    form_class = ChangeProfileForm
    model = Profile
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.my_profile
    

@login_required
def give_rate(request, username):
    req_user = request.user
    profile = get_object_or_404(Profile, owner_user__username=username)

    if Rate.objects.filter(user=req_user, profile=profile).exists():
        raise Http404('Вы уже оставили отзыв')
    else:
        if request.method == 'POST':
            form = GiveRateForm(request.POST)
            if form.is_valid():
                new_rate_res = form.save(commit=False)
                new_rate_res.user = req_user
                new_rate_res.profile = profile
                new_rate_res.save()
                return HttpResponseRedirect(reverse('profile', args=[profile.owner_user.username]))
        else:
            form = GiveRateForm()
        
        return render(request, 'users/give_rate.html', {'form': form, 'profile': profile})


# One more auth logic
@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = ChangeUserPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('index')
    else:
        form = ChangeUserPasswordForm(instance=user)

    return render(request, 'users/change_password.html', {'form': form})


class CompanyListView(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		companies = Company.objects.all()
		return render(request, 'users/companies.html', {'companies': companies})


@login_required
def send_res_com(request, pk):
    company = get_object_or_404(Company, pk=pk)
    user = request.user

    if request.method == 'POST':
        form = SendResComForm(request.POST)
        if form.is_valid():
            new_res = form.save(commit=False)
            new_res.from_user = user
            new_res.to_company = company
            new_res.save()
            return redirect('companies')
    else:
        form = SendResComForm()
    
    return render(request, 'users/send_res.html', {'form': form})