from django.conf.urls import include, url
from django.contrib import admin
import posts.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', posts.views.PostView.as_view()),
    url(r'^p/(?P<pk>[0-9]+)/$', posts.views.PostDetailView.as_view(), name='post-detail'),
]
