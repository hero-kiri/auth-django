from django.core.mail import send_mail
from django.http import HttpResponse

def send_email(subject, email, message):
    recipient_list = [email]
    from_email = 'hero.beka.kg@gmail.com'

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Письмо отправлено')
    except Exception as e:
        return HttpResponse(str(e))

