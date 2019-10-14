from django.conf.urls import url

from show import views

urlpatterns = [
    url(r'^multi_slide/$', views.multi_slide, name='home_multi_slide'),
    url(r'^carousel/$', views.carousel, name='home_carousel'),
    url(r'^impulse_image/$', views.impulse_image, name='home_impulse_image'),
    url(r'^fullscreen_image/$', views.fullscreen_image, name='home_fullscreen_image'),
    url(r'^fullscreen_slide/$', views.fullscreen_slide, name='home_fullscreen_slide'),
    url(r'^fullscreen_slide_show/$', views.fullscreen_slide_show, name='home_fullscreen_slide_show'),
    url(r'^video/$', views.video, name='home_video'),
]
