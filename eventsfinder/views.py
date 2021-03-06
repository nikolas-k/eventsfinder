from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from eventsfinder.models import Event, Attendee, Staff
import settings

from eventsfinder.tools.forms import EventCreationForm

def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def add_event(request):

    form = request.POST.get("form", "")

    if request.method =='POST':
        form = EventCreationForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('manage_events')
    else:
        form = EventCreationForm()

    return render(request, 'add_event.html', { 'form' : form, 'debug' : False })

@login_required(login_url='/login/')
def find_events(request):

    events = None

    if request.method == 'POST':
        tags = list(request.POST.get("tags", "").split(','))

        if tags:
            try:
                events = Event.objects.filter(tags=tags)

            except Exception:
                pass

    return render(request, 'find_events.html', { 'events' : events })

@login_required(login_url='/login/')
def manage_events(request):
    created = Event.objects.filter(creator=request.user)
    attendee_all = Attendee.objects.filter(attendee=request.user)
    attending = []
    for a in attendee_all:
        attending.append(a.event)

    return render(request, 'manage_events.html', { 'created': created, 'attending': attending })

def edit_event(request, event_id):

    data = {}
    data['form'] = request.POST.get("form", "")

    try:
        data['event'] = Event.objects.get(id=event_id)

        if data['event'].creator != request.user:
            return render(request, 'generic_message.html', { 'header' : 'Event not found...', 'message': "Oops, we couldn't find the event you were looking for..." })

        all_attendees = Attendee.objects.filter(event=event_id)
        all_staff = Staff.objects.filter(event=event_id)

        data['attendees'] = all_attendees.filter(type='A')
        data['trackers'] = all_attendees.filter(type='T')

        data['organizers'] = all_staff.filter(type='O')
        data['mentors'] = all_staff.filter(type='M')
        data['speakers'] = all_staff.filter(type='S')

        if request.method =='POST':
            data['form'] = EventCreationForm(request.POST)

            if data['form'].is_valid():
                event = data['form'].save(commit=False)
                event.creator = request.user
                event_id = data['event'].id
                data['event'] = event
                data['event'].id = event_id
                data['event'].save()
        else:
            data['form'] = EventCreationForm()

    except Exception, err:
        # Event not found so raise an event not found
        return render(request, 'generic_message.html', { 'header' : 'Event not found...', 'message': err if settings.DEBUG else "Oops, we couldn't find the event you were looking for..." })

    return render(request, 'edit_event.html', data)

def view_event(request, event_id):
    data = {}

    try:
        data['event'] = Event.objects.get(id=event_id)

        all_attendees = Attendee.objects.filter(event=event_id)
        all_staff = Staff.objects.filter(event=event_id)

        data['attendees'] = all_attendees.filter(type='A')
        data['trackers'] = all_attendees.filter(type='T')

        data['organizers'] = all_staff.filter(type='O')
        data['mentors'] = all_staff.filter(type='M')
        data['speakers'] = all_staff.filter(type='S')

    except Exception, err:
        # Event not found so raise an event not found

        return render(request, 'generic_message.html', { 'header' : 'Event not found...', 'message': err if settings.DEBUG else "Oops, we couldn't find the event you were looking for..." })

    return render(request, 'view_event.html', data)


def signup(request):

    form = request.POST.get("form", "")

    if request.method =='POST':
        form = UserCreationForm(request.POST)

    if form:
        if form.is_valid():
            user = form.save()

            # We use this to set the user as authenticated, as we have just created the user
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)
            return redirect('home') # Redirect after POST
    else:
        form = UserCreationForm() # An unbound form

    return render_to_response('signup.html', { 'form': form, }, context_instance=RequestContext(request))


def handler404(request):
    return render(request, 'generic_message.html', { 'header' : '404 not found...', 'message': "Oops, we couldn't find what you were looking for..." })