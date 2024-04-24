from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from testAPI.models import CollectionModel, LinkModel, CustomUserModel


@admin.register(CollectionModel)
class CollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(LinkModel)
class LinkAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomUserModel)
class CustomUserAdmin(UserAdmin):
    pass
