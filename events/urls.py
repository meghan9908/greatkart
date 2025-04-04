                                                                                                                                                       

from django.urls import path
from . import views
urlpatterns = [
#path converters
#int:numbers
#str:strings
#path:who;e urls/
#slugs:hypen-and underscores stuff
#uuid:universally unique identifiers

    path('',views.home,name="home"),
    path('<int:year>/<str:month>/',views.home,name="home"),
    path('events',views.all_events,name="list-events"),
    path('addvenue',views.add_venue,name="add_venue"),
    path('list_venues',views.list_venues,name="list-venues"),
    path('show_venue/<venue_id>',views.show_venue,name="show-venue"), #default create a id like 1,2,3
    path('search_venues',views.search_venues,name="search-venues"),
    path('update_venue/<venue_id>',views.update_venue,name="update-venue"),
    path('addevent',views.add_event,name="add-event"),
    path('update_event/<event_id>',views.update_event,name="update-event"),
    path('delete_event/<event_id>',views.delete_event,name="delete-event"),
    path('delete_venue/<venue_id>',views.delete_venue,name="delete-venue"),
    path('venue_text',views.venue_text,name="venue-text"),
    path('venue_csv',views.venue_csv,name="venue-csv"),
    path('venue_pdf',views.venue_pdf,name="venue-pdf"),
    path('my_events',views.my_events,name="my-events"),
    path('search_events',views.search_events,name="search-events"),
    path('admin approval',views.admin_approval,name="admin-approval"),
      path('venue_event/<venue_id>',views.venue_event,name="venue-event"),
       path('show_event/<event_id>',views.show_event,name="show-event"),

]

