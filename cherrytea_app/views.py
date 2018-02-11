from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cherrytea_app.forms import *
from cherrytea_app.models import User, CharityGroup, DonationPlan
from cherrytea_app.util import day_map


@require_http_methods(['GET'])
def index(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'index.html', {
        'auth_form': AuthForm(),
    })


@login_required
@require_http_methods(['GET'])
def home(request):
    return render(request, 'home.html')


@require_http_methods(['GET'])
def browse(request):
    return render(request, 'browse.html', {
        'charitygroups': CharityGroup.objects.all()
    })


@require_http_methods(['GET'])
def group(request, id=None):
    return render(request, 'group.html', {
        'group': CharityGroup.objects.get(pk=id)
    })


@login_required
@require_http_methods(['GET', 'POST'])
def plan(request, id=None):
    donation_plan = DonationPlan.objects.get(pk=id)
    if donation_plan.user != request.user:
        messages.add_message(request, messages.WARNING, 'That\'s not one of your donation plans!')
        return redirect('home')

    return render(request, 'user/plan.html', {
        'plan': donation_plan,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def create_plan(request, id=None):
    charity_group = CharityGroup.objects.get(pk=id)

    for plan in request.user.plans.all():
        if plan.group == charity_group:
            messages.add_message(
                request,
                messages.INFO,
                'Whoops, looks like you already have a donation plan for that group!',
            )
            return redirect('plan', id=plan.id)

    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            amount = int(data['amount'])

            if amount < 5:
                messages.add_message(request, messages.WARNING, 'There is a $5 minimum for donation plans.')
                return redirect('create_plan', id=id)

            new_plan = DonationPlan.objects.create(
                group=charity_group,
                user=request.user,
                amount=amount,
                day=day_map[data['day_of_week']],
            )
            messages.add_message(
                request,
                messages.INFO,
                'Thanks so much! Your plan will start on the following %s.' % data['day_of_week'],
            )
            return redirect('plan', id=new_plan.id)

    else:
        return render(request, 'plan.html', {
            'group': charity_group,
            'plan_form': PlanForm(),
        })


@login_required
@require_http_methods(['GET'])
def cancel_plan(request, id=None):
    donation_plan = DonationPlan.objects.get(pk=id)

    # this shouldnt be possible but yeah
    if donation_plan.user != request.user:
        messages.add_message(request, messages.WARNING, 'That\'s not one of your donation plans!')
        return redirect('home')

    donation_plan.delete()
    messages.add_message(
        request,
        messages.INFO,
        'We\'ve cancelled your donation plan for %s. Thanks for your contributions!' % donation_plan.group.name,
    )
    return redirect('home')


def sign_up(request, email, password):
    try:
        User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        authed_user = authenticate(username=email, password=password)
        login(request, authed_user)
        return redirect('home')

    except IntegrityError:
        messages.add_message(request, messages.ERROR, 'Whoops! Looks like that user already exists.')
        return redirect('index')


def sign_in(request, email, password):
    authed_user = authenticate(username=email, password=password)
    if authed_user:
        login(request, authed_user)
        return redirect('home')
    else:
        messages.add_message(request, messages.ERROR, 'Login failed.')
        return redirect('index')


def sign_out(request):
    logout(request)
    return redirect('index')


@require_http_methods(['POST'])
def auth(request):
    form = AuthForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        email = data['email']
        password = data['password']

        if data['type'] == 'UP':
            return sign_up(request, email, password)
        if data['type'] == 'IN':
            return sign_in(request, email, password)

    else:
        return messages.add_message(
            request, messages.ERROR, 'Whoops, looks like something wasn\'t quite right there.'
        )
