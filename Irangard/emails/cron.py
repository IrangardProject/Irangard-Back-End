from django.core.mail import EmailMessage

from emails.models import EmailQueue


"""
EMAIL_STATES = [
        ("0", "wait"),
        ("1", "sent"),
        ("2", "idle")
]
"""


def email_send_cronjob():
    emails = EmailQueue.objects.filter(state='0')
    for email in emails:
        try:
            email_obj = EmailMessage(email.email_title, email.email_body, email.sender, [email.receiver])
            email_obj.content_subtype = "html"
            email_obj.fail_silently = False
            email_obj.send()
        except TimeoutError as t:
            print("timeout error")
            email.state = '2'
            email.save()
            return False
        except Exception as e:
            print(e)
            email.state = '2'
            email.save()
            return False
        else:
            email.state = '1'
            email.save()