from django.conf.urls import url

from about import views

urlpatterns = [
    url(r'^studio/$', views.studio, name='about_studio'),
    url(r'^personal/$', views.personal, name='about_personal'),
]
