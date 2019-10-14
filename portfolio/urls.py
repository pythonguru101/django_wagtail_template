from django.conf.urls import url

from portfolio import views

urlpatterns = [
    url(r'^fullscreen_grid/$', views.fullscreen_grid, name='portfolio_fullscreen_grid'),
    url(r'^horizontal2/$', views.horizontal2, name='portfolio_horizontal2'),
    url(r'^horizontal3/$', views.horizontal3, name='portfolio_horizontal3'),
    url(r'^horizontal1/$', views.horizontal1, name='portfolio_horizontal1'),
    url(r'^boxed_grid/$', views.boxed_grid, name='portfolio_boxed_grid'),
    url(r'^column_grid/$', views.column_grid, name='portfolio_column_grid'),
    url(r'^column_grid2/$', views.column_grid2, name='portfolio_column_grid2'),
    url(r'^style1/$', views.style1, name='portfolio_style1'),
    url(r'^style2/$', views.style2, name='portfolio_style2'),
    url(r'^style3/$', views.style3, name='portfolio_style3'),
    url(r'^style4/$', views.style4, name='portfolio_style4'),
    url(r'^style5/$', views.style5, name='portfolio_style5'),
    url(r'^style6/$', views.style6, name='portfolio_style6'),
    url(r'^style7/$', views.style7, name='portfolio_style7'),
]
