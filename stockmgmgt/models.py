from django.db import models


unit_choice = (
		('Kg', 'Kg'),
		('g', 'g'),
		('pcs', 'pcs'),
        ('Liter' , 'Liter'),
        ('mL', 'mL'),
        ('pack', 'pack'),
	)


class Category(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	def __str__(self):
		return self.name
      
class Stock(models.Model):
	category            =   models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	item_name           =   models.CharField(max_length=50, blank=True, null=True)
	item_code			=	models.CharField(max_length=12, blank=True, null=True)
	quantity            =   models.IntegerField(default='0', blank=True, null=True)
	receive_quantity    =   models.IntegerField(default='0', blank=True, null= True)
	receive_by          =   models.CharField(max_length=50, blank=True, null= True)
	issue_quantity      =   models.IntegerField(default='0', blank=True, null= True)
	issue_by            =   models.CharField(max_length=50, blank=True, null= True)
	issue_to            =   models.CharField(max_length=50, blank=True, null= True)
	phone_number        =   models.IntegerField(blank=True, null= True)
	created_by          =   models.CharField(max_length=50, blank=True, null= True)
	reorder_level       =   models.IntegerField(default='0', blank=True, null= True)
	last_updated        =   models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp           =   models.DateTimeField(auto_now_add=True, auto_now=False)
	unit                = 	models.CharField(choices=unit_choice, max_length=20, blank=True)
    
	def __str__(self):
		return self.item_name +  " (Quantity = "+ str(self.quantity) + self.unit + ")"
    

class StockHistory(models.Model):
	category 			= models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	item_name 			= models.CharField(max_length=50, blank=True, null=True)
	quantity 			= models.IntegerField(default='0', blank=True, null=True)
	receive_quantity 	= models.IntegerField(default='0', blank=True, null=True)
	receive_by 			= models.CharField(max_length=50, blank=True, null=True)
	issue_quantity 		= models.IntegerField(default='0', blank=True, null=True)
	issue_by 			= models.CharField(max_length=50, blank=True, null=True)
	issue_to 			= models.CharField(max_length=50, blank=True, null=True)
	phone_number 		= models.CharField(max_length=50, blank=True, null=True)
	created_by 			= models.CharField(max_length=50, blank=True, null=True)
	reorder_level 		= models.IntegerField(default='0', blank=True, null=True)
	last_updated 		= models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	timestamp 			= models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	unit        		= models.CharField(choices=unit_choice, max_length=20, blank=True, null=True)
