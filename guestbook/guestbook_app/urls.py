from django.conf.urls import include,url
from guestbook_app.views import MainView,SignForm,SignView

urlpatterns = [
    url(r'^sign/$', SignView.as_view(),name="sign" ),
    url(r'^$', MainView.as_view(), name="main")
]
