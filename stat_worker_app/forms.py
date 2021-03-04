"""
    Links a model to a form.
"""

from django import forms

from .models import ComputeRequestModel


class ComputeRequestForm(forms.ModelForm):
    """
        Represents a container for the form of an compute resquests.

        Most of it's the content of it will be build without djangos form templates.
    """

    class Meta:
        model = ComputeRequestModel
        fields = ['method', 'source', 'file', 'data1', 'data2']
