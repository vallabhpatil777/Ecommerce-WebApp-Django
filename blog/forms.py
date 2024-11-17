from django import forms

from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'body', 'snippet', 'author','category', 'image',)
        labels = {
        	"title":  "عنوان ",
			"body": "متن",
			"snippet": "چکیده",
			"category": "دسته بندی ",
			"image": "تصویر ",
    	}
        
        widgets = {
            
            'title': forms.TextInput(attrs={'class' : 'form-control',}),
            'author': forms.TextInput(attrs={'class' : 'form-control', 'value': '', 'id': 'author', 'type': 'hidden'}),
            'body': forms.TextInput(attrs={'class' : 'form-control',}),
            'category': forms.Select(attrs={'class' : 'form-control'}),
            'snippet': forms.TextInput(attrs={'class' : 'form-control',}),
            'image': forms.FileInput(attrs={'accept': 'image/*'})
        }
        

class EditForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'body', 'snippet', 'image',)
        
        widgets = {
            
            'title': forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'write your title here'}),
            'body': forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'write your body here...'}),
            'snippet': forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'write your snippet here...'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'})
        }
        
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control md-textarea',
        'placeholder': 'Comment Here...',
        'rows': 4,
        
        
    }))
    
    class Meta:
        model = Comment
        fields = ('content',)
    