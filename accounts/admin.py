from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', "phone_number"),
                },
            ),
        )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ['email', 'first_name', 'last_name', "phone_number",'is_staff']
    ordering = ['email']
    exclude = ['username']

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if 'password1' in form.cleaned_data:
                obj.set_password(form.cleaned_data["password1"])
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Applicant)
admin.site.register(Student)
admin.site.register(Organization)
admin.site.register(UniversityCoordinator)
admin.site.register(UniversitySupervisor)
admin.site.register(Notification)
admin.site.register(AcceptedStudents)