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
def contacts(request):
    return render(request, 'contacts.html')

