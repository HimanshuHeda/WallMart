from django import forms
from ecom.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['customer', 'product','placedorder','image','shipped','delivery','deliverydate','paymentstatus','date','quantity']  # Exclude the user and product fields from the form
