from unfold import admin as uadmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, Contact


@admin.register(User)
class UserModelAdmin(UserAdmin, uadmin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ["phone", "full_name", "is_active",]
    ordering = []
    model = User
    fieldsets = (
        ("Foydalanuvchini tahrirlash", {
            "fields": ("phone", "full_name", "is_active", "fcm_token", )
        }), 
    )
    add_fieldsets = (
        ("Yangi foydalanuvchi qo'shish", {
            "fields": ("phone", "password1", "password2", "full_name", )
        }), 
    )


@admin.register(Contact)
class ContactModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", "phone", "telegram"]


admin.site.unregister(Group)

admin.site.index_title = 'IMedTeam admin panelga xush kelibsiz'
admin.site.site_header = 'IMedTeam'
admin.site.site_title = 'IMedTeam Admin'