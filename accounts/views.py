from django.contrib.messages.api import success
from django.http.response import JsonResponse
from accounts.models import Profile, Contact
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from images.models import Image
from comon.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action

User = get_user_model()
def dashboard(request):
    # Display all actions by defaut
    all_actions = Action.objects.all()
    actions = all_actions.exclude(user=request.user)

    following_ids = request.user.following.values_list('id', flat=True)
    
    if following_ids:
        # if user is following others then retrieve all their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    template_name = 'home.html'
    context = {
        'section': 'dashboard',
        'actions': actions,
    }

    return render(request, template_name, context)



def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get('password2')
        user = form.save(commit=False)
        # set the chosen user password
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
        create_action(user, 'has created an account')
        template_name = 'registration/register_done.html'
        context = {
            'user': user
        }
        return render(request, template_name, context)


    form = UserRegistrationForm()
    template_name = 'registration/register.html'
    context = {
        'form': form
    }

    return render(request, template_name, context)

@login_required
def editprofile(request):
    user = request.user
    if request.method == 'POST':
        u_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data = request.POST,
            files = request.FILES
        )

        if u_form.is_valid() and profile_form.is_valid():
            user_form = u_form.save(commit=False)
            user_form.user = user
            print('can save user')
            user.save
            print('can save profile')
            profile_form.save()

            messages.success(request, 'you have successfuly update your profile')
            return redirect('/')
        else:
            messages.error(request, 'Oops!! something went wrong')
            print('Error submitting the form')
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)

    template_name = 'registration/profile-edit.html'
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, template_name, context)


@login_required
def profile_listview(request):
    queryset = User.objects.filter(is_active=True)
    template_name = 'profile-list.html'
    context = {
        'obj_list': queryset,
        'section': 'people'
    }

    return render(request, template_name, context)


@login_required
def profile_detailview(request, username):
    user = get_object_or_404(User, username=username, is_active=True)

    template_name = 'profile-view.html'
    context = {
        'user': user,
        'section': 'people',
    }


    return render(request, template_name, context)


@ajax_required
@login_required
@require_POST
def follow_user(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    print('following the function')
    if action and user_id:
        try:
            user = get_object_or_404(User, id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})