import uuid
import os
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from blog import forms
from blog.models import story


def posts(request):
    posts = story.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})


@login_required
def new(request):
    # Handle image uploads for the post.
    if request.is_ajax():
        json_response = "{"
        for uploaded_file in request.FILES.getlist('photo'):
            # create folder with story id
            if not os.path.exists(settings.MEDIA_ROOT + request.POST.get('story_id')):
                os.makedirs(settings.MEDIA_ROOT + request.POST['story_id'])
            if os.path.exists(settings.MEDIA_ROOT + request.POST['story_id'] + '/' + uploaded_file.name):
                uploaded_file.name = '1' + uploaded_file.name
            with open(settings.MEDIA_ROOT + request.POST['story_id'] + '/' + uploaded_file.name, 'w') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            json_response = json_response + "\"" + \
                uploaded_file.name + "\": \"" + destination.name + "\","
        json_response = json_response[:-1] + "}"
        return HttpResponse(json_response, content_type="application/json")

    # Handle the draft saves.

    # Handle the final save.
    if request.method == 'POST':
        form = forms.BlogEditForm(request.POST)
        story_id = request.POST['story_id']
        try:
            article = story.objects.get(uuid=story_id)
            return render(request,
                          'blog/editor.html',
                          {'error': 'Naah.. heard that, tell something new.'})
        except story.DoesNotExist:
            pass
        if form.is_valid():
            form.clean()
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            author = request.user
            article = story(
                title=title,
                body=body,
                uuid=story_id,
                timestamp=timezone.now(),
                author=author)
            article.save()
            return render(request, 'blog/index.html', {'posts': [article]})
        else:
            return render(request,
                          'blog/editor.html',
                          {'error': 'some thing went wrong',
                           'action': 'new',
                           'form': form, 'id': story_id})
    story_id = uuid.uuid4().get_hex()
    form = forms.BlogEditForm()
    return render(request,
                  'blog/editor.html',
                  {'form': form, 'id': story_id, 'action': 'new', })


@login_required
def edit(request):
    # Handle changes
    if request.method == 'POST':
        form = forms.BlogEditForm(request.POST)
        story_id = request.POST.get('story_id', None)
        if form.is_valid():
            form.clean()
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            try:
                article = story.objects.get(uuid=story_id)
            except story.DoesNotExist:
                return render(request,
                              'blog/editor.html',
                              {'error': 'Thats an untold story..'})
            if request.user != article.author:
                return render(request,
                              'blog/editor.html',
                              {'error': 'You don\'t seem to have the keys to the forbiden palace'})
            article.title = title
            article.body = body
            article.timestamp = timezone.now()
            article.save()
            return render(request, 'blog/index.html', {'posts': [article]})
        else:
            return render(request,
                          'blog/editor.html',
                          {'error': 'some thing went wrong',
                           'action': 'edit',
                           'form': form, 'id': story_id})
    # Display the edit form with story
    else:
        story_id = request.GET.get('id', None)
        try:
            article = story.objects.get(uuid=story_id)
        except story.DoesNotExist:
            return render(request,
                          'blog/editor.html',
                          {'error': 'Thats an untold story..'})
        if request.user != article.author:
            return render(request,
                          'blog/editor.html',
                          {'error': 'You don\'t seem to have the keys to the forbiden palace'})
        initial = {}
        initial['title'] = article.title
        initial['body'] = article.body
        form = forms.BlogEditForm(initial=initial)
        return render(request,
                      'blog/editor.html',
                      {'form': form, 'id': story_id, 'action': 'edit', })
