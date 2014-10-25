from django.shortcuts import render
from events.forms import EventForm


def new(request):
    form = EventForm()
    return render(request, 'events/create.html', {'form': form})


def edit(request):
    pass


def delete(request):
    pass


def show(request):
    pass
