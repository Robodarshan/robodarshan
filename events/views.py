from django.shortcuts import render
from events.forms import EventPostForm
import uuid
import os
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from accounts.models import robodarshanMember
from events.models import event
from events.models import event_list


@login_required
def new(request):
    # Handle image uploads for the post.
    if request.is_ajax():
        json_response = "{"
        for uploaded_file in request.FILES.getlist('photo'):
            # create folder with story id
            if not os.path.exists(settings.MEDIA_ROOT + request.POST.get('event_id')):
                os.makedirs(settings.MEDIA_ROOT + request.POST['event_id'])
            if os.path.exists(settings.MEDIA_ROOT + request.POST['event_id'] + '/' + uploaded_file.name):
                e.name = '1' + uploaded_file.name
            with open(settings.MEDIA_ROOT + request.POST['event_id'] + '/' + uploaded_file.name, 'w') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            json_response = json_response + "\"" + \
                uploaded_file.name + "\": \"" + destination.name + "\","
        json_response = json_response[:-1] + "}"
        return HttpResponse(json_response, content_type="application/json")

    # Handle the draft saves.

    # Handle the final save.
    if request.method == 'POST':
        form = EventPostForm(request.POST)
        event_id = request.POST['event_id']
        if form.is_valid():
            form.clean()
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            time = form.cleaned_data['time']
            coordinator1 = request.user
            coordinator2 = robodarshanMember.objects.get(
                email=form.cleaned_data['second_coordinator'])
            new_event = event(
                uuid=event_id,
                title=title,
                description=description,
                coordinator1=coordinator1,
                coordinator2=coordinator2,
                time=time,
                timestamp=timezone.now(),
            )
            volunteer1 = form.cleaned_data.get('volunteer1', None)
            volunteer2 = form.cleaned_data.get('volunteer2', None)
            location = form.cleaned_data.get('location', None)
            if volunteer1:
                volunteer1 = robodarshanMember.objects.get(email=volunteer1)
                new_event.volunteer1 = volunteer1
            if volunteer2:
                volunteer2 = robodarshanMember.objects.get(email=volunteer2)
                new_event.volunteer2 = volunteer2
            if location:
                new_event.location = location
            new_event.save()
            entry = event_list(f_uuid=event_id,
                               c_uuid=new_event,
                               l_uuid=new_event)
            entry.save()
            return render(request, 'events/index.html',
                          {'events': [new_event]})
        else:
            return render(request,
                          'events/editor.html',
                          {'post': 'some thing went wrong',
                           'action': 'new',
                           'form': form, 'id': event_id})
    event_id = uuid.uuid4().get_hex()
    form = EventPostForm()
    return render(request,
                  'events/editor.html',
                  {'post': 'edit page',
                   'action': 'new',
                   'form': form, 'id': event_id})


@login_required
def edit(request):
    # Handle changes
    if request.method == 'POST':
        form = EventPostForm(request.POST)
        event_id = request.POST.get('event_id', None)
        if form.is_valid():
            form.clean()
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            time = form.cleaned_data['time']
            coordinator1 = request.user
            coordinator2 = robodarshanMember.objects.get(
                email=form.cleaned_data['second_coordinator'])
            try:
                requested_event = event_list.objects.get(f_uuid=event_id)
            except event_list.DoesNotExist:
                return render(request,
                              'events/editor.html',
                              {'error': 'Sorry.. cannot find the event.'})
            if request.user not in [event_list.c_uuid.coordinator1, event_list.c_uuid.coordinator2]:
                return render(request,
                              'events/editor.html',
                              {'error': 'You don\'t seem to have the keys to the forbiden palace'})
            # generate new uuid
            new_uuid = uuid.uuid4().get_hex()
            new_event = event(
                uuid=new_uuid,
                title=title,
                description=description,
                coordinator1=coordinator1,
                coordinator2=coordinator2,
                time=time,
                timestamp=timezone.now(),
            )
            volunteer1 = form.cleaned_data.get('volunteer1', None)
            volunteer2 = form.cleaned_data.get('volunteer2', None)
            location = form.cleaned_data.get('location', None)
            if volunteer1:
                volunteer1 = robodarshanMember.objects.get(email=volunteer1)
                new_event.volunteer1 = volunteer1
            if volunteer2:
                volunteer2 = robodarshanMember.objects.get(email=volunteer2)
                new_event.volunteer2 = volunteer2
            if location:
                new_event.location = location
            new_event.save()
            requested_event.l_uuid = new_uuid
            requested_event.save()
            return render(request, 'events/index.html', {'posts': [new_event]})
        else:
            return render(request,
                          'blog/editor.html',
                          {'error': 'some thing went wrong',
                           'action': 'edit',
                           'form': form, 'id': event_id})
    # Display the edit form with story
    else:
        event_id = request.GET.get('id', None)
        try:
            requested_event = event_list.objects.get(f_uuid=event_id)
            requested_event = requested_event.c_uuid
        except event_list.DoesNotExist:
            return render(request,
                          'events/editor.html',
                          {'error': 'Event doesn\'t exist..'})
        if request.user not in [requested_event.coordinator1, requested_event.coordinator2]:
            return render(request,
                          'events/editor.html',
                          {'error': 'You don\'t seem to have the keys to the forbiden palace'})
        initial = {}
        initial['title'] = requested_event.title
        initial['description'] = requested_event.description
        initial['time'] = requested_event.time
        initial['volunteer1'] = requested_event.volunteer1
        initial['volunteer2'] = requested_event.volunteer2
        if request.user == requested_event.coordinator1:
            initial['second_coordinator'] = requested_event.coordinator2
        else:
            initial['second_coordinator'] = requested_event.coordinator1
        form = EventPostForm(initial=initial)
        return render(request,
                      'events/editor.html',
                      {'form': form, 'id': event_id, 'action': 'edit', })


@login_required
def delete(request):
    pass


@login_required
def show(request):
    events = event.objects.all()
    return render(request, 'events/index.html', {'events': events})
