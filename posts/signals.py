from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskStatus, PostStatus, Application, Task, TaskSubmission, Evaluation

@receiver(post_save, sender=TaskStatus)
def update_post_status_after_all_tasks_completed(sender, instance, **kwargs):
    post = instance.task.post
    applicant = instance.applicant

    task_statuses = TaskStatus.objects.filter(task__post=post, applicant=applicant)
    all_completed = all(task_status.status == TaskStatus.Status.COMPLETED for task_status in task_statuses)
    post_status, created = PostStatus.objects.get_or_create(post=post, applicant=applicant)
    if all_completed:
        post_status.status = PostStatus.Status.COMPLETED
    else:
        post_status.status = PostStatus.Status.INPROGRESS

    post_status.save()


@receiver(post_save, sender=Application)
def create_post_status_after_application_accepted(sender, instance, **kwargs):
    if instance.status == Application.Status.ACCEPTED:
        post = instance.post
        applicant = instance.applicant
        # Check if PostStatus already exists for this applicant and post
        post_status, created = PostStatus.objects.get_or_create(
            post=post,
            applicant=applicant,
            status = PostStatus.Status.INPROGRESS
        )
        if not created:
            post_status.status = PostStatus.Status.INPROGRESS
            post_status.save()

        tasks = Task.objects.filter(post=post)
        for task in tasks:
            TaskStatus.objects.get_or_create(task=task, applicant=applicant, status=TaskStatus.Status.INPROGRESS)

@receiver(post_save, sender=TaskSubmission)
def update_task_status_after_task_submitted(sender, instance, created, **kwargs):
    if created:
        task = instance.task
        applicant = instance.applicant

        task_status, created = TaskStatus.objects.get_or_create(task=task, applicant=applicant)
        task_status.status = TaskStatus.Status.SUBMITTED
        task_status.save()


@receiver(post_save, sender=Evaluation)
def update_task_status_after_evaluation(sender, instance, created, **kwargs):
    if created:
        submitted_task = instance.submitted_task
        applicant = instance.applicant
        task = submitted_task.task

        task_status, created = TaskStatus.objects.get_or_create(task=task, applicant=applicant)
        task_status.status = TaskStatus.Status.COMPLETED
        task_status.save()


