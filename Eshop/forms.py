from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		for field in self.visible_fields():
			field.field.widget.attrs["class"] = "form-control"
	email = forms.CharField(required=True)
	phone_number = forms.CharField(required=True)
	name = forms.CharField(required=True)
	surname = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "phone_number","name", "surname", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user