from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.PayView.as_view(), name='pay'),
    #url(r'^notify/$', views.NotifyView.as_view(), name='notify'),
]
