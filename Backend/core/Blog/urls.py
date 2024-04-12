from django.urls import path
from .views import *

urlpatterns = [
    path('list/',BlogView.as_view(),name='blog-list'),
    path('create/',BlogView.as_view(),name='blog-create'),
    path('update/',BlogView.as_view(),name='blog-update'),
    path('delete/',BlogView.as_view(),name='blog-delete'),
    path('view/',BlogList.as_view(),name='blog-view'),
]