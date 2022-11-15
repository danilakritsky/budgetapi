from celery import shared_task
from django.core.mail import send_mail
from transactions.helpers import get_current_week_text_summary
from transactions.models import Transaction
from users.models import User


@shared_task(name="celery_check", bind=True)
def celery_check(self):
    return {"result": "success"}


@shared_task(name="send_emails", bind=True)
def send_emails(self):
    users = User.objects.filter(subscribed=True)

    for user in users:
        summary = get_current_week_text_summary(
            Transaction.objects.filter(user=user.id)
        )
        send_mail(
            subject="Your budget summary for the current week",
            message=summary,
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
