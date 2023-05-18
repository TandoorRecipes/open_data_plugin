from django.urls import path

from recipes.plugins.open_data_plugin import views
from recipes.settings import DEBUG

urlpatterns = [
    path('', views.test, name='index'),
]

if DEBUG:
    urlpatterns.append(path('test/', views.test, name='view_test'))
