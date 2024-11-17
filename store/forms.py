from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Product, Profile, ProductComment


class SignUpForm(UserCreationForm):
    
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
  

class EditUserForm(UserChangeForm):
    
	class Meta:
		model = User
		password = forms.CharField(widget=forms.PasswordInput())
		fields = ('username', 'email', 'first_name', 'last_name','password',)
		labels = {
        	"username":  "نام کاربری",
			"email": "ایمیل",
			"first_name": "نام",
			"last_name": "نام خانوادگی",
			"password": "رمز عبور",
    	}

		help_texts = {
            'username': None,
            'password': None,
        }

		widgets = {
     		'username': forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'نام کاربری'}),
        	'email': forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'ایمیل'}),
        	'first_name': forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'نام '}),
        	'last_name': forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'نام خانوادگی'}),
			
		}
	
  

class ProfileForm(forms.ModelForm):
    
	class Meta:
		model = Profile
		fields = ('bio', 'profile_pic', 'facebook_url', 'instagram_url', 'twitter_url', 'pinterest_url', 'youtube_url',)
    
		widgets = {
		
    	        'bio': forms.Textarea(attrs={'class' : 'form-control'}),
    	        'profile_pic': forms.FileInput(attrs={'accept': 'image/*'}),
    	        'facebook_url': forms.TextInput(attrs={'class' : 'form-control'}),
    	        'instagram_url': forms.TextInput(attrs={'class' : 'form-control'}),
    	        'twitter_url': forms.TextInput(attrs={'class' : 'form-control',}),
    	        'pinterest_url': forms.TextInput(attrs={'class' : 'form-control',}),
    	        'youtube_url': forms.TextInput(attrs={'class' : 'form-control',}),
    	    }
  
class EditProfile(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'facebook_url', 'instagram_url', 'twitter_url', 'pinterest_url', 'youtube_url',)
        labels = {
        	"bio":  "درباره من",
			"profile_pic": "عکس پروفایل",
			"facebook_url": "فیسبوک",
			"instagram_url": "اینستاگرام",
			"twitter_url": "توییتر",
			"pinterest_url": "پینترست",
			"youtube_url": "یوتیوب",
	
    	}
        
        widgets = {
            
            'bio': forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'خود را معرفی کنید ...', 'label': 'درباره من'}),
            'profile_pic': forms.FileInput(attrs={'accept': 'image/*'}),
            'facebook_url': forms.TextInput(attrs={'class' : 'form-control',}),
            'instagram_url': forms.TextInput(attrs={'class' : 'form-control',}),
            'twitter_url': forms.TextInput(attrs={'class' : 'form-control',}),
            'pinterest_url': forms.TextInput(attrs={'class' : 'form-control',}),
            'youtube_url': forms.TextInput(attrs={'class' : 'form-control',}),
            
        }

class ProductCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control md-textarea',
        'placeholder': 'کامنت شما...',
        'rows': 4,
        
        
    }))
    
    class Meta:
        model = ProductComment
        fields = ('content',)