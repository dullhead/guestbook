from django.conf.urls import include,url
from guestbook_app.views import main_page,sign_post

urlpatterns = [
    url(r'^sign/$', sign_post),
    url(r'^$', main_page)
]
