from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'post_tag']

    def clean_post_tag(self):
        tags = self.cleaned_data.get('post_tag')

        # tags = 'hs'
        tags = tags.strip()
        tags = tags.replace(' ', '')
        tags = tags.replace('#', '-')
        tags = tags.lower()

        return tags