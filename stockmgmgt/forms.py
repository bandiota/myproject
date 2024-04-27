from django import forms
from.models import *

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'item_code', 'quantity', 'unit']
    

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        return category

    def clean_item_code(self):
        item_code = self.cleaned_data.get('item_code')
        if not item_code:
            raise forms.ValidationError('This field is required')
        return item_code
    

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name



class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['category', 'item_name',]

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'unit']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields  = ['issue_quantity', 'unit', 'issue_to']

class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity', 'unit']

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']

class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    class Meta:
        model = StockHistory
        fields = ('category', 'item_name', 'start_date','end_date')

class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ["name",]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('This field is required')
        for  category in Category.objects.all():
            if category.name == name:
                raise forms.ValidationError("Category with this name already exists")
        return name



class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ["name",]