from django.contrib import admin

from .models import Venue
from .models import MyClubUser
from .models import Event
from django.contrib.auth.models import Group

#.means in this directory we should go

#admin.site.register(Venue,Venueadmin)
admin.site.register(MyClubUser)


#remove Groups

admin.site.unregister(Group)





#admin.site.register(Event)

#push into database


#instead this @admin we simply use it in ()
@admin.register(Venue)
class Venueadmin(admin.ModelAdmin):
	list_display=('name','address','phone')
	#alphabetical order
	#ordering=('name',)
	#for reverse
	ordering=('-name',)
	search_fields=("name","address")



@admin.register(Event)
class Eventadmin(admin.ModelAdmin):

	#to change the data is called fields
	fields=(('name','venue'),'eventdate','description','manager','approved')
	list_display=('name','eventdate','venue')
	list_filter=('eventdate','venue')
	ordering=('-eventdate',)