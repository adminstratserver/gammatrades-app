from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'salesrep', 'country', 'agent')
  list_display_links = ('name', 'salesrep', 'country', 'agent')
  list_filter = ('name', 'salesrep', 'country', 'agent')
  search_fields = ('name', 'salesrep', 'country', 'agent')
  list_per_page = 20

admin.site.register(Customer, CustomerAdmin)

