from django.db import models

from accounts.models import *

class Post(models.Model):
    TYPE_CHOICES = [
        ('Internship', 'Internship'),
        ('VolunteerWork', 'Volunteer Work'),
    ]

    LEVEL_CHOICES = [
        ('Entry', 'Entry Level'),
        ('Mid', 'Mid Level'),
        ('Senior', 'Senior Level'),
    ]

    CATEGORY_CHOICES = [
        ('Banking', 'Banking'),
        ('Business', 'Business'),
        ('Marketing', 'Marketing'),
        ('Data', 'Data'),
        ('Finance', 'Finance'),
        ('Security', 'Security'),
        ('Software Engineering', 'Software Engineering'),
        ('Other', 'Other'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text="Enter the title of the post")
    description = models.TextField(help_text="Enter a detailed description of the post")
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, help_text="Upload an image related to the post (optional)")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    skills_gained = models.TextField(help_text = "Type skills gained after the post comma separated e.g problem solving, ", null=True, blank=True)
    duration = models.CharField(max_length=100, help_text="Enter the duration of the post (e.g., '3 months')")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated', '-created']
        get_latest_by = "created"

    def __str__(self):
        return self.title

    def get_tasks(self):
        try:
            return Task.objects.filter(post=self)
        except Task.DoesNotExist:
            return None
        
    def get_requirements(self):
        try:
            return Requirement.objects.filter(post=self)
        except Requirement.DoesNotExist:
            return None
        
    def get_applications(self):
        try:
            return Application.objects.filter(post=self)
        except Application.DoesNotExist:
            return None


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending' , 'Pending'
        SUBMITTED = 'submitted','submitted' 
        COMPLETED = 'completed', 'completed'

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text="Enter the title of the task")
    description = models.TextField(help_text="Enter a detailed description of the task")
    resource_url = models.URLField(blank=True, help_text="Enter a URL for additional resources related to the task (if any)")
    resource_video = models.URLField(blank=True, help_text="Enter a URL for a video resource related to the task (if any)")
    duration = models.CharField(max_length=100, help_text="Enter the estimated duration of the task (e.g., '1 hour', '30 minutes')")
    is_file = models.BooleanField(default=False, help_text="Do you want applicants to submit this task as a file e.g txt, pdf, patch, doc")
    is_url = models.BooleanField(default=False, help_text="Do you want applicants to submit this task as a url for the solution e.g github link, google drive link")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_task_submissions(self):
        try:
            return TaskSubmission.objects.filter(task=self)
        except TaskSubmission.DoesNotExist:
            return None
    
    def get_evaluation(self):
        try:
            return Evaluation.objects.filter(task=self)
        except Evaluation.DoesNotExist:
            return None

class TaskSubmission(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="submission")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="submission")
    submited_url = models.URLField(null=True, blank=True, help_text="Submit solution's url")
    submited_file = models.FileField(upload_to="submissions/", null=True, blank=True, help_text="Submit solution's file")

    def __str__(self):
        return f"submission for task {self.task} by {self.applicant}"


class Requirement(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    skills = models.BooleanField(default=False, help_text="Specify whether you want to inquire about the applicant's skills.")
    cover_letter = models.BooleanField(default=False, help_text="Specify whether you want to inquire about the applicant's motivation for choosing your company.")
    availability = models.BooleanField(default=False, help_text="Specify whether you want to inquire about the applicant's availability for the position.")
    other = models.TextField(help_text="Enter any other questions you want to ask applicants.", null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Requirement for {self.post}"

class Application(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending' , 'Pending'
        COMPLETED = 'accepted', 'accepted'
        REJECTED = 'rejected', 'rejected'

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    skills = models.TextField(help_text="Write down your skills.", null=True, blank=True)
    cover_letter = models.TextField(help_text="Enter your motivation for choosing this company.", null=True, blank=True)
    availability = models.TextField(help_text="Enter your availability for the position.", null=True, blank=True)
    other = models.TextField(help_text="Enter your answer for any question", null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application #{self.id} - {self.applicant} for {self.post.title}"


class Certificate(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.PROTECT, null=True)
    default_text = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def generate_default_text(self):
        default_text = f"Congratulations {self.applicant.first_name} for completing {self.post.title} provided by VIVP and {self.post.organization.name}."
        return default_text

    def save(self, *args, **kwargs):
        if not self.default_text:
            self.default_text = self.generate_default_text()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'

    def __str__(self):
        return f"Certificate for {self.applicant.first_name} - {self.post.title}"


class Evaluation(models.Model):
    comment = models.TextField(blank=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    grade = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Enter a numerical value out of one hundred to indicate how well the task is completed."
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation for {self.task.title}"
    

class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    supervisor = models.ForeignKey(UniversitySupervisor, on_delete=models.SET_NULL, null=True)
    coordinator = models.ForeignKey(UniversityCoordinator, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"student {self.student.first_name} assigned to supervisor {self.supervisor.first_name}"