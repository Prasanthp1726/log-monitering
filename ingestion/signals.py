from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender='ingestion.LogEntry')
def alert_on_log(sender, instance, created, **kwargs):
    if not created:
        return

    from .models import Alert
    alerts = Alert.objects.filter(is_active=True)
    for alert in alerts:
        match = True
        if alert.service and alert.service.lower() != instance.service.lower():
            match = False
        if alert.log_level and alert.log_level.upper() != instance.log_level.upper():
            match = False
        if alert.message_contains and alert.message_contains.lower() not in instance.message.lower():
            match = False

        if match:
            subject = f'Alert: {alert.name} - {instance.service} {instance.log_level}'
            message = f'Alert triggered: {alert.name}\n\nLog Details:\nService: {instance.service}\nTimestamp: {instance.timestamp}\nLevel: {instance.log_level}\nMessage: {instance.message}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email.strip() for email in alert.email_recipients.split(',')]

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                print(f'Failed to send alert email: {e}')