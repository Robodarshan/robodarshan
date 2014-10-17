from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.models import becAlumnus
from accounts.forms import becAlumnusChangeForm, becAlumnusCreationForm

class becAlumnusAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('fullname', 'nickname')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = becAlumnusChangeForm
    add_form = becAlumnusCreationForm
    list_display = ('email', 'fullname', 'nickname', 'is_staff')
    search_fields = ('email', 'fullname', 'nickname')
    ordering = ('email',)

admin.site.register(becAlumnus, becAlumnusAdmin)