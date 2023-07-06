from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Leads


class AddRecordForm(forms.ModelForm):
    STATUS = (
        ('Active Leads', 'Active'),
        ('Dead Leads', 'Dead'),
    )
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "First Name", "class": "form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Last Name", "class": "form-control"}), label="")
    contact = forms.CharField(required=True,
                           widget=forms.widgets.TextInput(attrs={"placeholder": "Contact", "class": "form-control"}),
                           label="")
    email = forms.EmailField(required=True,
                            widget=forms.widgets.TextInput(attrs={"placeholder": "Email", "class": "form-control"}),
                            label="")
    csv_file = forms.FileField(required=False)
    country = forms.CharField(required=True,
                            widget=forms.widgets.TextInput(attrs={"placeholder": "Country", "class": "form-control"}),
                            label="")
    industry = forms.CharField(required=True,
                              widget=forms.widgets.TextInput(attrs={"placeholder": "Industry", "class": "form-control"}),
                              label="")
    # created_at = forms.DateField(required=True,
    #                           widget=forms.widgets.TextInput(attrs={"placeholder": "Date", "class": "form-control"}),
    #                           label="")
    status = forms.ChoiceField(required=True,choices=STATUS,
                               widget=forms.widgets.TextInput(
                                   attrs={"placeholder": "Status", "class": "form-control"}),
                               label="")

    class Meta:
        model = Leads
        exclude = ("user",)



