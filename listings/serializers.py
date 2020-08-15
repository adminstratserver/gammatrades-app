from rest_framework import serializers
from .models import Product

class ListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'title', 'type', 'list_date', 'is_published']
		#fields = ['id', 'title', 'type', 'is_published']

