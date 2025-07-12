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
    list_display = ["username", "full_name", "is_active",]
    model = User
    fieldsets = (
        ("Foydalanuvchini tahrirlash", {
            "fields": ("username", "full_name", "password", "is_active", )
        }), 
    )
    add_fieldsets = (
        ("Yangi foydalanuvchi qo'shish", {
            "fields": ("username", "password1", "password2", "full_name", )
        }), 
    )


@admin.register(Contact)
class ContactModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", "phone", "telegram"]


admin.site.unregister(Group)

admin.site.index_title = 'IMedTeam admin panelga xush kelibsiz'
admin.site.site_header = 'IMedTeam'
admin.site.site_title = 'IMedTeam Admin'