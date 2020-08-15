from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'contributor', 'type', 'is_published', 'list_date')
  list_display_links = ('title', 'type')
  search_fields = ('title', 'contributor', 'type', 'is_published')
  list_per_page = 25

admin.site.register(Product, ProductAdmin)
