from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from posts.models import Application, Evaluation, Assignment
from .models import Notification


@receiver(post_save, sender = Application)
def create_application_acceptance_notification(sender, instance: Application, created , **kwargs):
    cn = ContentType.objects.get_for_model(Application)
    id = instance.id
    if instance.status == "accepted":
        Notification.objects.create(
            notify_to = instance.applicant, 
            content = f"Congratulation, Your application for the {instance.post.type} program of {instance.post.title} has been accepted!", 
            content_type = cn, 
            object_id = id )
    elif instance.status == "rejected":
        Notification.objects.create(
            notify_to = instance.applicant, 
            content = f"Unfortunately, Your application for the {instance.post.type} program of {instance.post.title} has been rejected.", 
            content_type = cn, 
            object_id = id )
    else:
        print("something in signals")

@receiver(post_save, sender = Evaluation)
def create_evaluation_result_notification(sender, instance: Evaluation, created , **kwargs):
    cn = ContentType.objects.get_for_model(Evaluation)
    id = instance.id
    if created:
        Notification.objects.create(
            notify_to = instance.applicant, 
            content = f"Your Submission for the task {instance.submitted_task.task.title} has been evaluated.\n Grade: {instance.grade} \n Comment: {instance.comment}", 
            content_type = cn, 
            object_id = id )
        

@receiver(post_save, sender = Assignment)
def create_supervisor_assigned_notification(sender, instance: Assignment, created , **kwargs):
    cn = ContentType.objects.get_for_model(Assignment)
    id = instance.id
    if created:
        Notification.objects.create(
            notify_to = instance.student, 
            content = f"{instance.supervisor.get_full_name()} has been assigned to you as your University Supervisor.", 
            content_type = cn, 
            object_id = id )