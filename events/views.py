from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from.models import Event,Venue
#import user model from
from django.contrib.auth.models import User
from.forms import VenueForm,EventForm,EventFormAdmin
from django.http import HttpResponse
from django.contrib import messages
import csv
from django.shortcuts import get_object_or_404

#for pdf files


from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
#import pagination stuff
from django.core.paginator import Paginator

def show_event(request,event_id):
	event=Event.objects.get(pk=event_id)
	return render(request,'events/show_event.html',{
			"event":event
			})

def  venue_event(request,venue_id):
	#grab the venue
	venue=Venue.objects.get(id=venue_id)
	#grab the events 
	events=venue.event_set.all()
	if events:

		return render(request,'events/venue_event.html',{
			"events":events
			})
	else:
		messages.success(request,("that venue has no events at this time"))
		return redirect('list-events')

#create admin event approval page

def admin_approval(request):

	#get venue
	venuelist=Venue.objects.all()

	#get count
	eventcount=Event.objects.all().count()
	venuecount=Venue.objects.all().count()
	usercount=User.objects.all().count()
	event_list=Event.objects.all().order_by('-eventdate')
	if request.user.is_superuser:


		if request.method=="POST":
			id_list=request.POST.getlist('boxes')
			#uncheck all events

			event_list.update(approved=False)
			#update the database
			for x in id_list:
				Event.objects.filter(pk=int(x)).update(approved=True)

			messages.success(request,("Event list approval has been upadted"))
			return redirect('list-events')
		else:
			return render(request,'events/adminapproval.html',{
			'event_list':event_list,
			'eventcount':eventcount,
			'venuecount':venuecount,
			'usercount':usercount,
			'venuelist':venuelist,
			})

	else:
		messages.success(request,("you are authorized to use this page"))
		return redirect('home')
	return render(request,'events/adminapproval.html',{})

def search_events(request):
	if request.method == 'POST':
		searched=request.POST['searched']
		events=Event.objects.filter(description__contains=searched)
		return render(request,'events/search_venues.html',
		{'searched':searched,
		'events':events})
	else:

		return render(request,'events/searchevents.html',
		{})


def my_events(request):
	if request.user.is_authenticated:
		me = request.user.id
		events=Event.objects.filter(attedence=me)
		return render(request,'events/myevent.html',{
			"events":events,
			})
	else:
		messages.success(request,("your are not authorized to view this page"))
		return redirect('home')





#generate a pdf file

def venue_pdf(request):
	#create Bytestream buffer
	buf=io.BytesIO()
	#create canvas
	c=canvas.Canvas(buf,pagsize=letter,bottomup=0)
	#create a text object
	textob=c.beginText()
	textob.setTextOrigin(inch,inch)
	textob.setFont("Helvetica",14)

	#add some line of text
	#lines=["this is line 1",
	#"this is line 2"]

	venues=Venue.objects.all()
	#create a blank list
	lines=[]
	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.phone)
		lines.append(venue.web)
		lines.append(venue.zipcode)
		lines.append(venue.emailaddress)
		lines.append(" ")

	#for loop
	for line in lines:
		textob.textLine(line)
	#finish up

	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	#return something
	return FileResponse(buf,as_attachment=True,filename='venue.pdf')

#generate csv file for venue list
def venue_csv(request):
	response=HttpResponse(content_type="text/csv")
	response['Content-Disposition']='attachement;filename=venues.csv'

	#create a csv writer

	writer=csv.writer(response)
	
	#designate into  model
	venues=Venue.objects.all()


	#add column heading in csv file

	writer.writerow(['name','address','zipcode','phone','web','emailaddress'])

		#loop through output
	for venue in venues:
		writer.writerow([venue,venue.name,venue.address,venue.phone,venue.zipcode,venue.emailaddress,venue.web])

	return response


	





#generate text file for venue list
def venue_text(request):
	response=HttpResponse(content_type="text/plain")
	response['Content-Disposition']='attachement;filename=venue.txt'
	#lines=["this is line1\n",
	#"this is line2\n"]
	#write into text file
	#designate into  model
	venues=Venue.objects.all()
	lines=[]


	#loop through output
	for venue in venues:
		lines.append(f'{venue}\n{venue.name}\n{venue.address}\n{venue.phone}\n{venue.zipcode}\n{venue.emailaddress}\n{venue.web}')



	response.writelines(lines)
	return response

def delete_venue(request,venue_id):
	venue=Venue.objects.get(pk=venue_id)
	venue.delete()
	return redirect('list-venues')


