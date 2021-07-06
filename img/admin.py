from django.contrib import admin
from .models import Github,Profile

@admin.register(Github)
class GithubAdmin(admin.ModelAdmin):
    list_display=['githubuser','imagelink','username']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','token','verify']