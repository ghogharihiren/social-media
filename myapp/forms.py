from django import forms
from .models import*
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),
    )
    class Meta:
        model=User
        fields=['first_name','last_name','username','email']
        
        widgets={
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),     
        }
        
class LoginForm(AuthenticationForm):
    username=forms.CharField(
        label='Username',widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'type':'text', 'align':'center'}) )
    password=forms.CharField(
        label='Password',widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg', 'type':'password', 'align':'center'}) )
    
class EditprofileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','mobile','profile_pic','bio']      
        widgets={
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'mobile': forms.TextInput(attrs={'class':'form-control'}),  
            'profile_pic':forms.FileInput(attrs={'class':'form-control'}),
            'bio':forms.Textarea(attrs={'class':'form-control'})   
        }
class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),    
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),    
    )
    
    
class CreatepostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['files','dec']
        widgets={
            'files':forms.FileInput(attrs={'class':'form-control'}),
            'dec':forms.Textarea(attrs={'class':'form-control'}),
        }        
              
class EditpostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['dec']
        widgets={
            'dec':forms.TextInput(attrs={'class':'form-control'}),
        }        
                           
              
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment']          
        widgets={
            'comment':forms.TextInput(attrs={'class':'form-control'}),
        }    