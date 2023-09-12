from django import forms


# QUANTITY_CHOICES = [(i, i) for i in range(1, 10)]
# QUANTITY_CHOICES = [
#     (1, '1'),
#     (2, '2'),
#     (3, '3'),
#     ...
#     (9, '9'),
# ]

class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int, label='Количество')
    quantity = forms.IntegerField(max_value=1000, label='Количество')
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    