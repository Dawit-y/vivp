from django.contrib import admin
from .models import *

# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# class CustomUserCreationForm(UserCreationForm):
#     """
#     A form that creates a custom user with no privileges
#     from a provided email and password.
#     """

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('email',)

# class CustomUserChangeForm(UserChangeForm):
#     """
#     A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields.pop('username')

#     class Meta(UserChangeForm.Meta):
#         model = User
#         fields = '__all__'

# class CustomUserAdmin(UserAdmin):
#     model = User
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     form = CustomUserChangeForm
#     add_form = CustomUserCreationForm
#     list_display = ['email', 'first_name', 'last_name', 'is_staff']
#     ordering = ['email']
#     exclude = ['username']

#     def save_model(self, request, obj, form, change):

#         obj.set_password(form.cleaned_data["password"])
#         super().save_model(request, obj, form, change)

admin.site.register(User)
admin.site.register(Applicant)
admin.site.register(Student)
admin.site.register(Organization)
admin.site.register(UniversityCoordinator)
admin.site.register(UniversitySupervisor)
admin.site.register(Notification)