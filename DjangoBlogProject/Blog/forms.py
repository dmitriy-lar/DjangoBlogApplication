from django import forms
from .models import Newsletter, Comments, CustomUserModel, PostModel
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class NewsLetterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'example@gmail.com'
    }), label='Enter your email address for newsletter:')

    class Meta:
        model = Newsletter
        fields = '__all__'


class CommentsForm(forms.ModelForm):
    content = forms.CharField(label='Message', widget=forms.Textarea(attrs={
        'rows': "10",
        'cols': "30",
        'class': 'form-control',
    }))

    class Meta:
        model = Comments
        fields = (
            'content',
        )


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = (
            'username',
            'email',
            'profile_picture'
        )


class PostCreationForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    thumbnail = forms.ImageField(required=True)

    class Meta:
        model = PostModel
        fields = (
            'title',
            'overview',
            'content',
            'category',
            'thumbnail'
        )