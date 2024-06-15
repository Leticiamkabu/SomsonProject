from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('services/', views.services, name='services'),
    path('contact-us/', views.contact, name="contact"),
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('unsubscribe-newsletter/', views.unsubscribe_newsletter, name='unsubscribe_newsletter'), 
    path('request-estimate/', views.request_estimate, name='request_estimate'),
    path('faqs/',views.faqs,name='faqs'),
    path('req-estimate/',views.request_short_estimate,name='request_short_estimate'),
    path('send_bulk_email_test/', views.send_bulk_email, name='send_bulk_email_test')
]