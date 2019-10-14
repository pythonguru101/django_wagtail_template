from django.db import models
from show.models import PrintSeries
from home.models import OverviewPage, ComplexPage


def published_series(request):
    published_series = PrintSeries.objects.live().filter(show_in_menus=True)
    return {
        'published_series': published_series,
    }


def other_pages(request):
    other_pages = ComplexPage.objects.live().filter(show_in_menus=True)
    return {
        'other_pages': other_pages,
    }
