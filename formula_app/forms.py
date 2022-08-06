from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	# def save(self, commit=True):
	# 	user = super(NewUserForm, self).save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 	return user

	class Meta:
		model = User
		fields=['username','password1','password2']
		widgets = {
			'username': forms.TextInput(attrs={'class':'form-control'}),
		}