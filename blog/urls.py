from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^blog/$', views.blog, name='blog_blog'),
]
