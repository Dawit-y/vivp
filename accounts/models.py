from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.apps import apps as django_apps

from .managers import UserManager
from .utils import UNIVERSITY_CHOICES


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, max_length=255, blank=False)
    first_name = models.CharField( _('first name'), max_length=30, blank=True)
    last_name = models.CharField( _('last name'), max_length=150,  blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField( _('active'), default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField( _('date joined'),default=timezone.now,)
    phone_regex = RegexValidator(regex=r'^\+251\d{9}$', message="Phone number must be entered in the format: '+251xxxxxxxxx'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class Applicant(User):

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female")
    ]
    gender = models.CharField(max_length = 1,choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(validators=[MinValueValidator(13), MaxValueValidator(120)])
    resume = models.FileField(upload_to='resumes/')
    portfolio_link = models.URLField()

    def __str__(self) -> str:
        return self.get_full_name()

    def clean(self):
        if self.resume.size > 5 * 1024 * 1024:
            raise ValidationError("File size too large. Maximum size allowed is 5 MB.")
    
    def get_certificates(self):
        try:
            Certificate = django_apps.get_model('posts.Certificate')
            return Certificate.objects.filter(applicant=self)
        except Certificate.DoesNotExist:
            return None
    
    def get_applications(self):
        try:
            Application = django_apps.get_model('posts.Application')
            return Application.objects.filter(applicant=self)
        except Application.DoesNotExist:
            return None
        
    def get_evaluations(self):
        try:
            Evaluation = django_apps.get_model('posts.Evaluation')
            return Evaluation.objects.filter(applicant=self)
        except Evaluation.DoesNotExist:
            return None
        
    def get_notifications(self):
        try:
            return Notification.objects.filter(notify_to=self, is_read=False)
        except Notification.DoesNotExist:
            return None
        
    def get_submitted_tasks(self):
        try:
            TaskSubmission = django_apps.get_model('posts.TaskSubmission')
            return TaskSubmission.objects.filter(applicant=self)
        except TaskSubmission.DoesNotExist:
            return None
  
        
class Student(Applicant):
    university = models.CharField(max_length=100, choices=UNIVERSITY_CHOICES, help_text="Choose your university", blank=False, null=False)
    university_id_number = models.CharField(max_length=100, help_text="Type your university ID", blank=False, null=False)
    batch = models.CharField(max_length=10, help_text="Enter your academic year or term (e.g., 3rd year)", blank=False, null=False)
    department = models.CharField(max_length=100, help_text="Enter your department or major (if applicable), otherwise enter 'Freshman' or your school name", blank=True)

    def __str__(self):
        return self.get_full_name()

    def get_supervisor(self):
        try:
            Assignment = django_apps.get_model('posts.Assignment')
            assigned = Assignment.objects.get(student=self)
            return assigned.supervisor
        except Assignment.DoesNotExist:
            return None

    def get_coordinator(self):
        try:
            Assignment = django_apps.get_model('posts.Assignment')
            assigned = Assignment.objects.get(student=self)
            return assigned.coordinator
        except Assignment.DoesNotExist:
            return None    


class Organization(models.Model):
    name = models.CharField(max_length=255, help_text='Full legal name of the organization')
    email = models.EmailField(help_text='Contact email address')
    phone_number = models.CharField(max_length=20, help_text='Contact phone number')
    organization_type = models.CharField(max_length=100, help_text='Type of organization (e.g., company, non-profit)')
    website = models.URLField(blank=True, help_text='Organization website URL')
    location_city = models.CharField(max_length=100, help_text='City where the organization is located')
    location_state = models.CharField(max_length=100, help_text='State/Province where the organization is located')
    description = models.TextField(help_text='Brief description of the organization and its mission')
    logo = models.ImageField(upload_to='organization_logos/', blank=True, help_text='Organization logo')
    linkedin_url = models.URLField(blank=True, null=True, help_text='LinkedIn profile URL')
    registration_date = models.DateTimeField(auto_now_add=True)
    supervisor = models.OneToOneField(User, on_delete = models.PROTECT)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name
    
    def get_posts(self):
        try:
            Post = django_apps.get_model("posts.Post")
            return Post.objects.filter(organization=self)
        except Post.DoesNotExist:
            return None
        
    def get_applicants(self):
        try:
            posts = self.get_posts()
            applications = [post.get_applications() for post in posts]
            applicants = [application.applicant for queryset in applications for application in queryset]
            return applicants
        except Exception as e:
            return None


class UniversityCoordinator(User):
    university = models.CharField(max_length=100, choices=UNIVERSITY_CHOICES, help_text="Choose your university", blank=False, null=False)
    legal_document = models.FileField(
        upload_to="university_coordinators/",
        help_text="Upload a document that proves you are assigned as a university coordinator by your university. "
                "Acceptable file formats include PDF or images. "
                "The document should contain official approval, such as a letter with a university stamp.",
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'University Coordinator'
        verbose_name_plural = 'University Coordinators'

    def __str__(self):
        return self.get_full_name()
    
    def get_assignments(self):
        try:
            Assignment = django_apps.get_model("posts.Assignment")
            return Assignment.objects.filter(coordinator=self)
        except Assignment.DoesNotExist:
            return None

    def get_students(self):
        try:
            return Student.objects.filter(university=self.university)
        except Student.DoesNotExist:
            return None

class UniversitySupervisor(User):
    coordinator = models.ForeignKey(UniversityCoordinator, on_delete=models.CASCADE)
    university = models.CharField(max_length=100, choices=UNIVERSITY_CHOICES, help_text="Select the university associated with the supervisor", blank=False, null=False)
    department = models.CharField(max_length=100, help_text="Enter the department where the supervisor is working")
    specialization = models.CharField(max_length=100, help_text="Specify the supervisor's area of expertise (e.g., Machine Learning, Data Science)")

    class Meta:
        verbose_name = 'University Supervisor'
        verbose_name_plural = 'University Supervisors'

    def __str__(self):
        return self.get_full_name()

    def get_students(self):
        try:
            Assignment = django_apps.get_model("posts.Assignment")
            assignments = Assignment.objects.select_related('student').filter(supervisor=self)
            return [assign.student for assign in assignments]
        except Assignment.DoesNotExist:
            return None


class Notification(models.Model):
    notify_to = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="notifications")
    content = models.TextField(null = True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    is_read = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"notify to {self.notify_to}"
    
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ['-updated', '-created']
        get_latest_by = "created"
