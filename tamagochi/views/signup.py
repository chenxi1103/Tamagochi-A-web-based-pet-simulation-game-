from django.shortcuts import render, reverse, get_object_or_404
from tamagochi.forms import *
from django.db import transaction
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404
from django.contrib.auth.tokens import default_token_generator


def make_view(request,signup_form=SignupForm()):
    context = {'signup_form': signup_form}
    return render(request, 'authen/signup.html', context)


def signup(request):
    form = SignupForm(request.POST)
    if not form.is_valid():
        return make_view(request, signup_form=SignupForm(request.POST))

    else:
        new_user = User(username=form.cleaned_data['username'],
                            email=form.cleaned_data['email'])
        new_user.set_password(form.cleaned_data['password'])
        new_user.is_active = 0
        new_user.save()
        token = default_token_generator.make_token(new_user)
        email_body = """
                        I am waiting for you for a long time! So great to see you here!
                        Welcome to Tamagochi (￣∇￣) There is only one last step to be our member!
                        Simply click this link and enjoy~

                        http://%s%s
                    """ % (request.get_host(),
                           reverse('confirm', args=(new_user.username, token)))
        send_mail(
                subject='Welcome to Tamagochi! One more step: Verify your email adress!',
                message=email_body,
                from_email='Tamagochi@andrew.cmu.edu',
                recipient_list=[new_user.email]
                )
        return render(request, 'authen/emailConfirm.html')


@transaction.atomic
def confirmEmail(request,username,token):
    confirmUser = get_object_or_404(User,username=username)
    if not default_token_generator.check_token(confirmUser,token):
        raise Http404
    confirmUser.is_active = True
    confirmUser.save()
    return render(request,'authen/confirm_email_complete.html')
