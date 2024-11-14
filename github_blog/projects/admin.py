# projects/admin.py

from django.contrib import admin
from .models import Repository, Group, UserGroupSelection

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    search_fields = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserGroupSelection)
class UserGroupSelectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    list_filter = ('user', 'group')
