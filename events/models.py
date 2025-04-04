
from django.db import models
#user authenication 

from django.contrib.auth.models import User
from datetime import date




class Venue(models.Model):
	name=models.CharField('Venue Name',max_length=120)
	address=models.CharField(max_length=300)
	zipcode=models.CharField('zip code',max_length=15)
	phone=models.CharField('Contact phone',max_length=25,blank=True)
	web=models.URLField('Website Address',blank=True)
	emailaddress=models.EmailField('Email Address',blank=True)
	owner=models.IntegerField("Venue Owner",blank=False,default=2)#admin user no=2
	venueimage=models.ImageField(null=True,blank=True,upload_to="images/")

	def __str__(self):
		return self.name

#we want many user connect to many events
#many to many relationship


class MyClubUser(models.Model):
	firstname=models.CharField(max_length=30)
	lastname=models.CharField(max_length=120)
	email=models.EmailField("UserEmail")

def __str__(self):
		return self.first.name + ' ' + self.lastname



# Create your models here.
#create table


class Event(models.Model):
	name=models.CharField('Event Name',max_length=120)
	eventdate=models.DateTimeField('Event Date')
	#to connect with venue table
	venue=models.ForeignKey(Venue,blank=True,null=True,on_delete=models.CASCADE)
	#venue=models.CharField(maxlength=120)
	#manager=models.CharField(max_length=60)

	#making manager as admin
	
	manager=models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
	description=models.TextField(blank=True)

#we dont use forign key because we dont have one relation one event have one venue 
	attedence=models.ManyToManyField( MyClubUser,blank=True,)
	approved=models.BooleanField("Approved",default=False)

#it allows to use in admin area we created
# allow to pop up on the page
	def __str__(self):
		return self.name



	@property
	def days_till(self):
		today=date.today()
		days_till=self.eventdate.date()-today
		daystillstripped=str(days_till).split(",",1)[0]
		return daystillstripped
	


	@property
	def ispast(self):
			today=date.today()
			if self.eventdate.date()<today:
				thing="past"
			else:
				thing="future"
			return thing