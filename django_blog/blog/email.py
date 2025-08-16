from django import forms
from django.contrib.auth.forms import UserCreationForm

class EmailAddForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
