from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        # Add classes to form fields
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control custom-file-input', 'id': 'customFile'})

    class Meta:
        model = Message
        fields = ['content', 'file']