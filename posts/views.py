from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from posts.models import Post

class PostView(ListView):
    model = Post
    queryset = Post.objects.all()
    context_object_name = 'posts'

    def head(self, *args, **kwargs):
        last_post = self.get_queryset().latest('created_at')
        response = HttpResponse('')
        # RFC 1123 date format
        response['Last-Modified'] = last_post.created_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

class PostDetailView(DetailView):

    queryset = Post.objects.all()

    def get_object(self):
        object = super(PostDetailView, self).get_object()
        return object
