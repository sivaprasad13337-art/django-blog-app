from django import forms
from .models import CommentsModel

class CommentsForm(forms.ModelForm):
    class Meta:
        model = CommentsModel
        fields = ['content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': '!h-10 bg-gray-600 p-2 rounded-full placeholder-gray-300 outline-gray-400',
                'style': 'height:40px; outline-color: gray; width: 90%',
                'id': 'input-bar'
            })

        self.fields['content'].widget.attrs['placeholder'] = 'Comment here...'