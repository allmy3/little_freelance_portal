from django import forms

from .models import Task, ResponseToTask, Report, GoodOrBadJob


class NewTaskForm(forms.ModelForm):

    intro = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Краткое описание','class': 'auth_form__field top-three-three'}))

    class Meta:
        model = Task
        fields = ['intro', 'description', 'taks_topic']


class GiveResponseForm(forms.ModelForm):

    class Meta:
        model = ResponseToTask
        fields = ['text']


class SendReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['type', 'description', 'photo_proof']


class GiveLikeForm(forms.ModelForm):

    class Meta:
        model = GoodOrBadJob
        fields = ['value']