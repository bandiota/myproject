from django.contrib import admin
from.models import *
from.forms import *

class StockCreateAdmin(admin.ModelAdmin):
    list_display    =   ['category', 'item_name', 'quantity', 'unit']
    form            =   StockCreateForm
    list_filter     =   ['category']
    search_fields   =   ['category', 'item_name']


admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)
admin.site.register(StockHistory)