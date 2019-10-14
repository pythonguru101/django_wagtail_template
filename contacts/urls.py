from django.conf.urls import url

from contacts import views

urlpatterns = [
    url(r'^contacts/$', views.contacts, name='contacts_contacts'),
]
