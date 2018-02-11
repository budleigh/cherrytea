from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import stripe

from cherrytea_app.forms import *
from cherrytea_app.logger import Logger
from cherrytea_app.interfaces import *

logger = Logger()
stripe.api_key = 'sk_test_3PFwtSlitXPqUhUmFXWi7sbR'

user_interface = UserInterface()
plan_interface = PlanInterface()
group_interface = GroupInterface()


@require_http_methods(['GET'])
def index(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'index.html', {
        'signin_form': SigninForm(),
        'signup_form': SignupForm(),
    })


@login_required
@require_http_methods(['GET'])
def home(request):
    return render(request, 'home.html')


@require_http_methods(['GET'])
def browse(request):
    return render(request, 'browse.html', {
        'charitygroups': group_interface.all()
    })


@require_http_methods(['GET'])
def group(request, id=None):
    return render(request, 'group.html', {
        'group': group_interface.get(id)
    })


@login_required
@require_http_methods(['GET', 'POST'])
def plan(request, id=None):
    donation_plan = plan_interface.get(id)
    if donation_plan.user != request.user:
        messages.add_message(request, messages.WARNING, 'That\'s not one of your donation plans!')
        return redirect('home')

    return render(request, 'user/plan.html', {
        'plan': donation_plan,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def create_plan(request, id=None):
    charity_group = group_interface.get(id)

    if request.method == 'POST':
        logger.info('creating plan for user', request.user)

        form = PlanForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            amount = int(data['amount'])

            if amount < 5:
                messages.add_message(request, messages.WARNING, 'There is a $5 minimum for donation plans.')
                return redirect('create_plan', id=id)

            try:
                new_plan = plan_interface.create(request.user, charity_group, amount, data['day_of_week'])
            except IntegrityError:
                messages.add_message(
                    request,
                    messages.WARNING,
                    'Whoops! Looks like you already have a plan for that charity group.',
                )
                return redirect('home')

            messages.add_message(
                request,
                messages.INFO,
                'Thanks so much! Your plan will start on the following %s.' % data['day_of_week'],
            )
            logger.info('created plan for user', request.user, new_plan)
            return redirect('plan', id=new_plan.id)

    else:
        return render(request, 'plan.html', {
            'group': charity_group,
            'plan_form': PlanForm(),
        })


@login_required
@require_http_methods(['GET'])
def cancel_plan(request, id=None):
    try:
        plan_interface.cancel(id, request.user)
    except AccessError:
        messages.add_message(request, messages.WARNING, 'Whoops, that plan isn\'t yours!')
        return redirect('home')

    messages.add_message(
        request,
        messages.INFO,
        'We\'ve cancelled your donation plan for %s. Thanks for your contributions!' % donation_plan.group.name,
    )
    return redirect('home')


@require_http_methods(['POST'])
def sign_up(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        email = data['email']
        password = data['password']
        timezone = data['timezone']

        try:
            user_interface.create_user(email, password, timezone)

            authed_user = authenticate(username=email, password=password)
            login(request, authed_user)
            logger.info('user created', authed_user)
            return redirect('home')

        except IntegrityError:
            logger.warning('user clash: %s' % email)
            messages.add_message(request, messages.ERROR, 'Whoops! Looks like that user already exists.')
            return redirect('index')

    else:
        messages.add_message(request, messages.ERROR, 'Whoops, something wasn\'t quite right there.')
        return redirect('index')


@require_http_methods(['POST'])
def sign_in(request):
    form = SigninForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        email = data['email']
        password = data['password']

        authed_user = authenticate(username=email, password=password)
        if authed_user:
            login(request, authed_user)
            logger.info('user logged in', authed_user)
            return redirect('home')
        else:
            logger.warning('user failed to logged in: %s' % email)
            messages.add_message(request, messages.ERROR, 'Login failed.')
            return redirect('index')

    else:
        messages.add_message(request, messages.ERROR, 'Whoops, something wasn\'t quite right there.')
        return redirect('index')


def sign_out(request):
    logger.info('user logged out', request.user)
    logout(request)
    return redirect('index')
