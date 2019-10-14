from django.conf.urls import url

from service import views

urlpatterns = [
    url(r'^service/$', views.service, name='service_service'),
]