def delete_event(request,event_id):
	event=Event.objects.get(pk=event_id)
	if request.user==event.manager:
		event.delete()
		messages.success(request,("Event Deleted!"))
		return redirect('list-events')
	else:
		messages.success(request,("your are not authorized to delete"))
		return redirect('list-events')






def add_event(request):
	submitted=False
	if request.method == "POST":
		#for anybody who can add evevnt we do
		#if request.uer.id=4: like this
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/addevent?submitted=True')
		else:
			form = EventForm(request.POST)
			
			if form.is_valid():
				event=form.save(commit=False)
				event.manager=request.user.id #looged in user
				event.save()
				return HttpResponseRedirect('/addevent?submitted=True')
	else:
		#just going into page not submiitteg
		if request.user.is_superuser:
			form=EventFormAdmin
		else:
			form = EventForm
		if'submitted' in request.GET:
			submitted=True
	return render(request,"events/addevent.html",
		{"form":form,
		"submitted":submitted
		})

def update_event(request,event_id):
	event=Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form=EventFormAdmin(request.POST or None,instance=event)
	else:
		form=EventForm(request.POST or None,instance=event)
	if form.is_valid():
		form.save()
		return redirect('list-events')

	return render(request,"events/update_event.html",
		{'event':event,
		"form":form})



def update_venue(request,venue_id):
	venue=Venue.objects.get(pk=venue_id)
	form=VenueForm(request.POST or None,request.FILES or None,instance=venue)
	if form.is_valid():
		form.save()
		return redirect('list-venues')

	return render(request,"events/update_venue.html",
		{'venue':venue,
		"form":form})



def search_venues(request):
	if request.method == 'POST':
		searched=request.POST['searched']
		venues=Venue.objects.filter(name__contains=searched)
		return render(request,'events/search_venues.html',
		{'searched':searched,
		'venues':venues})
	else:

		return render(request,'events/search_venues.html',
		{})




def show_venue(request, venue_id):

    # Fetch the venue or return a 404 if it doesn't exist
    venue = get_object_or_404(Venue, pk=venue_id)

    
    # Try to fetch the venue owner, handle the case where it doesn't exist
    try:
        venueowner = User.objects.get(pk=venue.owner)
    except User.DoesNotExist:
        venueowner = None  # Set to None if the owner does not exist



    #grab the events
    events=venue.event_set.all()
    return render(request, "events/show_venue.html", {
        'venue': venue,
        "venueowner": venueowner,
        "events":events,
    })



def list_venues(request):
	#venue_list=Venue.objects.all().order_by('?')  #everytime we open it gives random order
	venue_list=Venue.objects.all()   


	#set yup paginate
	p=Paginator(Venue.objects.all(),1)
	page=request.GET.get('page')
	venues=p.get_page(page)
	nums="a" * venues.paginator.num_pages  #make sure it is a string because when we give a number it 3 multiply that times


	return render(request,"events/venue.html",
		{'venue_list':venue_list,
		'venues':venues,
		"nums":nums})



def all_events(request):
	event_list=Event.objects.all().order_by('-eventdate')
	return render(request,"events/event_list.html",
		{'event_list':event_list})






def add_venue(request):
	submitted=False
	if request.method == "POST":
		form = VenueForm(request.POST,request.FILES)
		if form.is_valid():
			venue=form.save(commit=False)
			#form.save()
			venue.owner=request.user.id #looged in user
			venue.save()
			return HttpResponseRedirect('/addvenue?submitted=True')
	else:
		form=VenueForm
		if'submitted' in request.GET:
			submitted=True
	return render(request,"events/addvenue.html",
		{"form":form,
		"submitted":submitted
		})




def home(request,year=datetime.now().year,month=datetime.now().strftime("%B")):
	name="navya"
	#convert into uppercase title the month
	#month=month.title() or this

	month=month.capitalize()

	#convert month from name to number

	monthnumber=list(calendar.month_name).index(month)

	#to check whether it is actual integer or string 
	#or to convert it into exact integer
	monthnumber=int(monthnumber)

	#create a calendar

	cal=HTMLCalendar().formatmonth(year,monthnumber)

	#get current year

	now=datetime.now()
	currentyear=now.year



	#query eventmodel by date

	event_list=Event.objects.filter(
		#event_date__year=datetime.now().year   one way
		eventdate__year=year,
		eventdate__month=monthnumber
		)
	#get current time
	time=now.strftime('%I:%M:%S:%p')

	return render(request,"events/home.html",{
		"name":name,
		"year":year,
		"month":month,
		"monthnumber":monthnumber,
		"cal":cal,
		"currentyear":currentyear,
		"time":time,
		"event_list":event_list
		})

