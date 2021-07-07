from django.contrib import admin
from .models import Github,Profile,Quaries

@admin.register(Github)
class GithubAdmin(admin.ModelAdmin):
    list_display=['githubuser','imagelink','username']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','token','verify']

@admin.register(Quaries)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['email','msg']
    