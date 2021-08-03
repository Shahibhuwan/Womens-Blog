from django.db.models import fields
from blog.models import Customer, Post, Profile, Contact

from django.contrib.auth.models import User
from django import forms


class UserRegistration(forms.ModelForm):
    username =forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'}))
    email = forms.EmailField( label="Please enter your email address",widget=forms.EmailInput(attrs={
        'class': 'form-control'}))
    rpassword=forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'}))
    class Meta:
        model=Customer
        fields=['username','email','rpassword','password','full_name']
        widgets = {'full_name': forms.TextInput(attrs={'class': 'form-control'})}
    #,'image','phone','profession' ,'currently_working'
    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(" Customer with this user name is already exists.")
        return uname

    def clean_password(self):
        rpassword = self.cleaned_data["rpassword"]
        password =self.cleaned_data['password']
        if password != rpassword:
            raise forms.ValidationError(" password didnot match")

        return password
    
    

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','description','category','image']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows' :'3'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),}
#postgre
class LoginForm(forms.Form):
    username= forms.CharField(widget= forms.TextInput(attrs={
        'class': 'form-control'}))
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'class': 'form-control'}))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields=['description','secondary_email','image','phone','profession','currently_working','experience','hourtly_rate','total_projects','english_level','availability']

class ContactForm(forms.ModelForm):
    class Meta:
        model= Contact
        fields =['name','email','message']

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'}))        
# widgets handle rendering of html 

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password")
    
    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password


# class SubscribeForm(forms.Form):
#     email = forms.CharField(widget=forms.PasswordInput())

    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     if User.objects.filter(email=email).exists:
    #         pass
    #     else:
    #         raise forms.ValidationError("User does not exist in our website . Please Register first ")

        
    #     return email
    

