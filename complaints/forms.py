from django import forms
from .models import Complaint, ComplaintStatusLog, Feedback

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'department', 'priority', 'subject', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brief title summarizing your grievance'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'Provide clear details including date, location, course, or individuals involved...'}),
        }


class StatusUpdateForm(forms.Form):
    status = forms.ChoiceField(choices=Complaint.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Add staff resolution notes or comments (visible to student)'}))


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Optional feedback on resolution speed and quality'}),
        }
