from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('',                            views.index,                 name='index'),
    path('actualites/',                 views.actualites,            name='actualites'),
    path('actualites/<slug:slug>/',     views.actualite_detail,      name='actualite_detail'),
    path('newsletter/inscription/',     views.newsletter_inscription, name='newsletter_inscription'),
    path('contact/',                    views.contact,               name='contact'),


    path('parlement/',                  views.parlement,              name='parlement'),
    path('circonscription/',            views.circonscription,        name='circonscription'),
    path('agenda/',                     views.agenda,                 name='agenda'),

]