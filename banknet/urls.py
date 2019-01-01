from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.rating_list, name='rating_list'),
    url(r'^rating_list/(?P<method>(byEuclid|byAngle)+)/$', views.rating_list, name='rating_list'),
    url(r'^correct_weight/$', views.correct_weight, name='correct_weight'),
    url(r'^about/$', views.about, name='about')
]