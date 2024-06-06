from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail, EmailMessage
import threading
from django.conf import settings
from django.template.loader import render_to_string


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email =email
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            self.email.send()
        except Exception as e:
            # Log the error or handle it accordingly
            print(f"Failed to send email: {e}")

@receiver(post_save, sender=User)
def send_user_mail(sender, instance, created, *args, **kwargs):
    if created:
        client = User.objects.first()
        # customising the body
        email_template = "emails/register_login_email.html"
        c = {
            'client': client,
            'user': client.username,
            'user_email': client.email,
            'sender_email': settings.EMAIL_HOST_USER,
        }
        
        renderer = render_to_string(email_template, c)
        mysender = EmailMessage(subject='Account Created', body=renderer, to=[client.email], from_email=settings.EMAIL_HOST_USER)
        mysender.content_subtype = "html"
        EmailThread(mysender).start()
        # send_mail('Account Created', f"Hello {client.username} thank you for being a part of our system and we want to welcome to our site", recipient_list=[client.email], from_email="jackoliver023@gmail.com", fail_silently=False)
    else:
        # send_mail('Welcome Back Message', f"Hello welcome back to our site", recipient_list=[instance.email], from_email="jackoliver023@gmail.com", fail_silently=False)
        email_template = "emails/register_login_email.html"
        c = {
            'instance': instance,
            'user': instance.username,
            'user_email': instance.email,
            'sender_email': settings.EMAIL_HOST_USER,
        }
        renderer = render_to_string(email_template, c)
        mysender = EmailMessage(subject='Welcome Back Message', body=renderer, to=[instance.email], from_email=settings.EMAIL_HOST_USER)
        mysender.content_subtype = "html"
        EmailThread(mysender).start()
    