from django import forms
from gateway.models import View_lp

class DataSend(forms.ModelForm):
     class Meta:
          model = View_lp
          fields="__all__"
