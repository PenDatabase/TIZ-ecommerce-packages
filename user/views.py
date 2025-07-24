from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.conf import settings
from .forms import RegisterForm
from .tokens import account_activation_token

User = get_user_model()


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse("Activation Link is invalid")



def send_activation_email(user, request):
    domain = request.get_host()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    mail_subject = 'Activate your Account | CU Packages'
    html_message = render_to_string('registration/emails/activate_email.html', {
        'user': user,
        'domain': domain,
        'uid': uid,
        'token': token,
    })

    plain_message = f"Hello {user.first_name},\n\n" \
                    f"Please activate your account by clicking the link below:\n" \
                    f"http://{domain}/activate/{uid}/{token}/\n\n" \
                    f"If you did not request this, please ignore this email."
    
    email = EmailMultiAlternatives(mail_subject,
                                   plain_message,
                                   settings.EMAIL_HOST_USER,
                                   [user.email])
    
    email.attach_alternative(html_message, 'text/html')

    email.send()



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False # Deactivate user until email is activated
        user.save()
        send_activation_email(user, self.request)
        return render(self.request, 'registration/email_confirmation.html', {
            'user': user,
            'email': user.email
        })
        





