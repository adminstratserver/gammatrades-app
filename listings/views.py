from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from django.contrib.auth.decorators import login_required
from .models import Product
from members.models import Member
from .forms import UploadEproofForm, UploadBrochureForm, EditBrochureForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ListingSerializer


@login_required
def mydocuments(request):
    if request.user.is_authenticated:
        context = {"title": "My Documents"}
        return render(request, "hbi-dashboard/mydocuments.html", context)

@api_view(['GET'])
def mydocumentsOverview(request):
    api_urls = {
        'List':'/task-list/',
        'Detail View':'/task-detail/<str:pk>/',
        'Create':'/task-create/',
        'Update':'/task-update/<str:pk>/',
        'Delete':'/task-delete/<str:pk>/',
        }
    return Response(api_urls)

@api_view(['GET'])
def mydocumentstaskList(request):
    #tasks = Product.objects.all().order_by('-id')
    my_qs = Member.objects.filter(username=request.user)
    tasks = Product.objects.filter(contributor=my_qs[0])
    serializer = ListingSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def mydocumentstaskDetail(request, pk):
    tasks = Product.objects.get(id=pk)
    serializer = ListingSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def mydocumentstaskCreate(request):
    serializer = ListingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def mydocumentstaskUpdate(request, pk):
    task = Product.objects.get(id=pk)
    serializer = ListingSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        #print('Serializer is valid')
        serializer.save()
    else:
        pass
        #print('ERROR: Serializer is NOT valid')
    return Response(serializer.data)

@api_view(['DELETE'])
def mydocumentstaskDelete(request, pk):
    task = Product.objects.get(id=pk)
    task.delete()
    return Response('Item succsesfully delete!')





@login_required
def alldocuments(request):
    if request.user.is_authenticated:
        qs = Product.objects.order_by('-list_date').filter(is_published=True)
        paginator = Paginator(qs, 4)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)
        context = {"title": "All Documents",
                   'listings': paged_listings
                  }
        return render(request, "hbi-dashboard/alldocuments.html", context)



@login_required
def alldocumentsbytype(request, product_type):                 #display items based on type
    if request.user.is_authenticated:
        qs = Product.objects.order_by('-list_date').filter(is_published=True, type=product_type)
        paginator = Paginator(qs, 4)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)
        context = {"title": str(product_type).title() + " Documents",
                   'listings': paged_listings
                   }
        return render(request, "hbi-dashboard/alldocuments.html", context)


@login_required
def selecteddocument(request, listing_id):                 #display individual items
  listing = get_object_or_404(Product, pk=listing_id)
  context = {
    'title': 'Document:',
    'listing': listing
  }
  return render(request, 'hbi-dashboard/selecteddocument.html', context)


@login_required
def edit_document(request, listing_id):
    selected_document = get_object_or_404(Product, pk=listing_id)
    #print ('selected_document.type=', selected_document.type)
    form = EditBrochureForm(instance=selected_document)

    if request.method == 'POST':
        form = EditBrochureForm(request.POST, request.FILES, instance=selected_document)
        if form.is_valid():
            #print('1. form title=', form.cleaned_data['title'])
            #print('2. form description=', form.cleaned_data['description'])
            form.save()
            return redirect('home')
        else:
            return redirect('home')

    else:
        context = {'form':form,
                   'selected_document': selected_document,
                   'title': 'Edit Document',
                   'subtitle': selected_document.title,
                }
        if selected_document.type == "eproof":
            #print ('1. selected_document=', selected_document)
            return render(request, 'hbi-dashboard/edit_eproof.html', context)
        else:
            return render(request, 'hbi-dashboard/edit_brochure.html', context)

@login_required
def upload_eproof(request):
    if request.method == 'POST':
        #print('at request.method==POST')
        form = UploadEproofForm(request.POST, request.FILES)
        if form.is_valid():
            #print('form is valid')
            form.save()
            #selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            #print('1. object title=', selected_item.title)
            #print('2. object document_file=', selected_item.document_file)
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
            selected_item.cover_file = selected_item.document_file
            selected_item.image1_file = selected_item.document_file
            selected_item.type = 'eproof'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadEproofForm()
        context = {"title": "Upload EProof Document",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_eproof.html', context)



@login_required
def upload_brochure(request):
    if request.method == 'POST':
        form = UploadBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]
            selected_item.type = 'brochure'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadBrochureForm()
        context = {"title": "Upload Brochure Document",
                   "type": "Brochure",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_brochure.html', context)

@login_required
def upload_certificate(request):
    if request.method == 'POST':
        form = UploadBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]
            selected_item.type = 'certificate'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadBrochureForm()
        context = {"title": "Upload Certificate Document",
                   "type": "Certificate",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_brochure.html', context)

@login_required
def upload_manual(request):
    if request.method == 'POST':
        form = UploadBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]
            selected_item.type = 'manual'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadBrochureForm()
        context = {"title": "Upload Manual Document",
                   "type": "Manual",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_brochure.html', context)

@login_required
def upload_powerpoint(request):
    if request.method == 'POST':
        form = UploadBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]
            selected_item.type = 'powerpoint'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadBrochureForm()
        context = {"title": "Upload Powerpoint Document",
                   "type": "Powerpoint",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_brochure.html', context)

@login_required
def upload_proposal(request):
    if request.method == 'POST':
        form = UploadBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]
            selected_item.type = 'proposal'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadBrochureForm()
        context = {"title": "Upload Proposal Document",
                   "type": "Proposal",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_brochure.html', context)

def search(request):
  queryset_list = Product.objects.order_by('-list_date')
  #print('1. queryset_list=',queryset_list)

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  context = {
    'title': 'Search Results: ' + keywords,
    'listings': queryset_list,
  }
  return render(request, 'hbi-dashboard/alldocuments.html', context)

#BTRE functions ################################################################################################################

def search_OLD(request):
  queryset_list = Product.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)

  # State
  if 'state' in request.GET:
    state = request.GET['state']
    if state:
      queryset_list = queryset_list.filter(state__iexact=state)

  # Bedrooms
  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # Price
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'state_choices': state_choices,
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET
  }
  return render(request, 'listings/search.html', context)