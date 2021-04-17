from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from github import Github

User = get_user_model()

class ApplicantLoginForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            user = None
            raise forms.ValidationError("Username Not Found")
        except:
            user = None
            pass
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            user = None
        if user is not None and not user.check_password(password):
            raise forms.ValidationError("Incorrect Password")
        elif user is None:
            pass
        else:
            return password
        
    def __init__(self, *args, **kwargs):
        super(ApplicantLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control','placeholder' : 'Username'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control','placeholder' : 'Password'})

class ApplicantRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(),label='Confirm Password')

    class Meta:
        model = User
        help_texts = {
            'username' : None,
        }
        fields = ['username','email']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('No Matching Passwords')
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_count = User.objects.filter(email=email).count()
        if email_count > 0:
            raise forms.ValidationError('E-Mail Already Registered')
        return email

    def save(self, commit=True):
        user = super(ApplicantRegistrationForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(ApplicantRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control','placeholder' : 'Username'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control','placeholder' : 'Email'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control','placeholder' : 'Password'})
        self.fields['confirm_password'].widget.attrs.update({'class' : 'form-control','placeholder' : 'Confirm Password'})

# class GithubUsernameForm(forms.Form):
#     username = forms.CharField()

#     def clean_username(self):
#         access_token = settings.GIT_API_TOKEN
#         g = Github(access_token)
#         try:
#             git_user = g.get_user(username)
#         except:
#             raise forms.ValidationError('No Github Username Found')
#         return username

#     def __init__(self, *args, **kwargs):
#         super(GithubUsernameForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'class' : 'form-control','placeholder' : 'Github Username'})