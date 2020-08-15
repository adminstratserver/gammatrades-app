from django.shortcuts import render, get_object_or_404, redirect
from .forms import EditCustomerForm, CreateCustomerForm
from .models import Customer
from members.models import Member

def delete_customer(request, customer_id):
    selected_customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == "POST":
        #print('Here at delete customer')
        selected_customer.delete()
        return redirect('home')

    context = {'item': selected_customer,
               'title': 'Delete Customer',
              }
    return render(request, 'hbi-dashboard/delete_customer.html', context)

def create_customer(request):
    form = CreateCustomerForm()

    if request.method == 'POST':
        form = EditCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            #print('1. form name=', form.cleaned_data['name'])
            #print('2. form country=', form.cleaned_data['country'])
            #print('3. form agent=', form.cleaned_data['agent'])
            form.save()
            selected_customer = get_object_or_404(Customer, name=form.cleaned_data['name'])
            my_qs = Member.objects.filter(username=request.user)
            selected_customer.salesrep = my_qs[0]  #assign a Member object into selected_customer.salesrep
            selected_customer.save()
            return redirect('home')
        else:
            return redirect('home')
    context = {'form':form,
               'title': 'New Customer Profile',
              }
    return render(request, 'hbi-dashboard/create_customer.html', context)



def edit_customer(request, customer_id):
    selected_customer = get_object_or_404(Customer, pk=customer_id)
    form = EditCustomerForm(instance=selected_customer)

    if request.method == 'POST':
        form = EditCustomerForm(request.POST, request.FILES, instance=selected_customer)
        if form.is_valid():
            #print('1. form name=', form.cleaned_data['name'])
            #print('2. form salesrep=', form.cleaned_data['salesrep'])
            #print('3. form country=', form.cleaned_data['country'])
            #print('4. form agent=', form.cleaned_data['agent'])
            form.save()
            return redirect('home')
        else:
            return redirect('home')
    context = {'form':form,
               'title': 'Edit Customer Profile',
               'customer': selected_customer
              }
    return render(request, 'hbi-dashboard/edit_customer.html', context)


def mycustomers(request):
    my_customers = Customer.objects.filter(salesrep=request.user)
    #print ('mycustomers =',my_customers)

    context = {
                'title': 'My Customers',
                'my_customers' : my_customers,
              }
    return render(request, 'hbi-dashboard/mycustomerlist.html', context)
