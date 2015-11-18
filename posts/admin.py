from django.contrib import admin
from posts.models import Caption, Post, Comment, CaptionVote, CommentVote


admin.site.register([Caption, Post, Comment, CaptionVote, CommentVote])
