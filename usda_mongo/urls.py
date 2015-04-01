from django.conf.urls import patterns, url

from .views import FoodDetail, FoodList

urlpatterns = patterns('usda.views',
    url(r'^$', FoodList.as_view(), name='usda-food_list'),
    url(r'^(?P<ndb_number>\d+)/$', FoodDetail.as_view(), name='usda-food_detail'),
)
