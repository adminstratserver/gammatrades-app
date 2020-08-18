from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from members.models import account_activation_token
from members.models import Member
from django.views.generic import View
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from listings.models import Product
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
import os

@login_required
def blank(request):
    if request.user.is_authenticated:
        context = {"title": "BLANK"}
        return render(request, "hbi-dashboard/blank.html", context)

def about_page(request):
    return render(request, "about.html", {"title": "About"})


def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        #print(form.cleaned_data)
        form = ContactForm()
    context = {
        "title": "Contact us", 
        "form": form
    }
    return render(request, "form.html", context)


def nav(request):
    context = {"title": "NAV"}
    return render(request, 'hbi-homepage/base.html', context)


def gallery(request):
    #print('HERE at gallery')
    DEBUG1 = os.environ.get('TESTDATA')
    print("DEBUG1",DEBUG1)
    qs = Product.objects.filter(is_published=True, type="eproof")
    context = {
        "title": "GammaTrades Gallery",
        "listings": qs,
        "debug": DEBUG1
    }
    #print('1. qs=',qs)
    return render(request, 'hbi-homepage/gallery.html', context)


def index(request):
    if request.user.is_authenticated:
        my_qs = Member.objects.filter(username=request.user)
        context = {"title": "GammaTrades", 'blog_list': my_qs}
        return redirect('alldocuments')
    else:
        context = {"title": "GammaTrades"}
        return render(request, "hbi-homepage/index.html", context)

