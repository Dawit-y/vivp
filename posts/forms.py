from django import forms
from accounts.models import User
from .models import Post

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['system_coordinator'].queryset = User.objects.filter(is_staff=True, is_superuser=False)

    def clean(self):
        cleaned_data = super().clean()
        organization = cleaned_data.get('organization')
        system_coordinator = cleaned_data.get('system_coordinator')

        if organization and system_coordinator:
            raise forms.ValidationError('Only one of organization or system coordinator should be set.')
        if not organization and not system_coordinator:
            raise forms.ValidationError('Either organization or system coordinator must be set.')

        return cleaned_data
