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
def multi_slide(request):
    return render(request, 'home/index2.html')


@csrf_exempt
def carousel(request):
    return render(request, 'home/index8.html')


@csrf_exempt
def impulse_image(request):
    return render(request, 'home/index3.html')


@csrf_exempt
def fullscreen_image(request):
    return render(request, 'home/index4.html')


@csrf_exempt
def fullscreen_slide(request):
    return render(request, 'home/index5.html')


@csrf_exempt
def fullscreen_slide_show(request):
    return render(request, 'home/index6.html')


@csrf_exempt
def video(request):
    return render(request, 'home/index7.html')

