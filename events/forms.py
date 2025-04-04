from django import forms
#everything is model so it is a modelform from  model only that we register on venue 
from django.forms import ModelForm

from .models import Venue,Event
#create a venue form

class VenueForm(ModelForm):
	class Meta:
		#meta is just a django thing not pyhton
		model=Venue
		#for all fields in venue table
		#fields="__all__"
		fields=('name','address','zipcode','phone','web','emailaddress','venueimage')
		labels={
			'name':'Enter your name here', 
			"address":'Enter adress',
			"zipcode":'',
			"phone":'',
			"web":'',
			"emailaddress":'',
			"venueimage":'',
		}
		widgets={
			'name':forms.TextInput(attrs={"class":"form-control",'placeholder':" Venuename"}) , #form control is a boostrap thing
			"address":forms.TextInput(attrs={'class':'form-control','placeholder':"address "}),
			"zipcode":forms.TextInput(attrs={'class':'form-control','placeholder':" zipcode"}),
			"phone":forms.TextInput(attrs={'class':'form-control','placeholder':"phone "}),
			"web":forms.TextInput(attrs={'class':'form-control','placeholder':" web"}),
			"emailaddress":forms.TextInput(attrs={'class':'form-control','placeholder':" emailaddress"}),
		}


#admin superuser form

class EventFormAdmin(ModelForm):
	class Meta:
		#meta is just a django thing not pyhton
		model=Event
		#for all fields in venue table
		#fields="__all__"
		fields=('name','eventdate','venue','manager','attedence','description')
		labels={
			'name':'Enter your name here', 
			"eventdate":'YYYY-MM-DD HH:MM:SS',
			"venue":'venue',
			'manager':'manager',
			"attedence":'attedence',
			"description":'',
			
		}
		widgets={
			'name':forms.TextInput(attrs={"class":"form-control",'placeholder':" eventname"}) , #form control is a boostrap thing
			"eventdate":forms.TextInput(attrs={'class':'form-control','placeholder':"date"}),
			"venue":forms.Select(attrs={'class':'form-select','placeholder':" venue"}),
			"manager":forms.Select(attrs={'class':'form-select','placeholder':"manager "}),
			"attedence":forms.SelectMultiple(attrs={'class':'form-control','placeholder':" attedence"}),
			"description":forms.Textarea(attrs={'class':'form-control','placeholder':" description"}),
			
		}


#user event form


class EventForm(ModelForm):
	class Meta:
		#meta is just a django thing not pyhton
		model=Event
		#for all fields in venue table
		#fields="__all__"
		fields=('name','eventdate','venue','attedence','description')
		labels={
			'name':'Enter your name here', 
			"eventdate":'YYYY-MM-DD HH:MM:SS',
			"venue":'venue',
			"attedence":'attedence',
			"description":'',
			
		}
		widgets={
			'name':forms.TextInput(attrs={"class":"form-control",'placeholder':" eventname"}) , #form control is a boostrap thing
			"eventdate":forms.TextInput(attrs={'class':'form-control','placeholder':"date"}),
			"venue":forms.Select(attrs={'class':'form-select','placeholder':" venue"}),

			"attedence":forms.SelectMultiple(attrs={'class':'form-control','placeholder':" attedence"}),
			"description":forms.Textarea(attrs={'class':'form-control','placeholder':" description"}),
			
		}
