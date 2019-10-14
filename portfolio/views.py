from django.shortcuts import get_object_or_404, render, redirect

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    from django.middleware.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django_xhtml2pdf.utils import generate_pdf
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.timezone import now


@csrf_exempt
def fullscreen_grid(request):
    return render(request, 'portfolio.html')


@csrf_exempt
def horizontal2(request):
    return render(request, 'portfolio2.html')


@csrf_exempt
def horizontal3(request):
    return render(request, 'portfolio5.html')


@csrf_exempt
def horizontal1(request):
    return render(request, 'portfolio6.html')


@csrf_exempt
def boxed_grid(request):
    return render(request, 'portfolio3.html')


@csrf_exempt
def column_grid(request):
    return render(request, 'portfolio4.html')


@csrf_exempt
def column_grid2(request):
    return render(request, 'portfolio7.html')


@csrf_exempt
def style1(request):
    return render(request, 'portfolio-single.html')


@csrf_exempt
def style2(request):
    return render(request, 'portfolio-single2.html')


@csrf_exempt
def style3(request):
    return render(request, 'portfolio-single3.html')


@csrf_exempt
def style4(request):
    return render(request, 'portfolio-single4.html')


@csrf_exempt
def style5(request):
    return render(request, 'portfolio-single5.html')


@csrf_exempt
def style6(request):
    return render(request, 'portfolio-single6.html')


@csrf_exempt
def style7(request):
    return render(request, 'portfolio-single7.html')
