from django import forms
from .models import Candidate


class CandidateRegister(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'middle_name', 'last_name', 'skills']
