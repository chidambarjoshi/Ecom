from django import forms
from django.forms import widgets
from com.models import Users

class UsersForm(forms.ModelForm):
    """Form definition for Users."""
    class Meta:
        """Meta definition for Usersform."""
        model = Users
        fields = ('email','first_name','last_name','gender','dob','phone','photo','password','password2')
        widgets={
            'dob': forms.DateInput(
                attrs={'class': "form-control",
                       'type': 'date',
                       'required':'required'}),
        }
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        email_qs = Users.objects.filter(email=email)
        phone_qs = Users.objects.filter(phone=phone)
        con_password=self.cleaned_data.get('password2')
        password=self.cleaned_data.get('password')
        if password!=con_password:
            raise forms.ValidationError("Password and Confirm Password does not match")
        if email_qs.exists():
            raise forms.ValidationError("This Email is already registerd")
        if phone_qs.exists():
            raise forms.ValidationError("This Mobile number is already registerd")
        return super(UsersForm, self).clean(*args, **kwargs)