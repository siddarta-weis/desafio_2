from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('containers/', containers_list), #list containers GET
    path('containers/create', containers_create), #create container POST
    path('containers/stats/<str:id>', containers_stats),#view status container POST
    path('containers/start', containers_start), #start a container POST
    path('containers/stop', containers_stop), #stop a container POST
    path('containers/<str:id>', containers_remove),#remove container DELETE
    
    path('images/', images_list), #list images GET
    path('images/create', images_create), #create/pull image POST
    path('images/<str:name>', images_remove), #remove image DELETE
    
    path('networks/', networks_list), #list networks GET
    path('networks/create', networks_create), #create network POST
    path('networks/<str:id>', networks_remove), #remove network DELETE
    
    path('volumes/', volumes_list), #list volumes GET
    path('volumes/create', volumes_create), #create volume POST
    path('volumes/<str:name>', volumes_remove), #remove volumes DELETE
]
