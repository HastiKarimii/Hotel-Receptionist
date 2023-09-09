from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import ReceptionistCreationForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView, PasswordResetView


def base(request):
    if request.method == "GET":
        return render(request, 'Base.html')


def home(request):
    if request.method == "GET":
        return render(request, 'Home.html')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account'
    message = render_to_string('Emails/AccountActivationEmail.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email "{to_email}" inbox and click on \
                received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


class RegisterView(CreateView):
    form_class = ReceptionistCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account till it is confirmed
        user.save()
        activateEmail(self.request, user, form.cleaned_data.get('email'))
        # messages.success(self.request, 'Please confirm your email address to complete the registration')
        redirect('login')

        return super().form_valid(form)


@login_required()
def redirect_after_login(request):
    nxt = request.GET.get("next", None)
    if nxt is None:
        return redirect('listreserve')
    elif not url_has_allowed_host_and_scheme(
            url=nxt,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()):
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect(nxt)


def login_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active == True:
                form = login(request, user)
                messages.success(request, f' Welcome {user}!')
                return redirect_after_login(request)
            else:
                messages.info(request, 'Login Failed! Please confirm your email address first!')

        # else:
        #     messages.info(request, 'Login Failed! Enter the username and password correctly')

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'login'})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'ChangePassword.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed. Please login with your new password!')
        return super().form_valid(form)


@login_required()
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('home')
