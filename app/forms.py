from django import forms


class CheckoutForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        label="Full Name",
        widget=forms.TextInput(attrs={"placeholder": "Full Name", "class": "input input-bordered w-full"}),
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "input input-bordered w-full"}),
    )
    phone = forms.CharField(
        max_length=20,
        label="Contact Number",
        widget=forms.TextInput(attrs={"placeholder": "03XX-XXXXXXX", "class": "input input-bordered w-full"}),
    )
    delivery_address = forms.CharField(
        label="Delivery Address",
        widget=forms.Textarea(attrs={
            "placeholder": "Street, City, Province, ZIP",
            "class": "textarea textarea-bordered w-full",
            "rows": 3,
        }),
    )
    # Hidden field: 'standard' or 'whatsapp'
    order_type = forms.CharField(widget=forms.HiddenInput(), initial="standard")
