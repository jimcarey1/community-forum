from django import forms
from .models import Thread, Comment
from django.forms.widgets import Textarea

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'class': 'w-full bg-gray-800 border-gray-700 rounded-md'})
        }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['content'].widget.attrs.update({
                'placeholder':'What are your thoughts'
            })
            self.fields['content'].label = False

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content']
        widgets = {
            'content': Textarea(attrs={'class': 'w-full bg-gray-800 border-gray-700 rounded-md'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind CSS classes and placeholders to the title field
        self.fields['title'].widget.attrs.update({
            'class': 'mt-1 block w-full h-20 px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Title'
        })
        # Remove the label for the title field
        self.fields['title'].label = False

        # Apply placeholder to the content field (CKEditor5Widget already handles most styling)
        self.fields['content'].widget.attrs.update({
            'placeholder': 'Content'
        })
        # Remove the label for the content field
        self.fields['content'].label = False