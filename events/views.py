from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from pyppeteer import launch
from django.contrib import messages
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from datetime import datetime


# Venue PDF Generation using Pyppeteer
async def venue_pdf(request):
    # Fetch the venues from the database
    venues = Venue.objects.all()

    # Render the HTML content for the PDF
    html_content = render_to_string('events/venue_pdf_template.html', {'venues': venues})

    # Launch the browser and generate the PDF
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setContent(html_content)
    pdf_file = await page.pdf()

    # Close the browser after the PDF is generated
    await browser.close()

    # Return the PDF as a downloadable response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="venues.pdf"'
    return response


def venue_csv(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment;filename=venues.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate into model
    venues = Venue.objects.all()

    # Add column heading in csv file
    writer.writerow(['name', 'address', 'zipcode', 'phone', 'web', 'emailaddress'])

    # Loop through output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.zipcode, venue.emailaddress, venue.web])

    return response


def venue_text(request):
    response = HttpResponse(content_type="text/plain")
    response['Content-Disposition'] = 'attachment;filename=venue.txt'
    # Designate into model
    venues = Venue.objects.all()
    lines = []

    # Loop through output
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.phone}\n{venue.zipcode}\n{venue.emailaddress}\n{venue.web}\n')

    response.writelines(lines)
    return response


def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/show_event.html', {
        "event": event
    })


def admin_approval(request):
    # get venue
    venuelist = Venue.objects.all()
    # get count
    eventcount = Event.objects.all().count()
    venuecount = Venue.objects.all().count()
    usercount = User.objects.all().count()
    event_list = Event.objects.all().order_by('-eventdate')

    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')
            # uncheck all events
            event_list.update(approved=False)
            # update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)

            messages.success(request, ("Event list approval has been updated"))
            return redirect('list-events')
        else:
            return render(request, 'events/adminapproval.html', {
                'event_list': event_list,
                'eventcount': eventcount,
                'venuecount': venuecount,
                'usercount': usercount,
                'venuelist': venuelist,
            })

    else:
        messages.success(request, ("you are not authorized to use this page"))
        return redirect('home')


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/addevent?submitted=True')
        else:
            form = EventForm(request.POST)

            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user.id  # logged-in user
                event.save()
                return HttpResponseRedirect('/addevent?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, "events/addevent.html", {
        "form": form,
        "submitted": submitted
    })


# Venue PDF view using Pyppeteer
async def venue_pdf(request):
    # Fetch the venues from the database
    venues = Venue.objects.all()

    # Render the HTML content for the PDF
    html_content = render_to_string('events/venue_pdf_template.html', {'venues': venues})

    # Launch the browser and generate the PDF
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setContent(html_content)
    pdf_file = await page.pdf()

    # Close the browser after the PDF is generated
    await browser.close()

    # Return the PDF as a downloadable response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="venues.pdf"'
    return response


def show_venue(request, venue_id):
    # Fetch the venue or return a 404 if it doesn't exist
    venue = get_object_or_404(Venue, pk=venue_id)

    # Try to fetch the venue owner, handle the case where it doesn't exist
    try:
        venueowner = User.objects.get(pk=venue.owner)
    except User.DoesNotExist:
        venueowner = None  # Set to None if the owner does not exist

    # Grab the events
    events = venue.event_set.all()
    return render(request, "events/show_venue.html", {
        'venue': venue,
        "venueowner": venueowner,
        "events": events,
    })


def list_venues(request):
    venue_list = Venue.objects.all()
    p = Paginator(Venue.objects.all(), 1)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages  # make sure it is a string

    return render(request, "events/venue.html", {
        'venue_list': venue_list,
        'venues': venues,
        "nums": nums
    })


def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    name = "navya"
    month = month.capitalize()

    # Convert month from name to number
    monthnumber = list(calendar.month_name).index(month)
    monthnumber = int(monthnumber)

    # Create a calendar
    cal = HTMLCalendar().formatmonth(year, monthnumber)

    # Get current year
    now = datetime.now()
    currentyear = now.year

    # Query event model by date
    event_list = Event.objects.filter(
        eventdate__year=year,
        eventdate__month=monthnumber
    )

    # Get current time
    time = now.strftime('%I:%M:%S:%p')

    return render(request, "events/home.html", {
        "name": name,
        "year": year,
        "month": month,
        "monthnumber": monthnumber,
        "cal": cal,
        "currentyear": currentyear,
        "time": time,
        "event_list": event_list
    })
from django.shortcuts import render
from .models import Event

def all_events(request):
    event_list = Event.objects.all().order_by('-eventdate')  # Get all events and order them by event date
    return render(request, 'events/all_events.html', {'event_list': event_list})
