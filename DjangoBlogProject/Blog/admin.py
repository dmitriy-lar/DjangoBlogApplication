from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from .models import CustomUserModel, CategoryModel, PostModel, Newsletter, Comments, PostView
from django import forms


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'date_joined',
        'is_staff',
    )
    ordering = (
        'username',
    )
    list_filter = (
        'email',
        'username',
        'date_joined'
    )
    search_fields = (
        'username',
        'email',
    )
    list_display_links = (
        'username',
        'email'
    )


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = PostModel
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(CustomUserModel, CustomUserAdmin)
admin.site.register(PostModel, PostAdmin)
admin.site.register(CategoryModel)
admin.site.register(Newsletter)
admin.site.register(Comments)
admin.site.register(PostView)
