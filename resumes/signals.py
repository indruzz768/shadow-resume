from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Resume

@receiver(post_save, sender=Resume)
def resume_status_handler(sender, instance, created, **kwargs):
    # Notify admin when new resume is created
    if created:
        send_mail(
            subject="New Resume Submitted",
            message=f"A new resume has been submitted by {instance.user.email}.",
            from_email=None,
            recipient_list=["indransatheesan321@gmail.com"],  # 🔁 Replace with your admin email
        )

    # Notify user on moderation decision
    elif instance.moderation_status in ['approved', 'rejected']:
        send_mail(
            subject=f"Your Resume has been {instance.moderation_status.capitalize()}",
            message=f"Hi {instance.full_name},\n\nYour resume titled \"{instance.headline}\" has been {instance.moderation_status}.",
            from_email=None,
            recipient_list=[instance.user.email],
        )
