from foodgram.settings import DEFAULT_FROM_EMAIL
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail, BadHeaderError
from .forms import CreationForm, EmailForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'


def send_my_mail(request):
    form = EmailForm(request.POST or None)
    if form.is_valid():
        subject = 'Смена пароля'
        to_email = 'radikkhabibulin@mail.ru'
        message = 'ссылка на смену пароля'
        try:
            send_mail(f'{subject} от {to_email}', message,
                      DEFAULT_FROM_EMAIL, [to_email])
        except BadHeaderError:
            return HttpResponse('Ошибка в теме письма.')
        return redirect('password_reset_done')
    return render(request, 'registration/password_reset_form.html', {
            'form': form,
        }
    )

# class PasswordReset(PasswordResetView):
#     form_class = PasswordResetForm


# class PasswordResetView(PasswordContextMixin, FormView):
#     email_template_name = 'registration/password_reset_email.html'
#     extra_email_context = None
#     form_class = PasswordResetForm
#     from_email = None
#     html_email_template_name = None
#     subject_template_name = 'registration/password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')
#     template_name = 'registration/password_reset_form.html'
#     title = _('Password reset')
#     token_generator = default_token_generator

#     @method_decorator(csrf_protect)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def form_valid(self, form):
#         opts = {
#             'use_https': self.request.is_secure(),
#             'token_generator': self.token_generator,
#             'from_email': self.from_email,
#             'email_template_name': self.email_template_name,
#             'subject_template_name': self.subject_template_name,
#             'request': self.request,
#             'html_email_template_name': self.html_email_template_name,
#             'extra_email_context': self.extra_email_context,
#         }
#         form.save(**opts)
#         return super().form_valid(form)
