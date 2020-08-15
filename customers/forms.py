from django.forms import ModelForm
from .models import Customer

class EditCustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['salesrep', 'date_created']

class CreateCustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['salesrep', 'date_created']

