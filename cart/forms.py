from django import forms


class CartAddProductForm(forms.Form):
    
    quantity = forms.IntegerField(
        max_value=1000, 
        min_value=1,
        label='Количество',
        widget=forms.NumberInput(attrs={'style':'width:80px', 'id':'quantity', 'onchange':"sendCount(this)"}),
        initial=1
        )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    