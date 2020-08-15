from django.forms import ModelForm
from .models import Product
from django import forms


class UploadEproofForm(ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'description', 'document_file', 'image2_file', 'image3_file', 'list_date']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'eproof_title', 'placeholder': 'Type Eproof Title Here', 'required size':'10'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
			'document_file': forms.FileInput(attrs={'class': 'form-control', 'id': 'eproof_document_id'}),
			'image2_file': forms.FileInput(attrs={'class': 'form-control'}),
			'image3_file': forms.FileInput(attrs={'class': 'form-control'}),
			'list_date': forms.HiddenInput()

		}

class UploadBrochureForm(ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'description', 'document_file', 'cover_file', 'image1_file', 'image2_file', 'image3_file', 'list_date']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'eproof_title', 'placeholder': 'Type Brochure Title Here'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
			'document_file': forms.FileInput(attrs={'class': 'form-control', 'id': 'eproof_document_id'}),
			'cover_file': forms.FileInput(attrs={'class': 'form-control'}),
			'list_date': forms.HiddenInput()
		}

class EditBrochureForm(ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'description', 'document_file', 'cover_file', 'image1_file', 'image2_file', 'image3_file']

		widgets = {
			'title': forms.TextInput(
				attrs={'required size': '45'}),
		}




