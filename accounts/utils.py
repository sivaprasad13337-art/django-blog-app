from django.contrib.auth.models import User
from django.core.mail import send_mail

def does_user_exists(username):
    return User.objects.filter(username=username).exists()

def fun(request):
    subject = 'About Registration'
    message = f'Hi ,You has been registered successfully on website.'
    email_from = 'sivaprasadfullstackdev@gmail.com'
    email = 'sivaprasad13337@gmaill.com'
    rec_list = [email,]
    response = send_mail(
                subject,
                message,
                email_from,
                rec_list,
                fail_silently=False
            )
    print("UYFRUYYUBTYUTBYUTUYBGUN", response)
    