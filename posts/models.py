from django.db import models
from django.db.models import F
from django.contrib.auth.models import User


class Caption(models.Model):
    post = models.ForeignKey('Post')
    text = models.CharField(max_length=500)
    vote_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
        return '[{}] {}: {}'.format(
            self.vote_count,
            self.created_by.username,
            self.text
        )


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    imgur_id = models.CharField(max_length=50)

    @property
    def image_url(self):
        return "http://i.imgur.com/{}.jpg".format(self.imgur_id)

    @property
    def caption(self):
        return Caption.objects.filter(post=self).order_by('-vote_count').first()

    def __str__(self):
        return self.imgur_id


class Comment(models.Model):
    caption = models.ForeignKey(Caption)
    text = models.CharField(max_length=500)
    vote_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
        return self.text


class Vote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    delta = models.IntegerField(default=1)

    class Meta:
        abstract = True


class CaptionVote(Vote):
    caption = models.ForeignKey(Caption)

    def __str__(self):
        return "Vote ({}): {}".format(self.delta, self.caption)

    def save(self, *args, **kwargs):
        self.caption.vote_count = F('vote_count') + self.delta
        self.caption.save()
        super(CaptionVote, self).save(*args, **kwargs)


class CommentVote(Vote):
    comment = models.ForeignKey(Comment)

    def __str__(self):
        return str(self.comment) + ' (' + self.delta + ')'
