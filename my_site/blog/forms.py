from django.forms import (Form,
                          ModelForm,
                          CharField,
                          EmailField,
                          Textarea)
from .models import Comment


class EmailPostForm(Form):
    name = CharField(max_length=32)
    email = EmailField()
    to = EmailField()
    comments = CharField(required=False, widget=Textarea)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
