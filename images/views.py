from re import template
from django.contrib.auth import login
from django.db.models import Count
from actions.utils import create_action
from django.forms.widgets import PasswordInput
from images.models import Image
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ImageCreateForm
from django.contrib import messages
from comon.decorators import ajax_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
import redis

# Connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

@login_required
def create_image(request):
    user = request.user
    if request.method == 'POST':
        # form was submitted
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            print("form was valid")
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            new_item.user = user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Successfuly added an image')
            return redirect(new_item.get_absolute_url())
        else:
            print('FORM WAS NOT VALID')
            print(form.errors)
    else:
        form = ImageCreateForm(data=request.GET)

    template_name = 'create-image.html'
    context = {
        'user': user,
        'form': form
    }

    return render(request, template_name, context)


@login_required
def image_detail(request, slug):
    image = get_object_or_404(Image, slug=slug)
    # increment the image views by 1
    total_views = r.incr(f'image:{image.id}:views')
    # increment the ranking by 1
    r.zincrby('image_ranking', 1, image.id)
    template_name = 'image-detail.html'
    
    context = {
        'image': image,
        'total_views': total_views,
    }
    print(image.title)
    return render(request, template_name, context)


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        print('got that')
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                print('liked')
                image.users_likes.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                print('unliked')
                image.users_likes.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass

    return JsonResponse({'status':'error'})

@login_required
def list_images(request):
    print('this is the request', request.GET)
    images = Image.objects.order_by('-total_likes')
    paginator = Paginator(images, 6)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # page is not an interger deliver the first page
        print('This page is not an interger')
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # if the request is ajax and the page is out of range
            # return an empty page
            return HttpResponse('')
        #  if page is out of range deliver the last page of therresults
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        context = {
            'section': 'images',
            'images': images
        }
        template_name = 'list-ajax.html'
        return render(request, template_name, context)
    
    template_name = 'list.html'
    context = {
        'images': images,
    }

    return render(request, template_name, context)

@login_required
def image_ranking(request):
    # Get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]

    # Get the most viewed Images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))

    # most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    print(most_viewed)
    template_name = 'ranking.html'
    context = {
        'most_viewed': most_viewed
    }

    print(context['most_viewed'])
    
    return render(request, template_name, context)
    